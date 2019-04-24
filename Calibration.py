import numpy as np
import cv2
import glob
import math
from numpy.linalg import inv

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

def GetCalibrationParams():
    images = glob.glob('Samples/*.jpg')
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
            print(corners2)                
            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (9,6), corners2,ret)
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

            np.savez('Calib.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs, corners=corners2)
            cv2.imshow('img',img)
            cv2.waitKey(0)
            break
    cv2.destroyAllWindows()

def InverseRodrigues(rotVecs):
    theta = np.linalg.norm(rotVecs)
    r = rotVecs / theta
    r_calculate = np.reshape(r, (3, 1))
    I = np.eye(3, dtype=float)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    rx, ry, rz = rotVecs.item(0), rotVecs.item(1), rotVecs.item(2)
    temp = np.array([[0, -rz, ry], [rz, 0, -rx], [-ry, rx, 0]])
    rodrigues_mat = cos_theta * I + ((1 - cos_theta)*r_calculate).dot(r_calculate.T) + sin_theta * temp
    return rodrigues_mat

def ImgPoints2RealPoints(camearMtx, rodriguesMtx, translateMtx, imgPts, scaleFactor):
    translate = np.reshape(translateMtx, (3, 1))
    rInverse = inv(rodriguesMtx)
    mInverse = inv(camearMtx)
    
    realWorldPoints = rInverse.dot(mInverse).dot(scaleFactor * imgPts) - rInverse.dot(translate)
    return realWorldPoints


    # return realWorldPoints