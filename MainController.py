
#region: Import all modules neccessary
from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from main import Ui_MainWindow
from Configuration import Ui_ConfigurationUI
from ManualMode import Ui_ManualMode
from time_util import *
from numbers_util import *
import threading
import numpy as np
import time
import serial
import array
import logging
import cv2
import os
from datetime import datetime
from ObjectDetection import ObjectDetection
from Camera import Camera
from Calibration import *
#endregion

class Ui_MainControllerUI(object):
    stateCollect = False
    state = False
    event = threading.Event()
    stateLiveView = False
    stateAutoMode = False
    stateProcess = False
    stateHoming = False
    mode = 1
    # running = threading.Event()
    # running.set()
    ser = serial.Serial()
    # ser = serial.Serial()
    # ser.port = "COM1"
    def __init__(self, camera=None):
        super(Ui_MainControllerUI, self).__init__()
        self.homeX = 0
        self.homeY = 0
        # self.camera = Camera(0)
        
        self.od = ObjectDetection()
        t_filename = GetTimeForFile()
        self.FILE_LOG = 'logs/' + t_filename + '.log'
        logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
        t_log = GetTime()
        logging.info(t_log + ': Initialize the software...Connected')
        self.count = 0
        self.sumX = 0
        self.sumY = 0
        self.sumAngle = 0
        self.positionDictionary = {
            '1': [15, 20, 90],
            '2': [20, 20, 90],
            '3': [25, 20, 90],
            '4': [15, 25, 90],
            '5': [20, 25, 90],
            '6': [25, 25, 90],
        }
        self.objectCounting = 0
        self.currentDestination = 1
        self.myTimer = QtCore.QTimer()
        self.myTimer.timeout.connect(self.SendDestination)
        self.runAgain = QtCore.QTimer()
        self.runAgain.timeout.connect(self.RunAgain)
        try:
            with np.load('Calib.npz') as X:
                self.mtx, self.dist, self.rvects, self.tvects, self.corners = [X[i] for i in ('mtx','dist','rvecs','tvecs', 'corners')]
                print(self.mtx)
           
            self.rodrigues_Vecs = InverseRodrigues(self.rvects)
            translate = np.reshape(self.tvects, (3, 1))
            K = np.concatenate((self.rodrigues_Vecs, translate), axis=1)
            a = self.mtx.dot(K).dot(np.array([[1, 1, 1, 1]]).T)
            self.s = a.item(2)
            print(self.s)
        except:
            print('error occured')

    def setupUi(self, MainControllerUI):
        MainControllerUI.setObjectName("MainControllerUI")
        MainControllerUI.resize(1196, 592)
        MainControllerUI.setWindowIcon(QtGui.QIcon('./icons/joystick.png'))
        self.centralwidget = QtWidgets.QWidget(MainControllerUI)
        self.centralwidget.setObjectName("centralwidget")
        self.statusGB = QtWidgets.QGroupBox(self.centralwidget)
        self.statusGB.setGeometry(QtCore.QRect(940, 10, 251, 131))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.statusGB.setFont(font)
        self.statusGB.setStyleSheet("border-style: solid;\n"
        "border-width: 1px;")
        self.statusGB.setObjectName("statusGB")
        self.connectionLbl = QtWidgets.QLabel(self.statusGB)
        self.connectionLbl.setGeometry(QtCore.QRect(10, 30, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.connectionLbl.setFont(font)
        self.connectionLbl.setStyleSheet("border-style: none;")
        self.connectionLbl.setObjectName("connectionLbl")
        self.label_2 = QtWidgets.QLabel(self.statusGB)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("border-style: none;")
        self.label_2.setObjectName("label_2")
        self.sttLbl = QtWidgets.QLabel(self.statusGB)
        self.sttLbl.setGeometry(QtCore.QRect(60, 60, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sttLbl.setFont(font)
        self.sttLbl.setStyleSheet("border-style: none;")
        self.sttLbl.setObjectName("sttLbl")
        self.configBtn = QtWidgets.QPushButton(self.statusGB)
        self.configBtn.setGeometry(QtCore.QRect(10, 90, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(11)
        self.configBtn.setFont(font)
        self.configBtn.setStyleSheet(
            "background-color: orange;\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.configBtn.setObjectName("configBtn")
        self.calibGB = QtWidgets.QGroupBox(self.centralwidget)
        self.calibGB.setGeometry(QtCore.QRect(940, 150, 251, 121))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
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
        self.armHomeBtn.setStyleSheet(
            "background-color: rgb(0, 255, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.armHomeBtn.setObjectName("armHomeBtn")
        self.camHomeBtn = QtWidgets.QPushButton(self.calibGB)
        self.camHomeBtn.setGeometry(QtCore.QRect(10, 80, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.camHomeBtn.setFont(font)
        self.camHomeBtn.setStyleSheet(
            "background-color: rgb(0, 255, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.camHomeBtn.setObjectName("camHomeBtn")
        self.teachingCamBtn = QtWidgets.QPushButton(self.calibGB)
        self.teachingCamBtn.setGeometry(QtCore.QRect(130, 80, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.teachingCamBtn.setFont(font)
        self.teachingCamBtn.setStyleSheet(
            "background-color: rgb(255, 255, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.teachingCamBtn.setObjectName("teachingCamBtn")
        self.armTestingBtn = QtWidgets.QPushButton(self.calibGB)
        self.armTestingBtn.setGeometry(QtCore.QRect(130, 30, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.armTestingBtn.setFont(font)
        self.armTestingBtn.setStyleSheet(
            "background-color: rgb(255, 255, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.armTestingBtn.setObjectName("armTestingBtn")
        self.armPosGB = QtWidgets.QGroupBox(self.centralwidget)
        self.armPosGB.setGeometry(QtCore.QRect(730, 10, 201, 131))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.armPosGB.setFont(font)
        self.armPosGB.setStyleSheet("border-style: solid;\n"
        "border-width: 1px;")
        self.armPosGB.setObjectName("armPosGB")
        self.label = QtWidgets.QLabel(self.armPosGB)
        self.label.setGeometry(QtCore.QRect(10, 30, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setStyleSheet("border-style: none;")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.armPosGB)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border-style: none;")
        self.label_3.setObjectName("label_3")
        self.xCurLbl = QtWidgets.QLabel(self.armPosGB)
        self.xCurLbl.setGeometry(QtCore.QRect(90, 30, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        self.xCurLbl.setFont(font)
        self.xCurLbl.setStyleSheet("border-style: none;")
        self.xCurLbl.setText("")
        self.xCurLbl.setObjectName("xCurLbl")
        self.yCurLbl = QtWidgets.QLabel(self.armPosGB)
        self.yCurLbl.setGeometry(QtCore.QRect(90, 60, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        self.yCurLbl.setFont(font)
        self.yCurLbl.setStyleSheet("border-style: none;")
        self.yCurLbl.setText("")
        self.yCurLbl.setObjectName("yCurLbl")
        self.label_4 = QtWidgets.QLabel(self.armPosGB)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("border-style: none;")
        self.label_4.setObjectName("label_4")
        self.zCurLbl = QtWidgets.QLabel(self.armPosGB)
        self.zCurLbl.setGeometry(QtCore.QRect(90, 90, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        self.zCurLbl.setFont(font)
        self.zCurLbl.setStyleSheet("border-style: none;")
        self.zCurLbl.setText("")
        self.zCurLbl.setObjectName("zCurLbl")
        self.proPosGB = QtWidgets.QGroupBox(self.centralwidget)
        self.proPosGB.setGeometry(QtCore.QRect(730, 150, 201, 121))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.proPosGB.setFont(font)
        self.proPosGB.setStyleSheet("border-style: solid;\n"
        "border-width: 1px;")
        self.proPosGB.setObjectName("proPosGB")
        self.label_5 = QtWidgets.QLabel(self.proPosGB)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("border-style: none;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.proPosGB)
        self.label_6.setGeometry(QtCore.QRect(10, 80, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("border-style: none;")
        self.label_6.setObjectName("label_6")
        self.xProLbl = QtWidgets.QLabel(self.proPosGB)
        self.xProLbl.setGeometry(QtCore.QRect(90, 40, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.xProLbl.setFont(font)
        self.xProLbl.setStyleSheet("border-style: none;")
        self.xProLbl.setObjectName("xProLbl")
        self.yProLbl = QtWidgets.QLabel(self.proPosGB)
        self.yProLbl.setGeometry(QtCore.QRect(90, 80, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.yProLbl.setFont(font)
        self.yProLbl.setStyleSheet("border-style: none;")
        self.yProLbl.setObjectName("yProLbl")
        self.controlGB = QtWidgets.QGroupBox(self.centralwidget)
        self.controlGB.setGeometry(QtCore.QRect(730, 280, 461, 71))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.controlGB.setFont(font)
        self.controlGB.setStyleSheet("border-style: solid;\n"
        "border-width: 1px;")
        self.controlGB.setObjectName("controlGB")
        self.autoBtn = QtWidgets.QPushButton(self.controlGB)
        self.autoBtn.setGeometry(QtCore.QRect(100, 20, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(11)
        self.autoBtn.setFont(font)
        self.autoBtn.setStyleSheet(
            "background-color: rgb(85, 255, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.autoBtn.setObjectName("autoBtn")
        self.manualBtn = QtWidgets.QPushButton(self.controlGB)
        self.manualBtn.setGeometry(QtCore.QRect(250, 20, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(11)
        self.manualBtn.setFont(font)
        self.manualBtn.setStyleSheet(
            "background-color: rgb(255, 85, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
        self.manualBtn.setObjectName("manualBtn")
        self.processGB = QtWidgets.QGroupBox(self.centralwidget)
        self.processGB.setGeometry(QtCore.QRect(730, 360, 461, 191))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.processGB.setFont(font)
        self.processGB.setStyleSheet("border-style: solid;\n"
        "border-width: 1px;")
        self.processGB.setObjectName("processGB")
        self.processImgFrame = QtWidgets.QLabel(self.processGB)
        self.processImgFrame.setGeometry(QtCore.QRect(10, 20, 441, 161))
        self.processImgFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.processImgFrame.setText("")
        self.processImgFrame.setObjectName("processImgFrame")
        self.liveVidGB = QtWidgets.QGroupBox(self.centralwidget)
        self.liveVidGB.setGeometry(QtCore.QRect(10, 10, 711, 541))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        self.liveVidGB.setFont(font)
        self.liveVidGB.setStyleSheet("border-style: solid;\n"
        "border-width: 1px;")
        self.liveVidGB.setObjectName("liveVidGB")
        self.liveVidFrame = QtWidgets.QLabel(self.liveVidGB)
        self.liveVidFrame.setGeometry(QtCore.QRect(10, 20, 691, 511))
        self.liveVidFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.liveVidFrame.setText("")
        self.liveVidFrame.setObjectName("liveVidFrame")
        MainControllerUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainControllerUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1196, 21))
        self.menubar.setObjectName("menubar")
        MainControllerUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainControllerUI)
        self.statusbar.setObjectName("statusbar")
        MainControllerUI.setStatusBar(self.statusbar)

        self.retranslateUi(MainControllerUI)
        QtCore.QMetaObject.connectSlotsByName(MainControllerUI)

        if Ui_MainControllerUI.state:
            self.sttLbl.setText('Open')
        else:
            self.sttLbl.setText('Close')

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_data)
        # self.timer.start(300)
        
        # Initialize callbacks and events
        ## For Screens
        self.teachingCamBtn.clicked.connect(self.openCamTeaching)
        self.configBtn.clicked.connect(self.openCongiguration)
        ## End Screens
        # End initialize callbacks and events
        self.armHomeBtn.clicked.connect(self.homeArmSend)
        self.camHomeBtn.clicked.connect(self.read_data)
        self.armTestingBtn.clicked.connect(self.enableCam)
        self.manualBtn.clicked.connect(self.manualMode)
        self.autoBtn.clicked.connect(self.autoMode)
        self.camHomeBtn.clicked.connect(self.CamHoming)
        
    def retranslateUi(self, MainControllerUI):
        _translate = QtCore.QCoreApplication.translate
        MainControllerUI.setWindowTitle(_translate("MainControllerUI", "Main Controller-MC"))
        self.statusGB.setTitle(_translate("MainControllerUI", "Status"))
        self.connectionLbl.setText(_translate("MainControllerUI", "Connection: UART"))
        self.label_2.setText(_translate("MainControllerUI", "Status:"))
        self.sttLbl.setText(_translate("MainControllerUI", "Disconnect"))
        self.configBtn.setText(_translate("MainControllerUI", "Configuration "))
        self.calibGB.setTitle(_translate("MainControllerUI", "Calibration"))
        self.armHomeBtn.setText(_translate("MainControllerUI", "Arm Homing "))
        self.camHomeBtn.setText(_translate("MainControllerUI", "Cam Homing "))
        self.teachingCamBtn.setText(_translate("MainControllerUI", "Cam teaching "))
        self.armTestingBtn.setText(_translate("MainControllerUI", "Live View"))
        self.armPosGB.setTitle(_translate("MainControllerUI", "Arm Position"))
        self.label.setText(_translate("MainControllerUI", "X Position:"))
        self.label_3.setText(_translate("MainControllerUI", "Y Position:"))
        self.label_4.setText(_translate("MainControllerUI", "Z Position:"))
        self.proPosGB.setTitle(_translate("MainControllerUI", "Product Position"))
        self.label_5.setText(_translate("MainControllerUI", "X Position:"))
        self.label_6.setText(_translate("MainControllerUI", "Y Position:"))
        self.xProLbl.setText(_translate("MainControllerUI", "TextLabel"))
        self.yProLbl.setText(_translate("MainControllerUI", "TextLabel"))
        self.controlGB.setTitle(_translate("MainControllerUI", "Control"))
        self.autoBtn.setText(_translate("MainControllerUI", "Auto"))
        self.manualBtn.setText(_translate("MainControllerUI", "Manual"))
        self.processGB.setTitle(_translate("MainControllerUI", "Process"))
        self.liveVidGB.setTitle(_translate("MainControllerUI", "Live Cam"))


    ########################################################################################
    #                                                                                      #
    # Custom event: state change -> read the state of application to dynamically change UI #
    #                                                                                      #
    ########################################################################################
    # Set State -> set new state
    def SetState(self, value):
        self.oldState = self.state
        self.state = value
        self.myEvent = threading.Thread(target=self.StateChange)
        self.myEvent.start()
        self.event.set()
    # State change
    def StateChange(self):
        self.event.wait()
        if self.oldState is not self.state:
            self.Update_UI()
        else:
            pass
        self.event.clear()

    # Update UI
    def Update_UI(self):
        if self.state:
            self.sttLbl.setText('Open')
            self.sttLbl.setStyleSheet("border-style: none; color: green; font-weight: 400")
            # for debugging
            temp = 'connected \n'
            # temp_numb = [1, 2, 3]
            # temp_numb_bytes = bytearray(temp_numb)
            temp_bytes = bytes(temp, encoding='utf-8')
            # tmp = array.array('B', [0x00, 0x01, 0x02]).tostring()
            # self.ser.write(tmp)
            # self.ser.write(temp_bytes)
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': UART Connected.' + ' Port name: ' + self.ser.port)
        else:
            self.sttLbl.setText('Close')
            self.sttLbl.setStyleSheet("border-style: none; color: red; font-weight: 400")
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': UART Connection Closed.')

    ########################################################################################
    #                                                                                      #
    # Cam Teaching Window                                                                  #
    #                                                                                      #
    ########################################################################################

    '''Open main window( cam teaching window)'''
    def openCamTeaching(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    ########################################################################################
    #                                                                                      #
    # Configuraion Window UI and its callback                                              #
    #                                                                                      #
    ########################################################################################

    '''Custom close event ***very important '''
    def closeEvent(self, *arg):
        self.ser = Ui_ConfigurationUI.ser
        self.mode = Ui_ConfigurationUI.mode - 1
        self.SetState(Ui_ConfigurationUI.state)
           
    ''' Open Configuration Ui '''
    def openCongiguration(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ConfigurationUI()
        self.ui.setupUi(self.window)
        self.window.closeEvent = self.closeEvent
        self.window.show()

    ''' Arm homing button '''
    def homeArmSend(self):
        if self.state == False:
            message = 'Error Connection. Please check ports.'
            title = 'Error'
            self.createMessageBox(message, title, 'error')
            logging.basicConfig(filename=self.FILE_LOG, level=logging.ERROR)
            t_log = GetTime()
            logging.error(t_log + ': Error connection.')
        else: 
            self.stateProcess = False
            message = b"h00000000000000000000"
            # byteMessage = bytes(message, encoding='utf-8')
            self.ser.write(message)
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': Arm Homing.')
    ########################################################################################
    #                                                                                      #
    # Create Message box                                                                   #
    #                                                                                      #
    ########################################################################################

    def createMessageBox(self, message, title, style):
        msg = QtWidgets.QMessageBox()
        if style == 'infor':
            msg.setIcon(QtWidgets.QMessageBox.Information)
        elif style == 'error':
            msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setMinimumSize(QtCore.QSize(300, 200))
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()

    def read_data(self):
        if self.state == True:
            buf = self.ser.read(self.ser.inWaiting())
            message = buf.decode('utf-8')
        else:
            buf = 0
            message = ''
        if message != '':
            print(message)
            command = message
            if command == 'c':
                print('in c')
                index = str(self.currentDestination)
                nextPoints = self.positionDictionary[index]
                nextX, nextY, nextAngle = nextPoints[0], nextPoints[1], nextPoints[2]
                if self.currentDestination < 6:
                    self.currentDestination += 1
                else:
                    self.currentDestination = 1
                print(self.currentDestination) 
                mess = UARTMessage(nextX, nextY, nextAngle, 'r')
                mess_bytes = bytes(mess, encoding='utf-8')
                
                self.ser.write(mess_bytes)
                
            elif command == 'r':
                print('in r')
                logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
                t_log = GetTime()
                logging.info(t_log + ': Object number ' + str(self.objectCounting) + ' done.')
                self.stateProcess = False
                self.count = 0
                self.sumX = 0
                self.sumY = 0
                self.sumAngle = 0
                self.timer.stop()
                
            else:
                print('in nothing')
                self.stateProcess = True
        else:
            pass
        self.timer.setInterval(600)
        # return buf

    ########################################################################################
    #                                                                                      #
    # For camera displaying                                                                #
    #                                                                                      #
    ########################################################################################
    def enableCam(self):
        self.stateLiveView = not self.stateLiveView
        if self.stateLiveView == True:
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': Live View Enabled.')
            self.armTestingBtn.setStyleSheet("background-color: rgb(0, 255, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
            # self.camera.initialize()
            self.updateTimer = QtCore.QTimer()
            self.updateTimer.timeout.connect(self.update_Image)
            self.updateTimer.start(1)
            
        else:
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': Live View Disabled.')
            self.armTestingBtn.setStyleSheet("background-color: rgb(255, 255, 0);\n"
            "border-style: outset;\n"
            "border-width: 1px;\n"
            "border-radius: 4px;\n"
            "border-color: black;")
            # self.camera.close_camera()
            self.updateTimer.stop()
        
    def update_Image(self):
        try:
            frame, cx, cy, angle = self.od.Process(self.mode)
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
            qPixMap = QtGui.QPixmap(qImg)
            qPixMap = qPixMap.scaled(self.liveVidFrame.width(), self.liveVidFrame.height(),QtCore.Qt.KeepAspectRatio)
            self.liveVidFrame.setPixmap(qPixMap)
            
            points = np.array([[cx, cy, 1]]).T
            realPoints = ImgPoints2RealPoints(self.mtx, self.rodrigues_Vecs, self.tvects, points, self.s)
            _x, _y = realPoints.item(0), realPoints.item(1)
            # print(_x, _y)
            _angle = angle * 180.0 / 3.14159
            pointX = _x * 2.45 - 35
            pointY = _y * 2.45 + 0.1
            self.xProLbl.setText(str(pointX))
            self.yProLbl.setText(str(pointY))
            # print(_angle)
            self.sumX += pointX
            self.sumY += pointY
            self.sumAngle += _angle
            self.count += 1
            
            if self.state == True and self.stateProcess == False and self.count == 10:
                print('---------------------')
                self.count = 0
                aveA = self.sumAngle / 10.0
                # + 0.2 * math.cos(aveA * 3.14159 / 180.0)
                aveX = self.sumX / 10.0 
                aveY = self.sumY / 10.0
                
                self.sumX = 0
                self.sumY = 0
                self.sumAngle = 0
                self.stateProcess = True
                self.objectCounting += 1
                logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
                t_log = GetTime()
                logging.info(t_log + ': ' + 'Object number ' + str(self.objectCounting) + ' in progress.')
                message = UARTMessage(aveX, aveY, aveA, 'c')
                message_bytes = bytes(message, encoding='utf-8')
                self.ser.write(message_bytes)
                self.timer.start(600)
                # self.myTimer.start(8000)
            self.updateTimer.setInterval(4)

        except:
            
            frame = self.od.Get_Frame()
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
            qPixMap = QtGui.QPixmap(qImg)
            qPixMap = qPixMap.scaled(self.liveVidFrame.width(), self.liveVidFrame.height(),QtCore.Qt.KeepAspectRatio)
            self.liveVidFrame.setPixmap(qPixMap)
            self.updateTimer.setInterval(4)


    ########################################################################################
    #                                                                                      #
    # Manual Mode                                                                          #
    #                                                                                      #
    ########################################################################################
    def manualMode(self):
        logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
        t_log = GetTime()
        logging.info(t_log + ': Enter manual Mode.')
        if self.state == False:
            message = 'Error Connection. Please check ports.'
            title = 'Error'
            self.createMessageBox(message, title, 'error')
            logging.basicConfig(filename=self.FILE_LOG, level=logging.ERROR)
            t_log = GetTime()
            logging.error(t_log + ': Error connection.')
        else: 
            # message = b"m"
            # # byteMessage = bytes(message, encoding='utf-8')
            # self.ser.write(message)
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': Enter Manual Mode successful.')
            self.widget = QtWidgets.QWidget()
            self.ui = Ui_ManualMode(self.ser, self.FILE_LOG)
            self.ui.setupUi(self.widget)
            self.widget.closeEvent = self.closeManualMode
            self.widget.show()
    def closeManualMode(self, *args):
        logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
        t_log = GetTime()
        logging.info(t_log + ': Exit manual Mode.')

    ########################################################################################
    #                                                                                      #
    # Auto Mode                                                                            #
    #                                                                                      #
    ########################################################################################
    def autoMode(self):
        self.stateAutoMode = not self.stateAutoMode
        if self.stateAutoMode == True:
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': Enter auto Mode.')
            if self.state == False:
                message = 'Error Connection. Please check ports.'
                title = 'Error'
                self.createMessageBox(message, title, 'error')
                logging.basicConfig(filename=self.FILE_LOG, level=logging.ERROR)
                t_log = GetTime()
                logging.error(t_log + ': Error connection.')
                self.stateAutoMode = False
            else: 
                logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
                t_log = GetTime()
                logging.info(t_log + ': Enter Auto Mode successful.')
                self.createMessageBox('Camera Auto Enabled!', 'Information', 'infor')
                # self.ser.write(b'a\n')
                
                self.enableCam()
        else:
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': Exit auto Mode.')  

    ########################################################################################
    #                                                                                      #
    # Camera Homing                                                                        #
    #                                                                                      #
    ########################################################################################
    def CamHoming(self):
        self.stateHoming = not self.stateHoming
        if self.stateHoming == True:
            # for homing
            
            self.updateTimerHoming = QtCore.QTimer()
            self.updateTimerHoming.timeout.connect(self.ImageForHoming)
            self.updateTimerHoming.start(1)
            
        else:
            path = 'Samples'
            for i in range(0, 15):
                last_frame = self.od.Get_Frame()
                cv2.imwrite(os.path.join(path, 'frame' + str(i) + '.jpg'), last_frame)
            self.GetHome()
            self.updateTimerHoming.stop()

    def ImageForHoming(self):
        frame = self.od.Get_Frame()
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
        qPixMap = QtGui.QPixmap(qImg)
        qPixMap = qPixMap.scaled(self.liveVidFrame.width(), self.liveVidFrame.height(),QtCore.Qt.KeepAspectRatio)
        self.liveVidFrame.setPixmap(qPixMap)
        self.updateTimerHoming.setInterval(3)   
    
    def GetHome(self):
        GetCalibrationParams()
        # UsingParams(np.array([[183, 285, 1]]).T)

    def SendDestination(self):
        index = str(self.currentDestination)
        nextPoints = self.positionDictionary[index]
        nextX, nextY, nextAngle = nextPoints[0], nextPoints[1], nextPoints[2]
        if self.currentDestination < 6:
            self.currentDestination += 1
        else:
            self.currentDestination = 1 
        mess = UARTMessage(nextX, nextY, nextAngle, 'r')
        mess_bytes = bytes(mess, encoding='utf-8')
        self.ser.write(mess_bytes)
        self.runAgain.start(8000)
        self.myTimer.stop()

    def RunAgain(self):
        self.stateProcess = False
        self.count = 0
        self.sumX = 0
        self.sumY = 0
        self.sumAngle = 0
        self.runAgain.stop()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainControllerUI = QtWidgets.QMainWindow()
    ui = Ui_MainControllerUI()
    ui.setupUi(MainControllerUI)
    MainControllerUI.show()
    
    sys.exit(app.exec_())

