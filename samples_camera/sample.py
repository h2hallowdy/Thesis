import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
import os

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
fps = video.get(cv2.CAP_PROP_FPS)
i = 300
while(capture.isOpened()):
	ret, frame = capture.read()
	cv2.imshow("Frame", frame)
	print fps
	# if cv2.waitKey(1) & 0xFF == ord('c'):
	# 	while i < 400:
	# 		cv2.imwrite(str(i) + ".jpg", frame)
	# 		i = i + 1
	# 	break
	
capture.release()
cv2.destroyAllWindows()