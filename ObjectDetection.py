import cv2
from darkflow.net.build import TFNet
import numpy as np
import imutils
import time
import math
from collections import OrderedDict
from CentroidTracker import CentroidTracker
from VelocityTracker import VelocityTracker
from ProcessItem import ProcessItem

class ObjectDetection():
    def __init__(self):
        options = {
            'model': 'cfg/tiny-yolo-voc-1c.cfg',
            'load': 12000,
            'threshold': 0.3,
            'gpu': 1.0
        }
        self.tfnet = TFNet(options)
        self.colors = [tuple(255 * np.random.rand(3)) for _ in range(5)]
        # initialize our centroid tracker and frame dimensions
        self.ct = CentroidTracker()
        # self.vt = VelocityTracker(OrderedDict())
        self.pt = ProcessItem()
        self.capture = cv2.VideoCapture(0)
        

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
        
        for idx, result in enumerate(results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])

            label = result['label']
            confidence = result['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            (startX, startY, endX, endY) = (result['topleft']['x'], result['topleft']['y'], result['bottomright']['x'], result['bottomright']['y'])
            if confidence > 0.85 and ((startX + endX) / 2) < 300:
                rects.append((startX, startY, endX, endY))

                frame_copy = cv2.rectangle(frame_copy, tl, br, (0, 255, 0), 2)    
        objects = self.ct.update(rects)
        self.pt.updateObject(rects, objects)
        (crop, angle, cx, cy) = self.pt.updateAngle(frame, mode)
        # self.vt.update(objects)
        # self.vt.velocityChange()
        
        if crop is not None:
            return frame_copy, cx, cy, angle
        else:
            pass
        #region: Do later
        # for displaying
        # for (objectID, centroid) in objects.items():
        #     # velocity = self.vt.velocity[objectID]
        #     # draw both the ID of the object and the centroid of the
        #     # object on the output frame
        #     text = "ID {}".format(objectID)
        #     # textVelocity = "{}".format(velocity)
        #     cv2.putText(frame_copy, text, (centroid[0] - 10, centroid[1] - 10),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #     cv2.putText(frame_copy, textVelocity, (centroid[0] + 10, centroid[1] + 10),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        #     cv2.circle(frame_copy, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
        #endregion
        # return frame, cx, cy, crop

    def Get_Frame(self):
        ret, last_frame = self.capture.read()
        return last_frame
    
if __name__ == '__main__':
    od = ObjectDetection()
    while True:
        frame, cx, cy, crop = od.Process()
        cv2.imshow('Frame', frame)
        
        if cv2.waitKey(1) == ord('q'):
            cv2.imwrite('crop.jpg', crop)
            break
    cv2.destroyAllWindows()