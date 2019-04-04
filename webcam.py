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

vt = VelocityTracker(OrderedDict())
pt = ProcessItem()

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

fps = capture.get(cv2.CAP_PROP_FPS)
wait_time = 1000 / fps

count = 0
# velocity = 0
_cx_Image = 320
_cy_Image = 180
_distance = {}
_min_key = None


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

			frame = cv2.rectangle(frame, tl, br, (0, 255, 0), 2)
			
	pt.updateObject(rects)
	(crop, angle, cx, cy) = pt.updateAngle(frame)
	if crop is not None:
		cv2.imshow('Process Item', crop)
		# cv2.circle(crop, (cx, cy), 2, (0, 255, 0), -1)
		print(cx, cy)
	else:
		pass
	objects = ct.update(rects)
	# print(objects)
	vt.update(objects)
	vt.velocityChange()
	for (objectID, centroid) in objects.items():
		velocity = vt.velocity[objectID]
		# draw both the ID of the object and the centroid of the
		# object on the output frame
		text = "ID {}".format(objectID)
		textVelocity = "{}".format(velocity)
		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.putText(frame, textVelocity, (centroid[0] + 10, centroid[1] + 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
		
	# cv2.circle(frame, (cx, cy), 4, (255, 255, 0), -1)
	
	
	cv2.imshow('frame', frame)
	delta_time = (time.time() - stime) * 1000
	if delta_time > wait_time:
		delay_time = 1
	else:
		delay_time = wait_time - delta_time


	if cv2.waitKey(int(delay_time)) & 0xFF == ord('q'):
		cv2.imwrite('crop.jpg', crop)
		break


capture.release()
cv2.destroyAllWindows()
