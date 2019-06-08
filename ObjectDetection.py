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
        self.capture = cv2.VideoCapture(0)
        options = {
            'model': 'cfg/tiny-yolo-voc-1c.cfg',
            'load': 12000,
            'threshold': 0.25,
            'gpu': 1.0
        }
        self.tfnet = TFNet(options)
        self.colors = [tuple(255 * np.random.rand(3)) for _ in range(5)]
        # initialize our centroid tracker and frame dimensions
        self.ct = CentroidTracker()
        # self.vt = VelocityTracker(OrderedDict())
        self.pt = ProcessItem()
        
        

        fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.wait_time = 1000 / fps
        self.count = 0
        self.angle = 0
        self.cx = 0
        self.cy = 0
        #region: Testing
        try:
            #region: Load M, R, T, corners for Mode 1
            with np.load('Calib.npz') as X:
                self.mtx, self.dist, self.rvects, self.tvects, self.corners = [X[i] for i in ('mtx','dist','rvecs','tvecs', 'corners')]
           
            self.rodrigues_Vecs = InverseRodrigues(self.rvects)
            translate = np.reshape(self.tvects, (3, 1))
            K = np.concatenate((self.rodrigues_Vecs, translate), axis=1)
            a = self.mtx.dot(K).dot(np.array([[1, 1, 1, 1]]).T)
            self.s = a.item(2)
            #endregion

            #region: Load M, R, T, corners for Mode 2
            with np.load('Calib_bc.npz') as P:
                self.mtx_BC, self.dist_BC, self.rvects_BC, self.tvects_BC, self.corners_BC = [P[i] for i in ('mtx','dist','rvecs','tvecs', 'corners')]

            self.rodrigues_Vecs_BC = InverseRodrigues(self.rvects_BC)
            translate_BC = np.reshape(self.tvects_BC, (3, 1))
            K_bc = np.concatenate((self.rodrigues_Vecs_BC, translate_BC), axis=1)
            a_bc = self.mtx_BC.dot(K_bc).dot(np.array([[1, 1, 1, 1]]).T)
            self.s_BC = a_bc.item(2)
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
        #endregion
    
    def Process(self, mode):
        pre_time = time.time()
        ret, img = self.capture.read()

        # region: Testing 
        h,  w = img.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(self.mtx,self.dist,(w,h),1,(w,h))
        # undistort
        dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)

        # crop the image
        x,y,w,h = roi
        frame = dst[y:y+h, x:x+w]

        #endregion
        
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
            if mode == 0:
                if ((startX + endX) / 2) < 300:
                    rects.append((startX, startY, endX, endY))

                    frame_copy = cv2.rectangle(frame_copy, tl, br, (0, 255, 0), 2)   
            elif mode == 1:
                if ((startY + endY) / 2) > 100 and ((startX + endX) / 2) < 300:
                    rects.append((startX, startY, endX, endY))

                    frame_copy = cv2.rectangle(frame_copy, tl, br, (0, 255, 0), 2)   

        objects = self.ct.update(rects)
        self.pt.updateObject(rects, objects)
        (crop, angle, cx, cy) = self.pt.updateAngle(frame, mode)
        # self.vt.update(objects)
        # velocity = self.vt.velocityChange()
        # print(velocity)
        # print(time.time() - pre_time)
        if crop is not None:
            # frame_copy = cv2.circle(frame_copy, (cx, cy), 2, (0, 255, 0), -1)
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
        try:
            frame, cx, cy, crop = od.Process(0)
        except:
            frame = od.Get_Frame()
        cv2.imshow('Frame', frame)
        
        if cv2.waitKey(1) == ord('q'):
            cv2.imwrite('crop.jpg', crop)
            break
    cv2.destroyAllWindows()