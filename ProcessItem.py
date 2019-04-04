import cv2
from collections import OrderedDict
import numpy as np

class ProcessItem():
    def __init__(self, error=20):
        self.error = error
        self.angle = 0
        self.rects = []
        self.processObject = None
    
    def updateObject(self, rects):
        self.rects = rects
        if len(self.rects) == 0:
            self.processObject = None
        else:
            self.processObject = self.rects[0]
        return self.processObject
    
    def updateAngle(self, img):
        if self.processObject != None:
            # destructuring the object
            (startX, startY, endX, endY) = self.processObject
            temp_cx = (startX + endX) / 2.0
            temp_cy = (startY + endY) / 2.0
            # crop = img[startY - self.error : endY + self.error, startX - self.error : endX + self.error]
            crop = img[startY : endY, startX : endX]
            w, h = crop.shape[1], crop.shape[0]
            _new_cenX = w / 2.0
            _new_cenY = h / 2.0
            cropGray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            # equ = cv2.equalizeHist(cropGray)
            # blur = cv2.GaussianBlur(equ, (5, 5), 0)
            ret, thresh = cv2.threshold(cropGray, 102, 255, 0)
            myThresh = 255 - thresh
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            erosion = cv2.erode(myThresh, kernel, iterations=2)
            cv2.imshow('erosion', erosion)
            _, contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            c = max(contours, key = cv2.contourArea)
            rect = cv2.minAreaRect(c)
            _cx, _cy = rect[0]
            deltaX = _cx - _new_cenX
            deltaY = _cy - _new_cenY
            cx = temp_cx + deltaX
            cy = temp_cy + deltaY
            return (crop, rect[2], cx, cy)
        else:
            return (None, None)



if __name__ == '__main__':
    crop = cv2.imread('crop.jpg')
    cropGray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    # equ = cv2.equalizeHist(cropGray)
    # blur = cv2.GaussianBlur(equ, (5, 5), 0)
    ret, thresh = cv2.threshold(cropGray, 102, 255, 0)
    cv2.imshow('thresh', thresh)
    myThresh = 255 - thresh
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    erosion = cv2.erode(myThresh, kernel)
    cv2.imshow('erosion', erosion)
    _, contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv2.contourArea)
    cv2.waitKey(0)
    

