# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\setup files\NVIDIA\GUI\screens\ManualMode.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import serial
import logging
from time_util import *
class Ui_ManualMode(object):
    ser = serial.Serial()
    def __init__(self, ser, LOG_FILE_NAME):
        super(Ui_ManualMode, self).__init__()
        self.ser = ser
        self.FILE_LOG = LOG_FILE_NAME
        

    def setupUi(self, ManualMode):
        ManualMode.setObjectName("ManualMode")
        ManualMode.resize(409, 223)
        ManualMode.setWindowIcon(QtGui.QIcon('./icons/test.png'))
        self.firstMGB = QtWidgets.QGroupBox(ManualMode)
        self.firstMGB.setGeometry(QtCore.QRect(10, 10, 191, 61))
        self.firstMGB.setObjectName("firstMGB")
        self.label = QtWidgets.QLabel(self.firstMGB)
        self.label.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.label.setObjectName("label")
        self.firstMEdit = QtWidgets.QLineEdit(self.firstMGB)
        self.firstMEdit.setGeometry(QtCore.QRect(50, 20, 113, 20))
        self.firstMEdit.setObjectName("firstMEdit")
        self.firstMGB_2 = QtWidgets.QGroupBox(ManualMode)
        self.firstMGB_2.setGeometry(QtCore.QRect(10, 90, 191, 61))
        self.firstMGB_2.setObjectName("firstMGB_2")
        self.label_2 = QtWidgets.QLabel(self.firstMGB_2)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.label_2.setObjectName("label_2")
        self.secMEdit = QtWidgets.QLineEdit(self.firstMGB_2)
        self.secMEdit.setGeometry(QtCore.QRect(50, 20, 113, 20))
        self.secMEdit.setObjectName("secMEdit")
        self.firstMGB_3 = QtWidgets.QGroupBox(ManualMode)
        self.firstMGB_3.setGeometry(QtCore.QRect(210, 10, 191, 61))
        self.firstMGB_3.setObjectName("firstMGB_3")
        self.label_3 = QtWidgets.QLabel(self.firstMGB_3)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.label_3.setObjectName("label_3")
        self.thirdMEdit = QtWidgets.QLineEdit(self.firstMGB_3)
        self.thirdMEdit.setGeometry(QtCore.QRect(50, 20, 113, 20))
        self.thirdMEdit.setObjectName("thirdMEdit")
        self.firstMGB_4 = QtWidgets.QGroupBox(ManualMode)
        self.firstMGB_4.setGeometry(QtCore.QRect(210, 90, 191, 61))
        self.firstMGB_4.setObjectName("firstMGB_4")
        self.label_4 = QtWidgets.QLabel(self.firstMGB_4)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.label_4.setObjectName("label_4")
        self.fourMEdit = QtWidgets.QLineEdit(self.firstMGB_4)
        self.fourMEdit.setGeometry(QtCore.QRect(50, 20, 113, 20))
        self.fourMEdit.setObjectName("fourMEdit")
        self.sendManualBtn = QtWidgets.QPushButton(ManualMode)
        self.sendManualBtn.setGeometry(QtCore.QRect(150, 170, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sendManualBtn.setFont(font)
        self.sendManualBtn.setStyleSheet("background-color: rgb(0, 255, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.sendManualBtn.setObjectName("sendManualBtn")

        self.sendManualBtn.clicked.connect(self.SendTestMotor)

        self.retranslateUi(ManualMode)
        QtCore.QMetaObject.connectSlotsByName(ManualMode)


    def retranslateUi(self, ManualMode):
        _translate = QtCore.QCoreApplication.translate
        ManualMode.setWindowTitle(_translate("ManualMode", "Manual Control"))
        self.firstMGB.setTitle(_translate("ManualMode", "Motor 1"))
        self.label.setText(_translate("ManualMode", "Angle:"))
        self.firstMGB_2.setTitle(_translate("ManualMode", "Motor 2"))
        self.label_2.setText(_translate("ManualMode", "Angle:"))
        self.firstMGB_3.setTitle(_translate("ManualMode", "Motor 3"))
        self.label_3.setText(_translate("ManualMode", "Angle:"))
        self.firstMGB_4.setTitle(_translate("ManualMode", "Motor 4"))
        self.label_4.setText(_translate("ManualMode", "Angle:"))
        self.sendManualBtn.setText(_translate("ManualMode", "Send"))

    def SendTestMotor(self):
        if self.firstMEdit.text() != "":
            if '-' in self.firstMEdit.text():
                num = self.firstMEdit.text().split('-')[1]
                num = '{:03d}'.format(int(num))
                motor1Angle = '0' + num
            else:
                motor1Angle = '1' + '{:03d}'.format(int(self.firstMEdit.text()))
        else:
            motor1Angle = '0000'
        if self.secMEdit.text() != '':
            if '-' in self.secMEdit.text():
                num = self.secMEdit.text().split('-')[1]
                num = '{:03d}'.format(int(num))
                motor2Angle = '0' + num
            else:
                motor2Angle = '1' + '{:03d}'.format(int(self.secMEdit.text()))
        else:
            motor2Angle = '0000'
        if self.thirdMEdit.text() != '':
            if '-' in self.thirdMEdit.text():
                num = self.thirdMEdit.text().split('-')[1]
                num = '{:03d}'.format(int(num))
                motor3Angle = '0' + num
            else:
                motor3Angle = '1' + '{:03d}'.format(int(self.thirdMEdit.text()))
        else:
            motor3Angle = '0000'
        if self.fourMEdit.text() != '':
            if '-' in self.fourMEdit.text():
                num = self.fourMEdit.text().split('-')[1]
                num = '{:03d}'.format(int(num))
                motor4Angle = '0' + num
            else:
                motor4Angle = '1' + '{:03d}'.format(int(self.fourMEdit.text()))
        else:
            motor4Angle = '0000'
        
        message = 't' + '-' + motor1Angle + '-' + motor2Angle + '-' + motor3Angle + '-' + motor4Angle
        # message = 't1-154-184'
        message_bytes = bytes(message , encoding='utf-8')
        self.ser.write(message_bytes)
        logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
        t_log = GetTime()
        logging.info(t_log + ': Send- ' + message)
       
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManualMode = QtWidgets.QWidget()
    ui = Ui_ManualMode()
    ui.setupUi(ManualMode)
    ManualMode.show()
    sys.exit(app.exec_())

