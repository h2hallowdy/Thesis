import cv2
from darkflow.net.build import TFNet
import numpy as np
import imutils
import time
import math
import random
from collections import OrderedDict
from CentroidTracker import CentroidTracker
from VelocityTracker import VelocityTracker
from ProcessItem import ProcessItem
from ProcessErasor import ProcessErasor

class ObjectDetection():
    def __init__(self):
        self.capture = cv2.VideoCapture('Bangchuyens.avi')
        options = {
            'model': 'cfg/tiny-yolo-voc-2c.cfg',
            'load': 12250,
            'threshold': 0.25,
            'gpu': 1.0
        }
        self.tfnet = TFNet(options)
        self.colors = [tuple(255 * np.random.rand(3)) for _ in range(5)]
        # initialize our centroid tracker and frame dimensions
        self.ct = CentroidTracker()
        self.ct_erasor = CentroidTracker()
        # self.vt = VelocityTracker(OrderedDict())
        self.pt = ProcessItem()
        self.pt_erasor = ProcessErasor()
        fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.wait_time = 1000 / fps
        self.count = 0
        self.angle = 0
        self.cx = 0
        self.cy = 0
    
    def Process(self, mode):
        pre_time = time.time()
        ret, frame = self.capture.read()
        # frame = cv2.resize(frame, (640, 360))
        frame_copy = frame.copy()
        results = self.tfnet.return_predict(frame)
        rects = []
        rects_erasor=[]
        for idx, result in enumerate(results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])

            label = result['label']
            confidence = result['confidence']
            text = '{}'.format(label)
            (startX, startY, endX, endY) = (result['topleft']['x'], result['topleft']['y'], result['bottomright']['x'], result['bottomright']['y'])
            if mode == 0:
                if ((startX + endX) / 2) < 300:
                    if label == 'battery':
                        rects.append((startX, startY, endX, endY))
                        frame_copy = cv2.rectangle(frame_copy, tl, br, (0, 255, 0), 2)  
                        cv2.putText(frame_copy, text, (int((startX + endX) / 2) - 10, int((startY + endY) / 2) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    elif label == 'erasor':
                        rects_erasor.append((startX, startY, endX, endY))
                        frame_copy = cv2.rectangle(frame_copy, tl, br, (0, 0, 255), 2)  
                        cv2.putText(frame_copy, text, (int((startX + endX) / 2) - 10, int((startY + endY) / 2) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            elif mode == 1:
                if ((startX + endX) / 2) < 300 and ((startY + endY) / 2) > 100:
                    if label == 'battery':
                        rects.append((startX, startY, endX, endY))
                        frame_copy = cv2.rectangle(frame_copy, tl, br, (0, 255, 0), 2)  
                        cv2.putText(frame_copy, text, (int((startX + endX) / 2) - 10, int((startY + endY) / 2) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    elif label == 'erasor':
                        rects_erasor.append((startX, startY, endX, endY))
                        frame_copy = cv2.rectangle(frame_copy, tl, br, (0, 0, 255), 2)  
                        cv2.putText(frame_copy, text, (int((startX + endX) / 2) - 10, int((startY + endY) / 2) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        objects = self.ct.update(rects)
        erasors = self.ct_erasor.update(rects_erasor)
        '''
        randomize what to return : battery or erasor?
        len(objects) == 0 => erasors only
        len(erasors) == 0 => battery only
        Battery => processItem()
        Erasor => Other...()
        '''
        for (objectID, centroid) in objects.items():
            text = "ID {}".format(objectID)
            cv2.circle(frame_copy, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
        for (objectID, centroid) in erasors.items():
            text = "ID {}".format(objectID)
            cv2.circle(frame_copy, (centroid[0], centroid[1]), 4, (0, 0, 255), -1)
        if len(objects) != 0:
            productStyle = 'Battery'
            self.pt.updateObject(rects, objects)
            (crop, angle, cx, cy) = self.pt.updateAngle(frame, mode)
            return frame_copy, cx, cy, angle, productStyle
        if len(erasors) != 0:
            productStyle = 'Erasor'
            self.pt_erasor.updateObject(rects_erasor, erasors)
            (crop, angle, cx, cy) = self.pt_erasor.updateAngle(frame, mode)
            return frame_copy, cx, cy, angle, productStyle
        else: 
            print('Nothing to catch')
            pass
          

    def Get_Frame(self):
        ret, last_frame = self.capture.read()
        return last_frame
    
if __name__ == '__main__':
    od = ObjectDetection()
    while True:
        try:
            frame, _,_, angle, style = od.Process(0)
            # frame = od.Process(1)
            print('{} ---- {}'.format(angle * 180.0 /3.14159, style))
            
        except Exception as e:
            print(e)
            frame = od.Get_Frame()
        cv2.imshow('Frame', frame)
        
        if cv2.waitKey(1) == ord('q'):
            cv2.imwrite('crop.jpg', crop)
            break
    cv2.destroyAllWindows()