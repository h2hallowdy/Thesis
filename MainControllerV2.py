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
import serial.tools.list_ports
import array
import logging
import cv2
import os
from datetime import datetime
from ObjectDetection import ObjectDetection
from Camera import Camera
from Calibration import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import random
import xlsxwriter
#endregion

class Ui_MainControllerUI(object):

    stateCollect = False
    state = False
    event = threading.Event()
    stateLiveView = False
    stateAutoMode = False
    stateProcess = False
    stateHoming = False
    stateProduct2 = False
    mode = 0
    # running = threading.Event()
    # running.set()
    ser = serial.Serial()
    # ser = serial.Serial()
    ser.port = "COM11"
    ser.baudrate = 115200
    ser.bytesize = 8
    ser.parity = serial.PARITY_NONE
    ser.rtscts = False
    

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
            '1': [15, 15, 90],
            '2': [20, 15, 90],
            '3': [25, 15, 90],
            '4': [15, 15, 90],
            '5': [20, 15, 90],
            '6': [25, 15, 90],
        }
        self.positionErasor = {
            '1': [15, 25, 90],
            '2': [20, 25, 90],
            '3': [25, 25, 90],
            '4': [15, 25, 90],
            '5': [20, 25, 90],
            '6': [25, 25, 90],
        }
        self.positionDictionaryBC = {
            '1': [0, 40, 90, 1],
            '2': [0, 40, 90, 3],
            '3': [0, 40, 90, 4.5],
            '4': [0, 40, 90, 1],
            '5': [0, 40, 90, 3],
            '6': [0, 40, 90, 4.5]
        }
        self.positionDictionaryBCErasor = {
            '1': [10, 35, 90, 1],
            '2': [10, 35, 90, 3],
            '3': [10, 35, 90, 4.5],
            '4': [10, 35, 90, 1],
            '5': [10, 35, 90, 3],
            '6': [10, 35, 90, 4.5]
        }
        self.objectCounting = 0
        self.currentDestination = 1
        self.currentDestinationErasor = 1
        self.myTimer = QtCore.QTimer()
        self.myTimer.timeout.connect(self.SendDestination)
        self.runAgain = QtCore.QTimer()
        self.runAgain.timeout.connect(self.RunAgain)
        # for Excel
        self.workbook = xlsxwriter.Workbook('laplai.xlsx') 
        self.worksheet = self.workbook.add_worksheet() 
        #Hoang's worksheet
        self.worksheetAngle = self.workbook.add_worksheet()
        self.row = 0
        self.col = 0
        self.rowAngle = 0
        self.colAngle = 0
        self.countForTest=0
        self.testState=False
        self.velocity = 0
        self.checkVec = 0
        try:
            self.ser.open()
            
            self.state = True
            print(self.ser)
            print(self.mode)

        except:
            print('cannot find any connection')
        try:
            #region: Load M, R, T, corners for Mode 1
            with np.load('B.npz') as X:
                self.mtx, self.dist, self.rvects, self.tvects, self.corners, self.tvec1, self.rvec1, self.s, self.newcameramtx = [X[i] for i in ('mtx','dist','rvecs','tvecs', 'corners','tvec1','rvec1', 's', 'newcameramtx')]
           
            self.rodrigues_Vecs = InverseRodrigues(self.rvec1)
            point = np.array([[214, 235, 1]], dtype=np.float32).T
            realWorldPoints = ImgPoints2RealPoints(self.newcameramtx, self.rodrigues_Vecs, self.tvec1, point, self.s)
            print(realWorldPoints)
            #endregion

            #region: Load M, R, T, corners for Mode 2
            with np.load('Calib_bc.npz') as P:
                self.mtx_BC, self.dist_BC, self.rvects_BC, self.tvects_BC, self.corners_BC, self.tvec1_BC, self.rvec1_BC, self.s_BC, self.newcameramtx_BC = [P[i] for i in ('mtx','dist','rvecs','tvecs', 'corners', 'tvec1', 'rvec1', 's', 'newcameramtx')]

            self.rodrigues_Vecs_BC = InverseRodrigues(self.rvec1_BC)
            # translate_BC = np.reshape(self.tvects_BC, (3, 1))
            # K_bc = np.concatenate((self.rodrigues_Vecs_BC, translate_BC), axis=1)
            # a_bc = self.mtx_BC.dot(K_bc).dot(np.array([[1, 1, 1, 1]]).T)
            # self.s_BC = a_bc.item(2)
            point = np.array([[216, 237, 1]], dtype=np.float32).T
            realWorldPoints = ImgPoints2RealPoints(self.newcameramtx_BC, self.rodrigues_Vecs_BC, self.tvec1_BC, point, self.s_BC)
            print(realWorldPoints)
            #endregion

            #region: Load M, R, T, corners for Mode 2
            with np.load('Calib_test.npz') as T:
                self.mtx_T, self.dist_T, self.rvects_T, self.tvects_T, self.corners_T = [T[i] for i in ('mtx','dist','rvecs','tvecs', 'corners')]

            self.rodrigues_Vecs_T = InverseRodrigues(self.rvects_T)
            translate_T = np.reshape(self.tvects_T, (3, 1))
            K_Te = np.concatenate((self.rodrigues_Vecs_T, translate_T), axis=1)
            a_T = self.mtx_T.dot(K_Te).dot(np.array([[1, 1, 1, 1]]).T)
            self.s_T = a_T.item(2)
            #endregion
            
        except Exception as e:
            print(e)

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
        self.liveVidFrame.setGeometry(QtCore.QRect(10, 20, 760, 480))
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
        self.manualBtn = QtWidgets.QPushButton(self.controlGB)
        self.manualBtn.setGeometry(QtCore.QRect(160, 20, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Material-Design-Iconic-Font")
        font.setPointSize(10)
        self.manualBtn.setFont(font)
        self.manualBtn.setStyleSheet("background-color: rgb(255, 85, 0);\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 4px;\n"
        "border-color: black;\n"
        "")
        self.manualBtn.setObjectName("manualBtn")
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

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim([-40, 10])
        self.ax.set_ylim([-10,50])
        self.canvas = FigureCanvas(self.figure)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(9, 20, 9, 9)
        # self.vbox = QtWidgets.QVBoxLayout()
        # self.canvas = Canvas(self.vbox, width=8, height=8, dpi=100)
        
        # self.vbox.addWidget(self.canvas)
        self.processGB.setLayout(layout)
        # self.plot()
        self.retranslateUi(MainControllerUI)

        if self.state:
            self.sttLbl.setText('Open')
        else:
            self.sttLbl.setText('Close')

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_data)
        self.timer.start(600)
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
        self.modeSlider.valueChanged.connect(self.OnValueChange)
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
        self.armTestingBtn.setText(_translate("MainControllerUI", "Live View"))
        self.controlGB.setTitle(_translate("MainControllerUI", "Control"))
        self.autoBtn.setText(_translate("MainControllerUI", "Auto"))
        self.manualBtn.setText(_translate("MainControllerUI", "Manual"))
        self.label_7.setText(_translate("MainControllerUI", "Mode"))
        self.processGB.setTitle(_translate("MainControllerUI", "Process"))

    ########################################################################################
    #                                                                                      #
    # Custom event: state change -> read the state of application to dynamically change UI #
    #                                                                                      #
    ########################################################################################
    # Set State -> set new state
    def SetState(self, value):
        print(self.state)
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
    # TODO: REMEMBER TO CHANGE THOSE CODE IN ORDER IF NEEDED
    def openCamTeaching(self):
        # self.window = QtWidgets.QMainWindow()
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self.window)
        # self.window.show()
        print('In Test')
        if self.state == False:
            message = 'Error Connection. Please check ports.'
            title = 'Error'
            self.createMessageBox(message, title, 'error')
            logging.basicConfig(filename=self.FILE_LOG, level=logging.ERROR)
            t_log = GetTime()
            logging.error(t_log + ': Error connection.')
        else:
            self.testState = True
            self.countForTest += 1 
            message = b"l00000000000000000000"
            # byteMessage = bytes(message, encoding='utf-8')
            self.ser.write(message)
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': Arm testing.')

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
        print(self.mode)
           
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
            self.count = 0
            self.sumX = 0
            self.sumY = 0
            self.sumAngle = 0
            self.currentDestination = 1
            self.countForTest = 0
            self.testState = False
            message = b"h00000000000000000000"
            # byteMessage = bytes(message, encoding='utf-8')
            self.ser.write(message)
            logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
            t_log = GetTime()
            logging.info(t_log + ': Arm Homing.')
            # time.sleep(30)
            # md = b"m10000000000000000000"
            # self.ser.write(md)
            
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
                print(self.stateProduct2)
                if self.stateProduct2 == False:
                    index = str(self.currentDestination)
                else:
                    index = str(self.currentDestinationErasor)
                print(index)
                if self.mode == 0:
                    if self.stateProduct2 == False:
                        nextPoints = self.positionDictionary[index]
                    else:
                        nextPoints = self.positionErasor[index]
                elif self.mode == 1:
                    if self.stateProduct2 == False:
                        nextPoints = self.positionDictionaryBC[index]
                    else:
                        nextPoints = self.positionDictionaryBCErasor[index]
                   
                nextX, nextY, nextAngle = nextPoints[0], nextPoints[1], nextPoints[2]
                if self.currentDestination < 6:
                    if self.stateProduct2 == False:
                        self.currentDestination += 1
                if self.currentDestinationErasor < 6:
                    if self.stateProduct2 == True:
                        self.currentDestinationErasor += 1
                if self.currentDestination >= 6:
                    self.currentDestination = 1
                if self.currentDestinationErasor >= 6:
                    self.currentDestinationErasor = 1
                
                # Nho sua 2 mode thanh 3 va 8
                if self.mode == 0:
                    mess = UARTMessage(nextX, nextY, nextAngle, 'r', 0.7)
                    mess_bytes = bytes(mess, encoding='utf-8')
                elif self.mode == 1:
                    mess = UARTMessage(nextX, nextY, nextAngle, 'r', nextPoints[3])
                    mess_bytes = bytes(mess, encoding='utf-8')
                time.sleep(0.4)
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

            elif command == 'h':
                print('homing done')
                if self.mode == 1:
                    md = b"m1-000000000000000000"
                    
                    time.sleep(0.4)
                    self.ser.write(md)
                else:
                    md = b"m0-000000000000000000"
                    
                    time.sleep(0.4)
                    self.ser.write(md)
                    try:
                        (pointX, pointY) = self.CheckPositionArm()
                        self.WriteToExcel(self.worksheet,self.row, self.col, pointX, pointY)
                        self.plot(pointX, pointY, 'CAM')
                    except:
                        print('Error Occured')
                    
            elif 'x' in command:
                if self.mode == 1:
                    pass
                else:
                    try:
                        data = command.split('x')[1]
                        decX, decY = int(data[0:2]), int(data[4:6])
                        pX, pY = int(data[2:4]), int(data[6:8])
                        X = -(decX + float(pX) / 100.0)
                        Y = decY + float(pY) / 100.0
                        self.WriteToExcel(self.worksheet,self.row, self.col + 4, X, Y)
                        self.row += 1
                        self.col = 0
                        self.plot(X, Y, 'ARM')
                    except: 
                        print('Error in write data')
                    try:
                        (pointX, pointY) = self.CheckPositionArm()
                        self.WriteToExcel(self.worksheet,self.row, self.col, pointX, pointY)
                        self.plot(pointX, pointY, 'CAM')
                    except:
                        print('Not camera')
                    if self.countForTest < 20 and self.testState == True:
                        time.sleep(1)
                        self.openCamTeaching()
            else:
                print('in nothing')
                print(command)
                # self.stateProcess = True
        else:
            pass
        self.timer.setInterval(500)
        # return buf

    ########################################################################################
    #                                                                                      #
    # For camera displaying                                                                #
    #                                                                                      #
    ########################################################################################
    def enableCam(self):
        self.stateLiveView = not self.stateLiveView
        print(self.stateLiveView)
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
            # if self.stateProcess == False:
            frame, cx, cy, angle, productStyle = self.od.Process(self.mode)
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
            qPixMap = QtGui.QPixmap(qImg)
            qPixMap = qPixMap.scaled(self.liveVidFrame.width(), self.liveVidFrame.height(),QtCore.Qt.KeepAspectRatio)
            self.liveVidFrame.setPixmap(qPixMap)
            points = np.array([[cx, cy, 1]]).T
            _angle = angle * 180.0 / 3.14159
                
            # duoi dat
            if self.mode == 0:
                if productStyle == 'Battery':
                    self.stateProduct2 = False
                else:
                    self.stateProduct2 = True
                realPoints = ImgPoints2RealPoints(self.newcameramtx, self.rodrigues_Vecs, self.tvec1, points, self.s)
                _x, _y = realPoints.item(0), realPoints.item(1)
                pointX = _x * 2.45 - 28.8
                pointY = _y * 2.45 + 19
                print(pointX, pointY)
                self.sumX += pointX
                self.sumY += pointY
                self.sumAngle += _angle
                self.count += 1 
            # tren bang chuyen
            elif self.mode == 1:
                if productStyle == 'Battery':
                    self.stateProduct2 = False
                else:
                    self.stateProduct2 = True
                realPoints = ImgPoints2RealPoints(self.newcameramtx_BC, self.rodrigues_Vecs_BC, self.tvec1_BC, points, self.s_BC)
                _x, _y = realPoints.item(0), realPoints.item(1)
                pointX = _x * 2.45 - 31.5
                pointY = _y * 2.45 + 11.85
                # print(pointX, pointY, _angle)
                    
                self.sumX = pointX
                self.sumY = pointY
                self.sumAngle = _angle
                self.count = 10
            self.xProLbl.setText(str(pointX))
            self.yProLbl.setText(str(pointY))
            # print(_angle)
                
            if self.state == True and self.stateProcess == False and self.count == 10:
                print('---------------------')
                self.count = 0
                aveA = self.sumAngle / 10.0
                aveX = self.sumX / 10.0 
                aveY = self.sumY / 10.0
                    
                #region: update toa do sau xx seconds TODO: update for not using offsets
                # if self.mode == 1:
                #     aveX = aveX * 10.0 + 0.9
                #     aveY = aveY * 10.0 - 0.4 + (1.5465 + 0.25 + 0.275) * (25 / 5.675)
                #     # aveY = aveY * 10.0 - 0.4
                #     if aveY < 10:
                #         aveY += 1.3
                #         aveX += 1.3
                #     elif aveY >= 10 and aveY <= 22:
                #         aveY += 0.6
                #         aveX -= 0.6
                #     else:
                #         pass
                #     if aveA > -2.0 and aveA < 2.0:
                #         aveY -= 0.2
                #     aveA = aveA * 10.0
                #endregion
                if self.mode == 1:
                    aveX = aveX * 10.0
                    aveY = aveY * 10.0 + (1.5465 + 0.25 + 0.275) * (25 / 5.675)
                    
                    # aveY = aveY * 10.0 - 0.4
                    aveA = aveA * 10.0  
                print(aveX, aveY, aveA)
                self.WriteToExcel(self.worksheetAngle, self.rowAngle, self.colAngle, aveX, aveY)
                self.rowAngle += 1
                #region: Uncomment this if anything bad happend
                # if aveY <= 25.0:
                #     aveY += 0.4
                # else:
                #     aveY += 0.2
                #endregion
                self.sumX = 0
                self.sumY = 0
                self.sumAngle = 0
                self.stateProcess = True
                self.objectCounting += 1
                logging.basicConfig(filename=self.FILE_LOG, level=logging.INFO)
                t_log = GetTime()
                logging.info(t_log + ': ' + 'Object number ' + str(self.objectCounting) + ' in progress.')

                if self.mode == 0:
                    message = UARTMessage(aveX, aveY, aveA, 'c', 3)
                    message_bytes = bytes(message, encoding='utf-8')
                elif self.mode == 1:
                    message = UARTMessage(aveX, aveY, aveA, 'c', 8.5)
                    message_bytes = bytes(message, encoding='utf-8')
                self.ser.write(message_bytes)
            

        except Exception as e:
            print(e)
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
                self.enableCam()
        else:
            self.enableCam()
            self.createMessageBox('Camera Auto Disabled!', 'Information', 'infor')
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

    def plot(self, x, y, title):
        ''' plot some random stuff '''
        # random data
        # data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        # self.figure.clear()

        # create an axis
        
        

        # discards the old graph
        # ax.hold(False) # deprecated, see above
        if title == 'ARM':
        # plot data
            self.ax.plot(x, y, 'bx')
        elif title == 'CAM':
            self.ax.plot(x, y, 'r*')
        # refresh canvas
        self.canvas.draw()

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

    # TODO: There is a close function for Excel file right here
    def OnValueChange(self, value):
        self.mode = value
        if self.mode == 1:
            self.workbook.close()
        print('Now in mode ' + str(self.mode))
        

    def CheckPositionArm(self):
        frame = self.od.Get_Frame()
        frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)     # Converting RGB system to HSV system.
        hand_lower = np.array([105,193,104])                         
        hand_upper = np.array([245,253,255])
        mask = cv2.inRange(frame_hsv,hand_lower,hand_upper)
        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = max(contours, key = cv2.contourArea)
        rectAngle = cv2.minAreaRect(c)
        tam = rectAngle[0]
        a = np.array([[tam[0], tam[1], 1]]).T
        realCenter = ImgPoints2RealPoints(self.mtx_T, self.rodrigues_Vecs_T, self.tvects_T, a, self.s_T)
        _x, _y = realCenter.item(0), realCenter.item(1)
        pointX = _x * 2.45 - 30.57
        pointY = _y * 2.45 + 24
        cv2.imshow('ABC', mask)
        print(pointX, pointY)
        return (pointX, pointY)
    
    def WriteToExcel(self, worksheet, row, col, data1, data2):
        
        worksheet.write(row, col, data1)
        worksheet.write(row, col + 1, data2)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainControllerUI = QtWidgets.QMainWindow()
    ui = Ui_MainControllerUI()
    ui.setupUi(MainControllerUI)
    MainControllerUI.show()
    sys.exit(app.exec_())

