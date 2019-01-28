import numpy as np
import cv2
import glob
import math


# Assume that camera 1 is labelled camera_no=1
def getImgRegionByCameraNo(img, camera_no):
    x_lower_bound = int((len(img) / 3) * math.floor((camera_no - 1) / 3))
    x_upper_bound = int((len(img) / 3) * (math.floor(camera_no / 4) + 1))

    y_lower_bound = int((len(img[0]) / 3) * ((camera_no - 1) % 3))
    y_upper_bound = int((len(img[0]) / 3) * (((camera_no - 1) % 3) + 1))

    return img[x_lower_bound:x_upper_bound, y_lower_bound:y_upper_bound, :]


# All in one signifies to calibrate the cameras using the different angles of chessboards from all of them to produce
# the transformation matrix

def calibrateCamera(all_in_one=True):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    grid_range = [(i, j) for i in range(3, 8) for j in range(3, 6)]
    grid_range.sort(key=sum, reverse=True)

    # Arrays to store object points and image points from all the images.
    if all_in_one:
        objpoint = []
        imgpoint = []
    else:
        objpoints = [[], [], [], []]  # 3d point in real world space
        imgpoints = [[], [], [], []]  # 2d points in image plane.

    images = glob.glob("Calibration Pictures/*.jpg")

    for fname in images:
        original_img = cv2.imread(fname)
        for camera_no in range(0, 4):
            for grid_val in grid_range:
                focused_img = getImgRegionByCameraNo(original_img, camera_no + 1)
                gray = cv2.cvtColor(focused_img, cv2.COLOR_BGR2GRAY)

                # Find the chess board corners
                ret, corners = cv2.findChessboardCorners(gray, grid_val, None)

                # If found, add object points, image points (after refining them)
                if ret == True:
                    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
                    objp = np.zeros((grid_val[1] * grid_val[0], 3), np.float32)
                    objp[:, :2] = np.mgrid[0:grid_val[0], 0:grid_val[1]].T.reshape(-1, 2)

                    if all_in_one:
                        objpoint.append(objp)
                    else:
                        objpoints[camera_no].append(objp)

                    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                    if all_in_one:
                        imgpoint.append(corners2)
                    else:
                        imgpoints[camera_no].append(corners2)

                    # Draw and display the corners
                    focused_img = cv2.drawChessboardCorners(focused_img, grid_val, corners2, ret)
                    break
        cv2.imshow('img', original_img)
        cv2.waitKey(10)

    if all_in_one:
        _, mtx, dist, _, _ = cv2.calibrateCamera(objpoint, imgpoint, gray.shape[::-1],
                                                 None, None)
    else:
        mtxs = []
        dists = []
        for camera_no in range(0, 4):
            _, mtx, dist, _, _ = cv2.calibrateCamera(objpoints[camera_no], imgpoints[camera_no], gray.shape[::-1],
                                                     None, None)
            mtxs.append(mtx)
            dists.append(dist)

    for fname in images:
        original_img = cv2.imread(fname)
        dsts = []
        dsts2 = []
        for camera_no in range(0, 4):
            img = getImgRegionByCameraNo(original_img, camera_no + 1)
            h, w = img.shape[:2]
            if all_in_one:
                newcameramtx, _ = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
                dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
            else:
                newcameramtx, _ = cv2.getOptimalNewCameraMatrix(mtxs[camera_no], dists[camera_no], (w, h), 1, (w, h))
                dst = cv2.undistort(img, mtxs[camera_no], dists[camera_no], None, newcameramtx)
            if camera_no == 0:
                dsts = dst
            elif camera_no == 1:
                dsts = np.concatenate((dsts, dst), axis=1)
            elif camera_no == 2:
                dsts2 = dst
            elif camera_no == 3:
                dsts2 = np.concatenate((dsts2, dst), axis=1)
                dsts = np.concatenate((dsts, dsts2), axis=0)
        cv2.imshow("Undistorted image", dsts)
        cv2.waitKey()

    cv2.destroyAllWindows()


calibrateCamera(all_in_one=False)
