# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\setup files\NVIDIA\GUI\main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import os
import glob
import math
from PIL import Image, ImageTk
from xml_util import createXMLAnnotation
from PyQt5 import QtCore, QtGui, QtWidgets


def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(711, 416)

        # Initialize global
        self.imageDir = ''
        self.imageList = []
        self.outDir = ''
        self.xmlDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagepath = ''
        self.imagename = ''
        self.labelfilename = ''
        self.xmlfilename = ''
        self.tkimg = None
        self.numbers = False
        self.boxcount = 0
        self.pixmap = None

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = 0
        self.bboxList = []
        self.bboxNumberList = []
        self.hl = None
        self.vl = None

        # initialize states
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['itemClick'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0
        self.itemSelected = None
        self.qItemSelected = None
        

        # Initialize main windows
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label.setObjectName("label")
        self.imgDir = QtWidgets.QLineEdit(self.centralwidget)
        self.imgDir.setGeometry(QtCore.QRect(70, 10, 481, 20))
        self.imgDir.setObjectName("imgDir")
        self.loadBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loadBtn.setGeometry(QtCore.QRect(570, 10, 131, 23))
        self.loadBtn.setObjectName("loadBtn")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(600, 50, 81, 16))
        self.label_2.setObjectName("label_2")
        self.listBBox = QtWidgets.QListView(self.centralwidget)
        self.listBBox.setGeometry(QtCore.QRect(570, 70, 131, 192))
        self.listBBox.setObjectName("listBBox")
        self.delBtn = QtWidgets.QPushButton(self.centralwidget)
        self.delBtn.setGeometry(QtCore.QRect(570, 270, 131, 23))
        self.delBtn.setObjectName("delBtn")
        self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
        self.clearBtn.setGeometry(QtCore.QRect(570, 300, 131, 23))
        self.clearBtn.setObjectName("clearBtn")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.label_3.setObjectName("label_3")
        self.prevBtn = QtWidgets.QPushButton(self.centralwidget)
        self.prevBtn.setGeometry(QtCore.QRect(160, 340, 75, 23))
        self.prevBtn.setObjectName("prevBtn")
        self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nextBtn.setGeometry(QtCore.QRect(260, 340, 75, 23))
        self.nextBtn.setObjectName("nextBtn")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(380, 340, 47, 13))
        self.label_4.setObjectName("label_4")
        self.currValue = QtWidgets.QLabel(self.centralwidget)
        self.currValue.setGeometry(QtCore.QRect(430, 340, 47, 13))
        self.currValue.setText("")
        self.currValue.setObjectName("currValue")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(480, 340, 16, 16))
        self.label_5.setObjectName("label_5")
        self.totalValue = QtWidgets.QLabel(self.centralwidget)
        self.totalValue.setGeometry(QtCore.QRect(510, 340, 47, 13))
        self.totalValue.setText("")
        self.totalValue.setObjectName("totalValue")
        self.imgFrame = QtWidgets.QLabel(self.centralwidget)
        self.imgFrame.setGeometry(QtCore.QRect(70, 40, 481, 281))
        self.imgFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.imgFrame.setText("")
        self.imgFrame.setObjectName("imgFrame")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(380, 360, 61, 16))
        self.label_6.setObjectName("label_6")
        self.xVal = QtWidgets.QLabel(self.centralwidget)
        self.xVal.setGeometry(QtCore.QRect(460, 360, 47, 13))
        self.xVal.setText("")
        self.xVal.setObjectName("xVal")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(510, 360, 16, 16))
        self.label_8.setObjectName("label_8")
        self.yVal = QtWidgets.QLabel(self.centralwidget)
        self.yVal.setGeometry(QtCore.QRect(520, 360, 47, 13))
        self.yVal.setText("")
        self.yVal.setObjectName("yVal")
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(570, 330, 131, 23))
        self.startBtn.setObjectName("startBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 711, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Initialize callback
        self.loadBtn.clicked.connect(self.loadDir)
        self.prevBtn.clicked.connect(self.prevImage)
        self.nextBtn.clicked.connect(self.nextImage)
        self.delBtn.clicked.connect(self.delItem)
        self.clearBtn.clicked.connect(self.clearAll)
        self.listBBox.clicked.connect(self.itemSelect)
        self.imgFrame.mousePressEvent = self.mouseClick
        self.imgFrame.mouseMoveEvent = self.mouseMove

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "ImageDir"))
        self.loadBtn.setText(_translate("MainWindow", "Load"))
        self.label_2.setText(_translate("MainWindow", "Bounding Boxes"))
        self.delBtn.setText(_translate("MainWindow", "Delete"))
        self.clearBtn.setText(_translate("MainWindow", "Clear All"))
        self.label_3.setText(_translate("MainWindow", "Image"))
        self.prevBtn.setText(_translate("MainWindow", "<< Prev"))
        self.nextBtn.setText(_translate("MainWindow", "Next >>"))
        self.label_4.setText(_translate("MainWindow", "Progress"))
        self.label_5.setText(_translate("MainWindow", "/"))
        self.label_6.setText(_translate("MainWindow", "Coordinates"))
        self.label_8.setText(_translate("MainWindow", ","))
        self.startBtn.setText(_translate("MainWindow", "Start"))


    def loadDir(self):
        s = self.imgDir.text()
        self.category = int(s)
        self.imageDir = os.path.join(r'./Images', '%03d' % (self.category))
        # dirs = os.listdir(self.imageDir)
        # for file in dirs:
        #     print(file)
        extensions = ("*.jpg", "*.jpeg", "*.JPG", "*.JPEG")
        for extension in extensions:
            self.imageList.extend(
                glob.glob(os.path.join(self.imageDir, extension)))
            self.imageList = Remove(self.imageList)
        if len(self.imageList) == 0:
            print('No .JPEG images found in the specified dir!')
            return
        # for debugging
        # print('We have found', '%d' %(len(self.imageList)), 'images')
        # for image in self.imageList:
        #     print(image)

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

        # set up output dir
        self.outDir = os.path.join(r'./Labels', '%03d' % (self.category))
        self.xmlDir = os.path.join(
            r'./AnnotationsXML', '%03d' % (self.category))
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        if not os.path.exists(self.xmlDir):
            os.mkdir(self.xmlDir)

        self.loadImage()

    # Load Image
    def loadImage(self):
        self.imagepath = self.imageList[self.cur - 1]
        # Setup pixmap with the provided image
        self.pixmap = QtGui.QPixmap(self.imagepath)
        self.pixmap = self.pixmap.scaled(self.imgFrame.width(), self.imgFrame.height(
        ), QtCore.Qt.KeepAspectRatio)  # Scale pixmap
        self.imgFrame.setPixmap(self.pixmap)  # Set the pixmap onto the label
        # Align the label to center
        self.imgFrame.setAlignment(QtCore.Qt.AlignCenter)
        # Current / Total
        self.currValue.setText(str(self.cur))
        self.totalValue.setText(str(self.total))

        # load labels
        self.clearAll()
        self.imagename = os.path.split(self.imagepath)[-1].split('.')[0]
        labelname = self.imagename + '.txt'
        xmlname = self.imagename + '.xml'
        self.labelfilename = os.path.join(self.outDir, labelname)
        self.xmlfilename = os.path.join(self.xmlDir, xmlname)

    # Save Annotations
    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write('%d\n' %len(self.bboxList))
            for bbox in self.bboxList:
                f.write(' '.join(map(str, bbox)) + '\n')
        im = Image.open(self.imagepath)
        # for debugging
        # print(im.size)
        createXMLAnnotation(os.path.split(self.imagepath)[-1], self.bboxList, im.size, self.xmlfilename)
        print('Image No. %d saved' %(self.cur))
        
    # Prev button
    def prevImage(self):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    # Next Button
    def nextImage(self):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    # Clear button
    def clearAll(self):
        self.bboxList = []
        model = QtGui.QStandardItemModel().clear()
        self.listBBox.setModel(model)

    # Delete button -> Still need to re-render the list
    def delItem(self):
        if self.STATE['itemClick'] == 1:
            # row = self.bboxList[self.itemSelected]
            
            # model = QtGui.QStandardItemModel().removeRow()
            # # self.listBBox.setModel(model)
            self.bboxIdList.pop(self.itemSelected)
            self.bboxList.pop(self.itemSelected)
            print(self.bboxIdList, self.bboxList)
            
    # List View Selection
    def itemSelect(self, qindex):
        # for debugging
        # print(qindex.row())
        self.STATE['itemClick'] = 1
        self.qItemSelected = qindex
        self.itemSelected = qindex.row()
        print(self.itemSelected)

    # Mouse click event
    def mouseClick(self, event):
        xq = event.pos().x()
        yq = event.pos().y()
        x = int(xq)
        y = int(yq)
        if self.STATE['click'] == 0:
            self.STATE['x'], self.STATE['y'] = x, y
        else:
            x1, x2 = min(self.STATE['x'], x), max(self.STATE['x'], x)
            y1, y2 = min(self.STATE['y'], y), max(self.STATE['y'], y)


            # Drawing function
            self.painterInstance = QtGui.QPainter(self.pixmap)        
            self.penRectangle = QtGui.QPen(QtCore.Qt.red)
            self.penRectangle.setWidth(3)
            self.painterInstance.setPen(self.penRectangle)
            xlen = abs(x1 - x2)
            ylen = abs(y1 - y2)
            self.painterInstance.drawRect(x1, y1, xlen, ylen)
            self.imgFrame.setPixmap(self.pixmap)
            self.imgFrame.show()
            # for debugging
            # print(x1, y1)
            # print(x2, y2)
            self.bboxList.append((x1, y1, x2, y2))
            self.bboxIdList.append(self.bboxId)
            self.bboxId = self.bboxId + 1
            
            # print(self.bboxIdList, self.bboxId)
            self.boxcount = self.boxcount + 1
            self.render()
            

        self.STATE['click'] = 1 - self.STATE['click']
        # for debugging
        # print('STATE NOW:', str(self.STATE['click']))

    # Mouse move event
    def mouseMove(self, event):
        xq = event.pos().x()
        yq = event.pos().y()
        x = int(xq)
        y = int(yq)
        self.xVal.setText(str(x))
        self.yVal.setText(str(y))
        
    # Render function
    def render(self):
        model = QtGui.QStandardItemModel()
        if (len(self.bboxList) != 0):
            self.listBBox.setModel(model)
            for val in self.bboxList:
                item = QtGui.QStandardItem(str(val))
                model.appendRow(item)

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
