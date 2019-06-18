#----------------------------------------------------------------------------------------------
# Name:             Calibration Camera
# Purpose:          Calibrate camera by extrinsic, intrinsic and camera mtx
# Author:           NXH
# Created:          Wednesday April 24
# Input:            Samples images at ./Samples/*.jpg
# Output:           cam mtx, distortion, rotation/ translation vecs, corners = reference points
#-----------------------------------------------------------------------------------------------

import numpy as np
import cv2
import glob
import math
from numpy.linalg import inv

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
total_points_used=54
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
            
            cv2.imshow('img',img)
            img = cv2.imread('Samples/frame2.jpg')
            h,  w = img.shape[:2]
            newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),0,(w,h))
            world = np.array([objpoints], dtype=np.float32)
            world = np.reshape(world, (54, 3))
            imgp = np.array([imgpoints], dtype=np.float32)
            imgp = np.reshape(imgp, (-1, 2))
            
            ret, rvec1, tvec1=cv2.solvePnP(world,imgp,newcameramtx,dist)
            R_mtx, jac=cv2.Rodrigues(rvec1)
            Rt=np.column_stack((R_mtx,tvec1))
            P_mtx=newcameramtx.dot(Rt)
            inverse_newcam_mtx = np.linalg.inv(newcameramtx)
            # np.savez('B.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs, corners=corners2, tvec1=tvec1)
            # # undistort
            # dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
            s_arr=np.array([0], dtype=np.float32)
            s_describe=np.zeros((54, 1), dtype=np.float32)

            for i in range(0,total_points_used):
                print("=======POINT # " + str(i) +" =========================")
                
                print("Forward: From World Points, Find Image Pixel")
                XYZ1=np.array([[world[i,0],world[i,1],world[i,2],1]], dtype=np.float32)
                XYZ1=XYZ1.T
                print("{{-- XYZ1")
                print(XYZ1)
                suv1=P_mtx.dot(XYZ1)
                print("//-- suv1")
                print(suv1)
                s=suv1[2,0]    
                uv1=suv1/s
                print(">==> uv1 - Image Points")
                print(uv1)
                print(">==> s - Scaling Factor")
                print(s)
                s_arr=np.array([s/total_points_used+s_arr[0]], dtype=np.float32)
                s_describe[i]=s
                

                print("Solve: From Image Pixels, find World Points")

                uv_1=np.array([[imgp[i,0],imgp[i,1],1]], dtype=np.float32)
                uv_1=uv_1.T
                print(">==> uv1")
                print(uv_1)
                suv_1=s*uv_1
                print("//-- suv1")
                print(suv_1)

                print("get camera coordinates, multiply by inverse Camera Matrix, subtract tvec1")
                xyz_c=inverse_newcam_mtx.dot(suv_1)
                xyz_c=xyz_c-tvec1
                print("      xyz_c")
                inverse_R_mtx = np.linalg.inv(R_mtx)
                XYZ=inverse_R_mtx.dot(xyz_c)
                print("{{-- XYZ")
                print(XYZ)
            
            s_mean, s_std = np.mean(s_describe), np.std(s_describe)
            np.savez('Calib_bc.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs, corners=corners2, tvec1=tvec1, rvec1=rvec1,s=s_mean, newcameramtx=newcameramtx)
            print(">>>>>>>>>>>>>>>>>>>>> S RESULTS")
            print("Mean: "+ str(s_mean))
            #print("Average: " + str(s_arr[0]))
            print("Std: " + str(s_std))

            print(">>>>>> S Error by Point")

            for i in range(0,total_points_used):
                print("Point "+str(i))
                print("S: " +str(s_describe[i])+" Mean: " +str(s_mean) + " Error: " + str(s_describe[i]-s_mean))

            
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