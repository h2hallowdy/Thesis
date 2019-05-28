# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\setup files\NVIDIA\GUI\screens\MainControllerV2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainControllerUI(object):
    def setupUi(self, MainControllerUI):
        MainControllerUI.setObjectName("MainControllerUI")
        MainControllerUI.resize(1396, 771)
        self.centralwidget = QtWidgets.QWidget(MainControllerUI)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.liveVidGB = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        self.liveVidGB.setFont(font)
        self.liveVidGB.setStyleSheet("border-style: solid;\n"
"border-width: 1px;")
        self.liveVidGB.setObjectName("liveVidGB")
        self.liveVidFrame = QtWidgets.QLabel(self.liveVidGB)
        self.liveVidFrame.setGeometry(QtCore.QRect(10, 20, 760, 640))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.liveVidFrame.sizePolicy().hasHeightForWidth())
        self.liveVidFrame.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.liveVidFrame.setFont(font)
        self.liveVidFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.liveVidFrame.setText("")
        self.liveVidFrame.setObjectName("liveVidFrame")
        self.gridLayout_2.addWidget(self.liveVidGB, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.armPosGB = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.armPosGB.setFont(font)
        self.armPosGB.setStyleSheet("border-style: solid;\n"
"border-width: 1px;")
        self.armPosGB.setObjectName("armPosGB")
        self.label = QtWidgets.QLabel(self.armPosGB)
        self.label.setGeometry(QtCore.QRect(10, 30, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("border-style: none;")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.armPosGB)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border-style: none;")
        self.label_3.setObjectName("label_3")
        self.xCurLbl = QtWidgets.QLabel(self.armPosGB)
        self.xCurLbl.setGeometry(QtCore.QRect(90, 30, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.xCurLbl.setFont(font)
        self.xCurLbl.setStyleSheet("border-style: none;")
        self.xCurLbl.setText("")
        self.xCurLbl.setObjectName("xCurLbl")
        self.yCurLbl = QtWidgets.QLabel(self.armPosGB)
        self.yCurLbl.setGeometry(QtCore.QRect(90, 60, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.yCurLbl.setFont(font)
        self.yCurLbl.setStyleSheet("border-style: none;")
        self.yCurLbl.setText("")
        self.yCurLbl.setObjectName("yCurLbl")
        self.label_4 = QtWidgets.QLabel(self.armPosGB)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("border-style: none;")
        self.label_4.setObjectName("label_4")
        self.zCurLbl = QtWidgets.QLabel(self.armPosGB)
        self.zCurLbl.setGeometry(QtCore.QRect(90, 90, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.zCurLbl.setFont(font)
        self.zCurLbl.setStyleSheet("border-style: none;")
        self.zCurLbl.setText("")
        self.zCurLbl.setObjectName("zCurLbl")
        self.gridLayout.addWidget(self.armPosGB, 0, 0, 1, 1)
        self.statusGB = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.statusGB.setFont(font)
        self.statusGB.setStyleSheet("border-style: solid;\n"
"border-width: 1px;")
        self.statusGB.setObjectName("statusGB")
        self.connectionLbl = QtWidgets.QLabel(self.statusGB)
        self.connectionLbl.setGeometry(QtCore.QRect(10, 20, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.connectionLbl.setFont(font)
        self.connectionLbl.setStyleSheet("border-style: none;")
        self.connectionLbl.setObjectName("connectionLbl")
        self.label_2 = QtWidgets.QLabel(self.statusGB)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("border-style: none;")
        self.label_2.setObjectName("label_2")
        self.sttLbl = QtWidgets.QLabel(self.statusGB)
        self.sttLbl.setGeometry(QtCore.QRect(60, 50, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sttLbl.setFont(font)
        self.sttLbl.setStyleSheet("border-style: none;")
        self.sttLbl.setObjectName("sttLbl")
        self.configBtn = QtWidgets.QPushButton(self.statusGB)
        self.configBtn.setGeometry(QtCore.QRect(10, 70, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.configBtn.setFont(font)
        self.configBtn.setStyleSheet("background-color: orange;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"border-color: black;\n"
"")
        self.configBtn.setObjectName("configBtn")
        self.gridLayout.addWidget(self.statusGB, 0, 1, 1, 1)
        self.proPosGB = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.proPosGB.setFont(font)
        self.proPosGB.setStyleSheet("border-style: solid;\n"
"border-width: 1px;")
        self.proPosGB.setObjectName("proPosGB")
        self.label_5 = QtWidgets.QLabel(self.proPosGB)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("border-style: none;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.proPosGB)
        self.label_6.setGeometry(QtCore.QRect(10, 80, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("border-style: none;")
        self.label_6.setObjectName("label_6")
        self.xProLbl = QtWidgets.QLabel(self.proPosGB)
        self.xProLbl.setGeometry(QtCore.QRect(90, 40, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.xProLbl.setFont(font)
        self.xProLbl.setStyleSheet("border-style: none;")
        self.xProLbl.setObjectName("xProLbl")
        self.yProLbl = QtWidgets.QLabel(self.proPosGB)
        self.yProLbl.setGeometry(QtCore.QRect(90, 80, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.yProLbl.setFont(font)
        self.yProLbl.setStyleSheet("border-style: none;")
        self.yProLbl.setObjectName("yProLbl")
        self.gridLayout.addWidget(self.proPosGB, 1, 0, 1, 1)
        self.calibGB = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.calibGB.setFont(font)
        self.calibGB.setStyleSheet("border-style: solid;\n"
"border-width: 1px;")
        self.calibGB.setObjectName("calibGB")
        self.armHomeBtn = QtWidgets.QPushButton(self.calibGB)
        self.armHomeBtn.setGeometry(QtCore.QRect(10, 30, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.armHomeBtn.setFont(font)
        self.armHomeBtn.setStyleSheet("background-color: rgb(0, 255, 0);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"border-color: black;\n"
"")
        self.armHomeBtn.setObjectName("armHomeBtn")
        self.camHomeBtn = QtWidgets.QPushButton(self.calibGB)
        self.camHomeBtn.setGeometry(QtCore.QRect(10, 80, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.camHomeBtn.setFont(font)
        self.camHomeBtn.setStyleSheet("background-color: rgb(0, 255, 0);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"border-color: black;\n"
"")
        self.camHomeBtn.setObjectName("camHomeBtn")
        self.teachingCamBtn = QtWidgets.QPushButton(self.calibGB)
        self.teachingCamBtn.setGeometry(QtCore.QRect(130, 80, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.teachingCamBtn.setFont(font)
        self.teachingCamBtn.setStyleSheet("\n"
"background-color: rgb(255, 255, 0);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"border-color: black;\n"
"")
        self.teachingCamBtn.setObjectName("teachingCamBtn")
        self.armTestingBtn = QtWidgets.QPushButton(self.calibGB)
        self.armTestingBtn.setGeometry(QtCore.QRect(130, 30, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.armTestingBtn.setFont(font)
        self.armTestingBtn.setStyleSheet("\n"
"background-color: rgb(255, 255, 0);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"border-color: black;\n"
"")
        self.armTestingBtn.setObjectName("armTestingBtn")
        self.gridLayout.addWidget(self.calibGB, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.controlGB = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.controlGB.setFont(font)
        self.controlGB.setStyleSheet("border-style: solid;\n"
"border-width: 1px;")
        self.controlGB.setObjectName("controlGB")
        self.autoBtn = QtWidgets.QPushButton(self.controlGB)
        self.autoBtn.setGeometry(QtCore.QRect(70, 20, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.autoBtn.setFont(font)
        self.autoBtn.setStyleSheet("background-color: rgb(85, 255, 0);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"border-color: black;\n"
"")
        self.autoBtn.setObjectName("autoBtn")
        self.armTestingBtn_2 = QtWidgets.QPushButton(self.controlGB)
        self.armTestingBtn_2.setGeometry(QtCore.QRect(160, 20, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.armTestingBtn_2.setFont(font)
        self.armTestingBtn_2.setStyleSheet("background-color: rgb(255, 85, 0);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"border-color: black;\n"
"")
        self.armTestingBtn_2.setObjectName("armTestingBtn_2")
        self.modeSlider = QtWidgets.QSlider(self.controlGB)
        self.modeSlider.setGeometry(QtCore.QRect(370, 20, 41, 31))
        self.modeSlider.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.modeSlider.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: white;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
"    stop: 0 #66e, stop: 1 #bbf);\n"
"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
"    stop: 0 #bbf, stop: 1 #55f);\n"
"border: 1px solid #777;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: #fff;\n"
"border: 1px solid #777;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #eee, stop:1 #ccc);\n"
"border: 1px solid #777;\n"
"width: 13px;\n"
"margin-top: -2px;\n"
"margin-bottom: -2px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #fff, stop:1 #ddd);\n"
"border: 1px solid #444;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.modeSlider.setMaximum(1)
        self.modeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.modeSlider.setInvertedAppearance(False)
        self.modeSlider.setObjectName("modeSlider")
        self.label_7 = QtWidgets.QLabel(self.controlGB)
        self.label_7.setGeometry(QtCore.QRect(330, 20, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("border: none;")
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.controlGB)
        self.processGB = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.processGB.setFont(font)
        self.processGB.setStyleSheet("border-style: solid;\n"
"border-width: 1px;")
        self.processGB.setObjectName("processGB")
        self.verticalLayout.addWidget(self.processGB)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 12)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.setStretch(0, 4)
        self.verticalLayout_2.setStretch(1, 7)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 7)
        self.gridLayout_2.setColumnStretch(1, 5)
        MainControllerUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainControllerUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1396, 21))
        self.menubar.setObjectName("menubar")
        MainControllerUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainControllerUI)
        self.statusbar.setObjectName("statusbar")
        MainControllerUI.setStatusBar(self.statusbar)

        self.retranslateUi(MainControllerUI)
        QtCore.QMetaObject.connectSlotsByName(MainControllerUI)

    def retranslateUi(self, MainControllerUI):
        _translate = QtCore.QCoreApplication.translate
        MainControllerUI.setWindowTitle(_translate("MainControllerUI", "Main Controller-MC"))
        self.liveVidGB.setTitle(_translate("MainControllerUI", "Live Cam"))
        self.armPosGB.setTitle(_translate("MainControllerUI", "Arm Position"))
        self.label.setText(_translate("MainControllerUI", "X Position:"))
        self.label_3.setText(_translate("MainControllerUI", "Y Position:"))
        self.label_4.setText(_translate("MainControllerUI", "Z Position:"))
        self.statusGB.setTitle(_translate("MainControllerUI", "Status"))
        self.connectionLbl.setText(_translate("MainControllerUI", "Connection: UART"))
        self.label_2.setText(_translate("MainControllerUI", "Status:"))
        self.sttLbl.setText(_translate("MainControllerUI", "Disconnect"))
        self.configBtn.setText(_translate("MainControllerUI", "Configuration "))
        self.proPosGB.setTitle(_translate("MainControllerUI", "Product Position"))
        self.label_5.setText(_translate("MainControllerUI", "X Position:"))
        self.label_6.setText(_translate("MainControllerUI", "Y Position:"))
        self.xProLbl.setText(_translate("MainControllerUI", "TextLabel"))
        self.yProLbl.setText(_translate("MainControllerUI", "TextLabel"))
        self.calibGB.setTitle(_translate("MainControllerUI", "Calibration"))
        self.armHomeBtn.setText(_translate("MainControllerUI", "Arm Homing "))
        self.camHomeBtn.setText(_translate("MainControllerUI", "Cam Homing "))
        self.teachingCamBtn.setText(_translate("MainControllerUI", "Cam teaching "))
        self.armTestingBtn.setText(_translate("MainControllerUI", "Arm Teaching"))
        self.controlGB.setTitle(_translate("MainControllerUI", "Control"))
        self.autoBtn.setText(_translate("MainControllerUI", "Auto"))
        self.armTestingBtn_2.setText(_translate("MainControllerUI", "Manual"))
        self.label_7.setText(_translate("MainControllerUI", "Mode"))
        self.processGB.setTitle(_translate("MainControllerUI", "Process"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainControllerUI = QtWidgets.QMainWindow()
    ui = Ui_MainControllerUI()
    ui.setupUi(MainControllerUI)
    MainControllerUI.show()
    sys.exit(app.exec_())

