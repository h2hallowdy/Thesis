# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\setup files\NVIDIA\GUI\screens\Configuration.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import time
import serial


class Ui_ConfigurationUI(object):
    ser = 0
    state = False

    def setupUi(self, ConfigurationUI):
        ConfigurationUI.setObjectName("ConfigurationUI")
        ConfigurationUI.resize(290, 601)
        ConfigurationUI.setWindowIcon(QtGui.QIcon('./icons/settings.png'))
        self.centralwidget = QtWidgets.QWidget(ConfigurationUI)
        self.centralwidget.setObjectName("centralwidget")
        self.confiGB = QtWidgets.QGroupBox(self.centralwidget)
        self.confiGB.setGeometry(QtCore.QRect(10, 10, 271, 551))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confiGB.setFont(font)
        self.confiGB.setObjectName("confiGB")
        self.label = QtWidgets.QLabel(self.confiGB)
        self.label.setGeometry(QtCore.QRect(20, 30, 41, 16))
        self.label.setObjectName("label")
        self.nameCb = QtWidgets.QComboBox(self.confiGB)
        self.nameCb.setGeometry(QtCore.QRect(20, 50, 141, 22))
        self.nameCb.setObjectName("nameCb")
        self.nameCb.addItem("")
        self.nameCb.addItem("")
        self.nameCb.addItem("")
        self.nameCb.addItem("")
        self.nameCb.addItem("")
        self.nameCb.addItem("")
        self.nameCb.addItem("")
        self.nameCb.addItem("")
        self.nameCb.addItem("")
        self.nameCb.addItem("")
        self.label_2 = QtWidgets.QLabel(self.confiGB)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 31, 16))
        self.label_2.setObjectName("label_2")
        self.baudCb = QtWidgets.QComboBox(self.confiGB)
        self.baudCb.setGeometry(QtCore.QRect(20, 110, 141, 22))
        self.baudCb.setObjectName("baudCb")
        self.baudCb.addItem("")
        self.baudCb.addItem("")
        self.baudCb.addItem("")
        self.baudCb.addItem("")
        self.baudCb.addItem("")
        self.baudCb.addItem("")
        self.baudCb.addItem("")
        self.label_3 = QtWidgets.QLabel(self.confiGB)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 61, 16))
        self.label_3.setObjectName("label_3")
        self.dataSizeCb = QtWidgets.QComboBox(self.confiGB)
        self.dataSizeCb.setGeometry(QtCore.QRect(20, 170, 141, 22))
        self.dataSizeCb.setObjectName("dataSizeCb")
        self.dataSizeCb.addItem("")
        self.dataSizeCb.addItem("")
        self.label_4 = QtWidgets.QLabel(self.confiGB)
        self.label_4.setGeometry(QtCore.QRect(20, 210, 41, 16))
        self.label_4.setObjectName("label_4")
        self.parityCb = QtWidgets.QComboBox(self.confiGB)
        self.parityCb.setGeometry(QtCore.QRect(20, 230, 141, 22))
        self.parityCb.setObjectName("parityCb")
        self.parityCb.addItem("")
        self.parityCb.addItem("")
        self.parityCb.addItem("")
        self.parityCb.addItem("")
        self.label_5 = QtWidgets.QLabel(self.confiGB)
        self.label_5.setGeometry(QtCore.QRect(20, 270, 71, 16))
        self.label_5.setObjectName("label_5")
        self.handshakeCb = QtWidgets.QComboBox(self.confiGB)
        self.handshakeCb.setGeometry(QtCore.QRect(20, 290, 141, 22))
        self.handshakeCb.setObjectName("handshakeCb")
        self.handshakeCb.addItem("")
        self.handshakeCb.addItem("")
        self.label_6 = QtWidgets.QLabel(self.confiGB)
        self.label_6.setGeometry(QtCore.QRect(20, 330, 41, 16))
        self.label_6.setObjectName("label_6")
        self.modeCb = QtWidgets.QComboBox(self.confiGB)
        self.modeCb.setGeometry(QtCore.QRect(20, 350, 141, 22))
        self.modeCb.setObjectName("modeCb")
        self.modeCb.addItem("")
        self.modeCb.addItem("")
        self.modeCb.addItem("")
        self.openBtn = QtWidgets.QPushButton(self.confiGB)
        self.openBtn.setGeometry(QtCore.QRect(70, 410, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(12)
        self.openBtn.setFont(font)
        self.openBtn.setStyleSheet(
            "background-color: rgb(0, 255, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.openBtn.setObjectName("openBtn")
        self.closeBtn = QtWidgets.QPushButton(self.confiGB)
        self.closeBtn.setEnabled(False)
        self.closeBtn.setGeometry(QtCore.QRect(70, 470, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(12)
        self.closeBtn.setFont(font)
        self.closeBtn.setStyleSheet(
            "background-color: rgba(255, 0, 0, 0.8);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.closeBtn.setObjectName("closeBtn")
        ConfigurationUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ConfigurationUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 290, 21))
        self.menubar.setObjectName("menubar")
        ConfigurationUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ConfigurationUI)
        self.statusbar.setObjectName("statusbar")
        ConfigurationUI.setStatusBar(self.statusbar)

        self.retranslateUi(ConfigurationUI)
        QtCore.QMetaObject.connectSlotsByName(ConfigurationUI)

        # Initialize callbacks and events
        self.openBtn.clicked.connect(self.openPort)
        self.closeBtn.clicked.connect(self.closePort)
        if Ui_ConfigurationUI.state:
            self.openBtn.setEnabled(False)
            self.closeBtn.setEnabled(True)
        else:
            self.openBtn.setEnabled(True)
            self.closeBtn.setEnabled(False)

    def retranslateUi(self, ConfigurationUI):
        _translate = QtCore.QCoreApplication.translate
        ConfigurationUI.setWindowTitle(_translate("ConfigurationUI", "Configuration"))
        self.confiGB.setTitle(_translate("ConfigurationUI", "Serial"))
        self.label.setText(_translate("ConfigurationUI", "Name"))
        self.nameCb.setItemText(0, _translate("ConfigurationUI", "COM1"))
        self.nameCb.setItemText(1, _translate("ConfigurationUI", "COM2"))
        self.nameCb.setItemText(2, _translate("ConfigurationUI", "COM3"))
        self.nameCb.setItemText(3, _translate("ConfigurationUI", "COM4"))
        self.nameCb.setItemText(4, _translate("ConfigurationUI", "COM5"))
        self.nameCb.setItemText(5, _translate("ConfigurationUI", "COM6"))
        self.nameCb.setItemText(6, _translate("ConfigurationUI", "COM7"))
        self.nameCb.setItemText(7, _translate("ConfigurationUI", "COM8"))
        self.nameCb.setItemText(8, _translate("ConfigurationUI", "COM9"))
        self.nameCb.setItemText(9, _translate("ConfigurationUI", "COM11"))
        self.label_2.setText(_translate("ConfigurationUI", "Baud"))
        self.baudCb.setCurrentText(_translate("ConfigurationUI", "9600"))
        self.baudCb.setItemText(0, _translate("ConfigurationUI", "9600"))
        self.baudCb.setItemText(1, _translate("ConfigurationUI", "14400"))
        self.baudCb.setItemText(2, _translate("ConfigurationUI", "19200"))
        self.baudCb.setItemText(3, _translate("ConfigurationUI", "38400"))
        self.baudCb.setItemText(4, _translate("ConfigurationUI", "56000"))
        self.baudCb.setItemText(5, _translate("ConfigurationUI", "57600"))
        self.baudCb.setItemText(6, _translate("ConfigurationUI", "115200"))
        self.label_3.setText(_translate("ConfigurationUI", "Data Size"))
        self.dataSizeCb.setItemText(0, _translate("ConfigurationUI", "8"))
        self.dataSizeCb.setItemText(1, _translate("ConfigurationUI", "7"))
        self.label_4.setText(_translate("ConfigurationUI", "Parity"))
        self.parityCb.setItemText(0, _translate("ConfigurationUI", "none"))
        self.parityCb.setItemText(1, _translate("ConfigurationUI", "odd"))
        self.parityCb.setItemText(2, _translate("ConfigurationUI", "even"))
        self.parityCb.setItemText(3, _translate("ConfigurationUI", "mark"))
        self.label_5.setText(_translate("ConfigurationUI", "Handshake"))
        self.handshakeCb.setItemText(0, _translate("ConfigurationUI", "OFF"))
        self.handshakeCb.setItemText(1, _translate("ConfigurationUI", "RTS/CTS"))
        self.label_6.setText(_translate("ConfigurationUI", "Mode"))
        self.modeCb.setItemText(0, _translate("ConfigurationUI", "Free"))
        self.modeCb.setItemText(1, _translate("ConfigurationUI", "Data"))
        self.modeCb.setItemText(2, _translate("ConfigurationUI", "Setup"))
        self.openBtn.setText(_translate("ConfigurationUI", "Open "))
        self.closeBtn.setText(_translate("ConfigurationUI", "Close "))

    def initSerial(self):
        Ui_ConfigurationUI.ser = serial.Serial()
        # data pre-processing
        port = self.nameCb.currentText()
        baudrate = int(self.baudCb.currentText())
        bytesize = int(self.dataSizeCb.currentText())

        if self.parityCb.currentText() == 'none':
            parity = serial.PARITY_NONE
        elif self.parityCb.currentText() == 'odd':
            parity = serial.PARITY_ODD
        elif self.parityCb.currentText() == 'even':
            parity = serial.PARITY_EVEN
        elif self.parityCb.currentText() == 'mark':
            parity = serial.PARITY_MARK
        
        if self.handshakeCb.currentText() == 'OFF':
            handshake = False
        else:
            handshake = True
        
        # serial communication init
        Ui_ConfigurationUI.ser.port = port
        Ui_ConfigurationUI.ser.baudrate = baudrate
        Ui_ConfigurationUI.ser.bytesize = bytesize
        Ui_ConfigurationUI.ser.parity = parity
        Ui_ConfigurationUI.ser.rtscts = handshake
        print(Ui_ConfigurationUI.ser)
        

    def openPort(self):
        self.initSerial()
        Ui_ConfigurationUI.ser.open()
        if Ui_ConfigurationUI.ser.isOpen() ==  True:
            message = Ui_ConfigurationUI.ser.port + ' is opened'
            self.createMessageBox(message)
        self.openBtn.setEnabled(False)
        self.closeBtn.setEnabled(True)
        if Ui_ConfigurationUI.state is not True:
            Ui_ConfigurationUI.state = True

    def closePort(self):
        print(Ui_ConfigurationUI.ser)
        self.initSerial()
        if Ui_ConfigurationUI.ser.isOpen() == True:
            Ui_ConfigurationUI.ser.close()
            message = Ui_ConfigurationUI.ser.port + ' is closed'
            self.createMessageBox(message)
        Ui_ConfigurationUI.state = False
        self.openBtn.setEnabled(True)
        self.closeBtn.setEnabled(False)

    def createMessageBox(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setMinimumSize(QtCore.QSize(300, 200))
        msg.setText(message)
        msg.setWindowTitle("Information")
        msg.exec_()
        
    def closeGui(self):
        print(Ui_ConfigurationUI.state)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigurationUI = QtWidgets.QMainWindow()
    ui = Ui_ConfigurationUI()
    ui.setupUi(ConfigurationUI)
    # App about to quit event
    # app.aboutToQuit.connect(ui.closeGui)
    ######################################################################
    ConfigurationUI.show()
    sys.exit(app.exec_())

