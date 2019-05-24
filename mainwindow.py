# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Lenovo\PycharmProjects\BallScroll\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(449, 194)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.typeLabel = QtWidgets.QLabel(self.centralwidget)
        self.typeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.typeLabel.setObjectName("typeLabel")
        self.verticalLayout.addWidget(self.typeLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.fileEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.fileEdit.setObjectName("fileEdit")
        self.horizontalLayout.addWidget(self.fileEdit)
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setObjectName("browseButton")
        self.horizontalLayout.addWidget(self.browseButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.tickEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.tickEdit.setObjectName("tickEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tickEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout_2.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setEnabled(False)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_2.addWidget(self.stopButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 449, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BallScroll"))
        self.typeLabel.setText(_translate("MainWindow", "Ничего"))
        self.label.setText(_translate("MainWindow", "Классификатор"))
        self.browseButton.setText(_translate("MainWindow", "Обзор"))
        self.label_2.setText(_translate("MainWindow", "Интервал"))
        self.startButton.setText(_translate("MainWindow", "Старт"))
        self.stopButton.setText(_translate("MainWindow", "Стоп"))

