import cv2
from collections import OrderedDict
import numpy as np
import math

def first(s):
    '''Return the first element from an ordered collection
       or an arbitrary element from an unordered collection.
       Raise StopIteration if the collection is empty.
    '''
    return next(iter(s))

class ProcessErasor():
    def __init__(self, error=10):
        self.error = error
        self.rects = []
        self.processObject = None
    
    def updateObject(self, rects, listObjects):
        self.distance = []
        self.rects = rects
        self.listRects = listObjects
        firstItem = self.listRects[first(self.listRects)]
        if len(self.rects) == 0:
            self.processObject = None
        else:
            for rect in self.rects:
                (startX, startY, endX, endY) = rect   
                [temp_cx, temp_cy] = [(startX + endX) / 2.0, (startY + endY) / 2.0] 
                self.distance.append(self.calculation(firstItem, [temp_cx, temp_cy]))
            min_index = np.argmin(self.distance)
            self.processObject = self.rects[min_index]
        return self.processObject
    
    def updateAngle(self, img, mode):
        if self.processObject != None:
                
            #region: Normal IP to get real rectangle
            # destructuring the object
            (startX, startY, endX, endY) = self.processObject
            temp_cx = (startX + endX) / 2.0
            temp_cy = (startY + endY) / 2.0
            if mode == 0:
                crop = img[startY - self.error : endY + self.error, startX - self.error : endX + self.error]
            elif mode == 1:
                crop = img[startY - 2 : endY + 2, startX - 2 : endX + 2]
            # crop = img[startY : endY, startX : endX]
            w, h = crop.shape[1], crop.shape[0]
            _new_cenX = w / 2.0
            _new_cenY = h / 2.0

            if mode == 0:
                #region: Static product image processing
                cropGray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                # th = cv2.adaptiveThreshold(cropGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 2*175+1, 27)
                # myThresh = 255 - th
                # crossmini = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
                # myth = cv2.erode(myThresh, crossmini, iterations=1)
                bound = self.LowBlueFilter(crop)
                _, contours, _ = cv2.findContours(bound, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                c = max(contours, key = cv2.contourArea)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(cropGray, [box],0,(0,0,255),1)
                # cv2.imshow('dilation',cropGray)
                #endregion
            elif mode == 1:
                #region: On conveyor belt image processing
                cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
                crossmini = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
                elipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
                kernel = np.ones((5, 5), np.uint8)
                kernel2 = np.ones((3, 3), np.uint8)
                frame_hsv = cv2.cvtColor(crop,cv2.COLOR_BGR2HSV)

                #region: Mask1 => green 
                hand_lower = np.array([54,65,6])                         
                hand_upper = np.array([104,255,255])

                
                mask1 = cv2.inRange(frame_hsv,hand_lower,hand_upper) 
                #endregion

                #region: Compile 2 masks, negative and find res
                result = mask1
                neg_result = 255 -result

                super_result = cv2.erode(neg_result, kernel2, iterations=1)
                abc = cv2.dilate(super_result, kernel2, iterations=1)
                res = cv2.bitwise_and(crop, crop, mask = neg_result)
                #endregion

                #region: Same thing to find 4 points coordinates
                cropGray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
                _, contours, _ = cv2.findContours(abc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                c = max(contours, key = cv2.contourArea)
                for smallerC in contours:
                    if cv2.contourArea(smallerC) > 474 and cv2.contourArea(smallerC) < 560:
                        c1 = smallerC
                        (x, y), (w, h), _ = cv2.minAreaRect(c)
                        if h != 0:
                            if w > h:
                                ratio = w / h
                            elif h > w:
                                ratio = h / w
            
                            if ratio > 1.78 and ratio < 3.3:
                                c = smallerC
                                break
                
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                sax = crop.copy()
                cv2.drawContours(sax, [box],0,(0,0,255),1)
                cv2.imshow("Hahaha", sax)
                #endregion

                #endregion

            # cv2.drawContours(crop, [box],0,(0,0,255),1)
            #endregion

            cv2.imwrite('crop.jpg', crop)
            #region: Calculate direction of product
            cropAngle = self.LowBlueFilter(crop)
            kernel = np.ones((5, 5), np.uint8)
            f = cv2.erode(cropAngle, kernel, iterations=1)
            _, contoursAngle, _ = cv2.findContours(cropAngle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cAngle = max(contoursAngle, key = cv2.contourArea)
            rectAngle = cv2.minAreaRect(cAngle)
            tam = rectAngle[0]
            # print(tam)

            # cv2.imshow('cropAngle', cropAngle)
            
            aw, ah = cropAngle.shape[1], cropAngle.shape[0]

            myLength1 = self.calculation(box[0], box[1])
            myLength2 = self.calculation(box[1], box[2])

            # determine width and height
            if myLength1 < myLength2:
                vtcp = box[0] - box[1]
                vtcp[1] = -vtcp[1]
                vtpt = vtcp
                cen1 = (box[0] + box[1]) / 2
                cen2 = (box[2] + box[3]) / 2
            else:
                vtcp = box[1] - box[2]
                vtcp[1] = -vtcp[1]
                vtpt = vtcp
                cen1 = (box[0] + box[3]) / 2
                cen2 = (box[2] + box[1]) / 2
            _cx, _cy = (cen1 + cen2) / 2
            
            # print(_cx, _cy)
            if mode == 0:
                cv2.circle(cropGray, (int(_cx), int(_cy)), 2, (0, 255, 0), -1)
                cv2.imshow('Result', cropGray)
            # cv2.circle(sax, (_cx, _cy), 2, (0, 255, 0), -1)
            
            dodai1 = self.calculation(cen1, tam)
            dodai2 = self.calculation(cen2, tam)
            # print(dodai1, dodai2)
            if dodai1 > dodai2:
                dau = cen2
                dit = cen1
            else:
                dau = cen1
                dit = cen2
            
            #endregion

            #region: Calculate angle
            
            v1 = dau - dit
            v2 = [-3, 0]
            v_dot = v1[0] * v2[0] + v1[1] * v2[1]
            d1 = math.sqrt(v1[0]*v1[0] + v1[1]*v1[1])
            d2 = math.sqrt(v2[0]*v2[0] + v2[1]*v2[1])
            cos = v_dot / (d1*d2)
            
            #for debugging
            # print(dau, dit)
            # Positive
            if dau[1] > dit[1]:
                angle = math.acos(cos)
            elif dau[1] < dit[1]:
                angle = -math.acos(cos)
            elif dau[0] > dit[0]:
                angle = math.acos(-1)
            elif dau[0] < dit[0]:
                angle = 0
            # print(angle)
            #endregion
            # Please uncomment this if there are too bright
            # angle_real = (angle * 180.0) / 3.14159
            # if angle_real == 0 or angle_real == -0 or angle_real == 180 or angle_real == -180:
            #     _cy = _cy - 1
            # elif angle_real > 0 and angle_real <= 90:
            #     _cy = _cy - 1 * abs(math.sin(angle))
            #     _cx = _cx + 1 * abs(math.cos(angle))
            # elif angle_real > -180 and angle_real <= -90:
            #     _cy = _cy - 1 * abs(math.sin(angle))
            #     _cx = _cx + 1 * abs(math.cos(angle))
            # elif angle_real > 90 and angle_real < 180:
            #     _cy = _cy - 1 * abs(math.sin(3.14159 - angle))
            #     _cx = _cx + 1 * abs(math.cos(3.14159 - angle))
            # elif angle_real > -90 and angle_real < 0:
            #     _cy = _cy - 1 * abs(math.sin(3.14159 - angle))
            #     _cx = _cx + 1 * abs(math.cos(3.14159 - angle))
            # Return real world center of product.
            deltaX = _new_cenX - _cx
            deltaY = _new_cenY - _cy
            cx = temp_cx - deltaX
            cy = temp_cy - deltaY
            return (crop, angle, cx, cy)
        else:
            return (None, None, None, None)

    def LowBlueFilter(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([45,54,30], dtype=np.uint8)
        upper_blue = np.array([255,191,255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        res = cv2.bitwise_and(img, img, mask = mask)
        n = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
        resg = cv2.cvtColor(n, cv2.COLOR_BGR2GRAY)
        return mask

    def calculation(self, x1, x2):
        dx = x1[0] - x2[0]
        dy = x1[1] - x2[1]
        length = math.sqrt((math.pow(dx, 2)) + (math.pow(dy, 2)))
        return length

if __name__ == '__main__':
    print('haha')
    

