import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import numpy as np
import os
import math


def calculation(x1, x2):
    dx = x1[0] - x2[0]
    dy = x1[1] - x2[1]
    length = math.sqrt((math.pow(dx, 2)) + (math.pow(dy, 2)))
    return length


def Min_value(pos):
    Min_value.value = pos


Min_value.value = 0


def Max_value(pos):
    Max_value.value = pos


Max_value.value = 255


X_ERROR = 20
Y_ERROR = 20
options = {
	'model': 'cfg/tiny-yolo-voc-1c.cfg',
	'load': 9750,
	'threshold': 0.2,
	'gpu': 1
}

tfnet = TFNet(options)

colors = [tuple(255 * np.random.rand(3)) for i in range(5)]
# Image classification
img = cv2.imread('0.png', cv2.IMREAD_COLOR)
img = cv2.resize(img, (640, 360))
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
result = tfnet.return_predict(img)
print(result)
for idx, res in enumerate(result):
	tl = (res['topleft']['x'], res['topleft']['y'])
	br = (res['bottomright']['x'], res['bottomright']['y'])

	label = res['label']
	confidence = res['confidence']
	text = '{}: {:.0f}%'.format(label, confidence * 100)
		
	if confidence > 0.70:
		img = cv2.rectangle(img, tl, br, (0, 255, 0), 2)
		img = cv2.putText(img, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
			################ Image processing #############################################
cv2.imshow('haha', img)
tl = (result[0]['topleft']['x'], result[0]['topleft']['y'])
br = (result[0]['bottomright']['x'], result[0]['bottomright']['y'])
label = result[0]['label']


# Crop the image to take the object
imcrop = img[tl[1]-Y_ERROR:br[1]+Y_ERROR, tl[0]-X_ERROR:br[0]+X_ERROR]
imcrop = cv2.cvtColor(imcrop, cv2.COLOR_RGB2BGR)
imcropGray = cv2.cvtColor(imcrop, cv2.COLOR_BGR2GRAY)
equ = cv2.equalizeHist(imcropGray)

cv2.namedWindow("Control", cv2.WINDOW_NORMAL)
cv2.resizeWindow('Control', 600,600)
cv2.createTrackbar("Min value", 'Control', 0, 255, Min_value)
cv2.createTrackbar("Max value", 'Control', 255, 255, Max_value)
while True:
	blur = cv2.GaussianBlur(equ, (5, 5), 0)
	cv2.imshow('Blur', blur)
	# ret, thresh = cv2.threshold(blur, Min_value.value, Max_value.value, 0)
	ret, thresh = cv2.threshold(blur, 102, 255, 0)
	myThresh = 255 - thresh
	cv2.imshow('First step', myThresh)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	erosion = cv2.erode(myThresh, kernel, iterations = 2)
	cv2.imshow('After erosion', erosion)
	closing = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, kernel, iterations = 2)
	cv2.imshow("Thresh hold", closing)
	if cv2.waitKey(10) == ord('q'):
		break
im2, contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    # compute the center of the contour
    # M = cv2.moments(c)
    # if M['m00'] != 0:
    #     cX = int(M['m10'] / M['m00'])
    #     cY = int(M['m01'] / M['m00'])
    #     cv2.circle(imcrop, (cX, cY), 4, (0, 0, 255), -1)
    #     cv2.putText(imcrop, "center", (cX - 20, cY - 20),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # # draw the contour and center of the shape on the image
    # cv2.drawContours(imcrop, [c], -1, (0, 255, 0), 2)
	approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
	print(len(approx))
cv2.imshow('imcrop', imcrop)

# Determine angle
c = max(contours, key = cv2.contourArea)
rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)
box = np.int0(box)
myOutput = np.zeros((300, 300))
for x in range(0, 4, 1):
    cv2.circle(imcrop, (box[x][0], box[x][1]), 4, (0, 0, 255), -1)
    cv2.putText(imcrop, str(x), (box[x][0] - 20, box[x][1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
cv2.drawContours(imcrop, [box], 0, (0, 255, 0), 2)
cv2.imshow('imcrop', imcrop)

myLength1 = calculation(box[0], box[1])
myLength2 = calculation(box[1], box[2])

myOutput = np.zeros((300, 300))

if myLength1 >= myLength2:
    cv2.putText(myOutput, "Chieu dai: doan 0 1", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(myOutput, "Chieu rong: doan 1 2", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
else:
    cv2.putText(myOutput, "Chieu dai: doan 1 2", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(myOutput, "Chieu rong: doan 0 1", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
cv2.putText(myOutput, "Point[0]:{0}".format(str(box[0])), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
cv2.putText(myOutput, "Point[1]:{0}".format(str(box[1])), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
cv2.putText(myOutput, "Point[2]:{0}".format(str(box[2])), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
cv2.putText(myOutput, "Point[3]:{0}".format(str(box[3])), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
cv2.putText(myOutput, "Angle:{0}".format(str(-rect[2])), (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

cv2.namedWindow("Parameters", cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow("Parameters", 300, 300)
cv2.imshow("Parameters", myOutput)
# Optional: draw a box cover all the object
img = cv2.rectangle(img, tl, br, (0, 255, 0), 5)
img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
plt.imshow(img)
plt.show()


