import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
import os

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
fps = capture.get(cv2.CAP_PROP_FPS)
wait_time = 1000 / fps
i = 121
while(capture.isOpened()):
    pre_time = time.time()
    ret, frame = capture.read()
    cv2.imshow("Frame", frame)
    cv2.imwrite(str(i) + ".jpg", frame)
    i = i + 1
    delta_time = (time.time() - pre_time) * 1000
    if delta_time > wait_time:
        delay_time = 1
    else:
        delay_time = wait_time - delta_time
    key = cv2.waitKey(int(delay_time))
    if key == ord('q'):
        break
    
    
capture.release()
cv2.destroyAllWindows()