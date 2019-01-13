import cv2
from darkflow.net.build import TFNet
import numpy as np
import time

options = {
	'model': 'cfg/tiny-yolo-voc-1c.cfg',
	'load': 9750,
	'threshold': 0.1,
	'gpu': 0.8
}

tfnet = TFNet(options)
colors = [tuple(255 * np.random.rand(3)) for _ in range(5)]

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
while True:
	stime = time.time()
	ret, frame = capture.read()
	results = tfnet.return_predict(frame)
	if ret:
		for color, result in zip(colors, results):
			tl = (result['topleft']['x'], result['topleft']['y'])
			br = (result['bottomright']['x'], result['bottomright']['y'])
			label = result['label']
			confidence = result['confidence']
			text = '{}: {:.0f}%'.format(label, confidence * 100)
			frame = cv2.rectangle(frame, tl, br, (0, 255, 0), 5)
			frame = cv2.putText(
				frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
		cv2.imshow('frame', frame)
		print('FPS {:.1f}'.format(1/ (time.time() - stime)))

	if cv2.waitKey(1) & 0xFF == ord('q'):
			break

capture.release()
cv2.destroyAllWindows()
