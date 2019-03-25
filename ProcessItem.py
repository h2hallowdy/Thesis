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
            crop = img[startY - self.error : endY + self.error, startX - self.error : endX + self.error]
            cropGray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            equ = cv2.equalizeHist(cropGray)
            blur = cv2.GaussianBlur(equ, (5, 5), 0)
            ret, thresh = cv2.threshold(blur, 102, 255, 0)
            myThresh = 255 - thresh
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            erosion = cv2.erode(myThresh, kernel, iterations=2)
            _, contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            c = max(contours, key = cv2.contourArea)
            rect = cv2.minAreaRect(c)
            return (crop, rect[2])
        else:
            return (None, None)



if __name__ == '__main__':
    rects = []
    rects.append((1, 2, 3, 4))
    rects.append((2, 2, 4, 5))

    pt = ProcessItem()
    objectSelected = pt.updateObject(rects)
    
    (x, y, z, t) = objectSelected
    print(t)

