import numpy as np
import cv2
import glob
import math


def getImgRegionByCameraNo(img, camera_no):
    x_lower_bound = int((len(img) / 3) * ((camera_no - 1) % 3))
    x_upper_bound = int((len(img) / 3) * (camera_no % 3))

    y_lower_bound = int((len(img[0]) / 3) * math.floor((camera_no - 1) / 3))
    y_upper_bound = int((len(img[0]) / 3) * (math.floor(camera_no / 3) + 1))

    return img[x_lower_bound:x_upper_bound, y_lower_bound:y_upper_bound, :]


def calibrateCamera(camera_no):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((5 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    cameras = ["Camera 1", "Camera 2", "Camera 3", "Camera 4"]

    images = glob.glob("Calibration Pictures/" + cameras[camera_no - 1] + "/*.jpg")

    for fname in images:
        img = getImgRegionByCameraNo(cv2.imread(fname), camera_no)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 5), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (7, 6), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    img = getImgRegionByCameraNo(cv2.imread("Calibration Pictures/" + cameras[camera_no - 1] + "/0.jpg"), camera_no)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    cv2.imshow("Undistorted %s" % cameras[camera_no - 1], dst)
    cv2.waitKey()

    cv2.destroyAllWindows()


calibrateCamera(1)
