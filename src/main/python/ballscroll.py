import pyautogui
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QSystemTrayIcon, QMenu, QAction
from numpy import newaxis
from tensorflow import keras
from mainwindow import Ui_MainWindow
from mousePos import getDirection


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
        self.model_path = ''
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
        self.settings_dict = {
            'tick': 10,
            'delay': 10,
            'power': 100
        }
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.browseButton.clicked.connect(self.browse)

    def start(self):
        try:
            if self.model_path != self.fileEdit.text():
                self.model_path = self.fileEdit.text()
                self.model = keras.models.load_model(self.model_path)
                self.statusBar().showMessage('Файл загружен', 10000)
                self.max_length = self.model.input_shape[1]
            self.settings_dict['delay'] = int(self.delayEdit.text())
            self.settings_dict['power'] = int(self.scrollEdit.text())
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.startAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.timer_id = self.startTimer(self.settings_dict['tick'])
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
            elif self.zero_count == self.settings_dict['delay']:
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
                        pyautogui.scroll(self.movement_sign[predicted]*self.settings_dict['power'])
                self.zero_count = self.zero_count + 1
            elif self.zero_count < self.settings_dict['delay']:
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
