import cv2
from darkflow.net.build import TFNet
import numpy as np
import imutils
import time
import math
from CentroidTracker import CentroidTracker


X_ERROR = 20
Y_ERROR = 20

def calculation(x1, x2):
    dx = x1[0] - x2[0]
    dy = x1[1] - x2[1]
    length = math.sqrt((math.pow(dx, 2)) + (math.pow(dy, 2)))
    return length

options = {
	'model': 'cfg/tiny-yolo-voc-1c.cfg',
	'load': 9750,
	'threshold': 0.2,
	'gpu': 1
}

tfnet = TFNet(options)
colors = [tuple(255 * np.random.rand(3)) for _ in range(5)]
# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)


capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

fps = capture.get(cv2.CAP_PROP_FPS)
wait_time = 1000 / fps

count = 0
velocity = 0
_cx_Image = 320
_cy_Image = 180
_distance = {}
_min_key = None
cv2.namedWindow('imcrop', cv2.WINDOW_NORMAL)
cv2.resizeWindow('imcrop', 150, 150)
myResult = []
while True:
	stime = time.time()
	ret, frame = capture.read()
	frame = cv2.resize(frame, (640, 360))

	# if the frame dimensions are None, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	results = tfnet.return_predict(frame)
	rects = []
	# print(results)	
	# for idx, result in enumerate(results):
	# 	tl = (result['topleft']['x'], result['topleft']['y'])
	# 	br = (result['bottomright']['x'], result['bottomright']['y'])
	# 	cx = (tl[0] + br[0]) / 2
	# 	cy = (tl[1] + br[1]) / 2
	# 	distance = calculation((cx, cy), (_cx_Image, _cy_Image))
	# 	_distance[str(idx)] = distance
	# _min_key = min(_distance.keys(), key=(lambda k: _distance[k]))
	# print(_min_key)
	# if ret:
	for idx, result in enumerate(results):
		# result = results[int(_min_key)]
		tl = (result['topleft']['x'], result['topleft']['y'])
		br = (result['bottomright']['x'], result['bottomright']['y'])

		label = result['label']
		confidence = result['confidence']
		text = '{}: {:.0f}%'.format(label, confidence * 100)
		(startX, startY, endX, endY) = (result['topleft']['x'], result['topleft']['y'], result['bottomright']['x'], result['bottomright']['y'])
		if confidence > 0.70:
			rects.append((startX, startY, endX, endY))
			# right_frame = frame.copy()
			frame = cv2.rectangle(frame, tl, br, (0, 255, 0), 2)
			# frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
			# ################ Image processing #############################################

			# imcrop = right_frame[tl[1] - Y_ERROR:br[1] + Y_ERROR, tl[0] - X_ERROR:br[0] + X_ERROR]
			# imcropGray = cv2.cvtColor(imcrop, cv2.COLOR_BGR2GRAY)
			# equ = cv2.equalizeHist(imcropGray)
			# blur = cv2.GaussianBlur(equ, (5, 5), 0)
			# ret, thresh = cv2.threshold(blur, 102, 255, 0)
			# myThresh = 255 - thresh
			# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
			# erosion = cv2.erode(myThresh, kernel, iterations=2)
			
			# im2, contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			
			# c = max(contours, key = cv2.contourArea)
			
			# rect = cv2.minAreaRect(c)
			# box = cv2.boxPoints(rect)
			# box = np.int0(box)
			# cx = int((box[0][0] + box[1][0] + box[2][0] + box[3][0]) / 4)
			# cy = int((box[0][1] + box[1][1] + box[2][1] + box[3][1]) / 4)
			# myOutput = np.zeros((300, 300))
			# for x in range(0, 4, 1):
			# 	cv2.circle(imcrop, (box[x][0], box[x][1]), 4, (0, 0, 255), -1)
			# 	cv2.putText(imcrop, str(x), (box[x][0] - 20, box[x][1] - 20),
			# 	                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
			# cv2.circle(imcrop, (cx, cy), 4, (0, 0, 255), -1)
			# cv2.drawContours(imcrop, [box], 0, (0, 255, 0), 2)
			# cv2.imshow('imcrop', imcrop)
		# print(myResult)
	objects = ct.update(rects)
	for (objectID, centroid) in objects.items():
		# draw both the ID of the object and the centroid of the
		# object on the output frame
		text = "ID {}".format(objectID)
		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
	
	cv2.imshow('frame', frame)
	delta_time = (time.time() - stime) * 1000
	if delta_time > wait_time:
		delay_time = 1
	else:
		delay_time = wait_time - delta_time
	# print('FPS {:.1f}'.format(1 / (time.time() - stime)))
	


	# if ret:
	# 	for color, result in zip(colors, results):
	# 		tl = (result['topleft']['x'], result['topleft']['y'])
	# 		br = (result['bottomright']['x'], result['bottomright']['y'])

	# 		label = result['label']
	# 		confidence = result['confidence']
	# 		text = '{}: {:.0f}%'.format(label, confidence * 100)

	# 		if confidence > 0.70:
	# 			right_frame = frame.copy()
	# 			frame = cv2.rectangle(frame, tl, br, (0, 255, 0), 2)
	# 			frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
	# 			################ Image processing #############################################
				

	# 			imcrop = right_frame[tl[1]-Y_ERROR:br[1]+Y_ERROR, tl[0]-X_ERROR:br[0]+X_ERROR]
	# 			# imcrop = cv2.cvtColor(imcrop, cv2.COLOR_RGB2BGR)
	# 			# cv2.imshow('test', imcrop)
	# 			imcropGray = cv2.cvtColor(imcrop, cv2.COLOR_BGR2GRAY)
	# 			equ = cv2.equalizeHist(imcropGray)
	# 			blur = cv2.GaussianBlur(equ, (5, 5), 0)
	# 			ret, thresh = cv2.threshold(blur, 102, 255, 0)
	# 			myThresh = 255 - thresh
	# 			kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	# 			erosion = cv2.erode(myThresh, kernel, iterations = 2)
	# 			# closing = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, kernel, iterations = 2)
	# 			im2, contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# 			c = contours[0]
	# 			rect = cv2.minAreaRect(c)
	# 			box = cv2.boxPoints(rect)
	# 			box = np.int0(box)
	# 			cx = int((box[0][0] + box[1][0] + box[2][0] + box[3][0]) / 4)
	# 			cy = int((box[0][1] + box[1][1] + box[2][1] + box[3][1]) / 4)
	# 			myOutput = np.zeros((300, 300))
	# 			for x in range(0, 4, 1):
	# 			    cv2.circle(imcrop, (box[x][0], box[x][1]), 4, (0, 0, 255), -1)
	# 			    cv2.putText(imcrop, str(x), (box[x][0] - 20, box[x][1] - 20),
	# 			                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	# 			cv2.circle(imcrop, (cx, cy), 4, (0, 0, 255), -1)
	# 			cv2.drawContours(imcrop, [box], 0, (0, 255, 0), 2)
	# 			cv2.imshow('imcrop', imcrop)
	# 	cv2.imshow('frame', frame)
	# 	delta_time = (time.time() - stime) * 1000
	# 	if delta_time > wait_time:
	# 		delay_time = 1
	# 	else:
	# 		delay_time = wait_time - delta_time
	# 	print('FPS {:.1f}'.format(1/ (time.time() - stime)))

	if cv2.waitKey(int(delay_time)) & 0xFF == ord('q'):
		break
	# if cv2.waitKey(1) & 0xFF == ord('q'):
	# 	break

capture.release()
cv2.destroyAllWindows()
