import cv2


class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
    
    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)

    def get_frame(self):
        ret, self.last_frame = self.cap.read()
        cv2.putText(self.last_frame, 'haha', (60, 50),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return self.last_frame

    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            movie.append(self.get_frame())
        return movie

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def close_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)

if __name__ == '__main__':
    cam = Camera(1)
    cam.initialize()
    print(cam)
    frame = cam.get_frame()
    print(frame)
    cam.close_camera()