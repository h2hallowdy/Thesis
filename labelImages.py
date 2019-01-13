import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import numpy as np
import os

options = {
	'model': 'cfg/tiny-yolo-voc-1c.cfg',
	'load': 9750,
	'threshold': 0.4,
	'gpu': 0.8
}

tfnet = TFNet(options)

colors = [tuple(255 * np.random.rand(3)) for i in range(5)]
for file in os.listdir('./samples_camera_new'):

	img = cv2.imread(os.path.join('./samples_camera_new',file), cv2.IMREAD_COLOR)
	
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	fig, ax = plt.subplots(1)
	results = tfnet.return_predict(img)

	for color, result in zip(colors, results):
		tl = (result['topleft']['x'], result['topleft']['y'])
		br = (result['bottomright']['x'], result['bottomright']['y'])
		label = result['label']
		img = cv2.rectangle(img, tl, br, (0, 255, 0), 5)
		img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
	ax.imshow(img)
	plt.show()
	cv2.waitKey()	
# img = cv2.imread('battery_test2.jpg', cv2.IMREAD_COLOR)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# result = tfnet.return_predict(img)
# tl = (result[0]['topleft']['x'], result[0]['topleft']['y'])
# br = (result[0]['bottomright']['x'], result[0]['bottomright']['y'])
# label = result[0]['label']

# img = cv2.rectangle(img, tl, br, (0, 255, 0), 5)
# img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
# plt.imshow(img)
# plt.show()