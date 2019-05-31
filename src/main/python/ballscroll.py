import pyautogui
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from numpy import newaxis
from tensorflow import keras
from mainwindow import Ui_MainWindow
from mousePos import getDirection
from configparser import ConfigParser


class BallScroll(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = None
        self.timer_id = 0
        self.x_prev = 0
        self.y_prev = 0
        self.code = []
        self.recordStart = False
        self.zero_count = 0
        self.max_length = 100
        self.isTrayClose = False
        # tray menu
        self.trayIcon = QSystemTrayIcon(self.windowIcon(), self)
        self.trayIcon.setToolTip('BallScroll')
        self.trayMenu = QMenu(self)
        self.openWindowAction = QAction('Развернуть', self)
        self.startAction = QAction('Старт', self)
        self.stopAction = QAction('Стоп', self)
        self.closeAction = QAction('Выйти', self)
        self.openWindowAction.triggered.connect(self.show)
        self.closeAction.triggered.connect(self.trayClose)
        self.startAction.triggered.connect(self.start)
        self.stopAction.triggered.connect(self.stop)
        self.stopAction.setEnabled(False)
        self.trayMenu.addActions([self.openWindowAction, self.startAction, self.stopAction, self.closeAction])
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.activated.connect(self.trayActivated)
        self.trayIcon.show()
        # settings
        self.config = ConfigParser()
        try:
            with open('config.ini', 'r') as config_file:
                self.config.read_file(config_file)
                self.initUI()
        except FileNotFoundError:
            self.setDefaultSettings()

        self.movement_types = {
            0: 'Ничего',
            1: 'Прокрутра вниз',
            2: 'Прокрутка вверх'
        }
        self.movement_sign = {
            0: 0,
            1: -1,
            2: 1
        }

        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.browseButton.clicked.connect(self.browse)
        # validators
        self.delay_validator = QRegExpValidator(QRegExp(r'\d+'), self)
        self.scroll_validator = QRegExpValidator(QRegExp(r'-?\d+'), self)
        self.delayEdit.setValidator(self.delay_validator)
        self.scrollEdit.setValidator(self.scroll_validator)

    def start(self):
        try:
            if self.config['model']['file'] != self.fileEdit.text():
                self.config['model']['file'] = self.fileEdit.text()
                self.model = keras.models.load_model(self.config['model']['file'])
                self.statusBar().showMessage('Файл загружен', 10000)
                self.max_length = self.model.input_shape[1]
            self.config['mouse']['delay'] = self.delayEdit.text()
            self.config['mouse']['power'] = self.scrollEdit.text()
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.startAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.timer_id = self.startTimer(int(self.config['mouse']['tick']))
        except ValueError:
            self.statusBar().showMessage('Неверный файл')
        except ImportError:
            self.statusBar().showMessage('Файл недоступен')

    def timerEvent(self, event):
        x, y = pyautogui.position()
        if self.recordStart:
            if (x, y) != (self.x_prev, self.y_prev):
                self.code.append(getDirection(self.x_prev, self.y_prev, x, y))
                self.zero_count = 0
            elif self.zero_count == int(self.config['mouse']['delay']):
                self.recordStart = False
                if len(self.code) <= self.max_length:
                    if len(self.code) < self.max_length:
                        self.code.extend([0]*(self.max_length - len(self.code)))
                    code_cat = keras.utils.to_categorical(self.code, 10)
                    code_cat = code_cat[newaxis, :, :]
                    predicted = self.model.predict(code_cat)
                    predicted = predicted.argmax()
                    move_type = self.movement_types[predicted]
                    self.typeLabel.setText(move_type)
                    print(predicted)
                    if predicted:
                        pyautogui.scroll(self.movement_sign[predicted] * int(self.config['mouse']['power']))
                self.zero_count = self.zero_count + 1
            elif self.zero_count < int(self.config['mouse']['delay']):
                self.zero_count = self.zero_count + 1
        else:
            if (x, y) != (self.x_prev, self.y_prev):
                self.code.clear()
                self.recordStart = True

        self.x_prev = x
        self.y_prev = y
        event.accept()

    def stop(self):
        self.killTimer(self.timer_id)
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.startAction.setEnabled(True)
        self.stopAction.setEnabled(False)

    def browse(self):
        file_path = QFileDialog.getOpenFileName(self, 'Выбор классиикатора', '.', 'hdf5 files (*.h5 *.hdf5)')
        if file_path[0]:
            self.fileEdit.setText(file_path[0])

    def closeEvent(self, event):
        if self.isTrayClose:
            with open('config.ini', 'w') as config_file:
                self.config.write(config_file)
            event.accept()
        else:
            self.hide()
            event.ignore()

    def trayActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger or reason == QSystemTrayIcon.DoubleClick:
            if not self.isVisible():
                self.show()

    def trayClose(self):
        self.isTrayClose = True
        self.close()

    def setDefaultSettings(self):
        self.config['DEFAULT'] = {
            'delay': '10',
            'tick': '10',
            'power': '2',
            'file': ''
        }
        self.config['mouse'] = {}
        self.config['model'] = {}
        with open('config.ini', 'w') as config_file:
            self.config.write(config_file)

    def initUI(self):
        self.fileEdit.setText(self.config['model']['file'])
        self.delayEdit.setText(self.config['mouse']['delay'])
        self.scrollEdit.setText((self.config['mouse']['power']))
