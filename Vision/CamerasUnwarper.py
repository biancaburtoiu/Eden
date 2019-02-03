import numpy as np
import cv2
import glob
import math
import time

# Segment the specified camera box from the CCTV screen
# Assume that camera 1 is labelled camera_no=1
def getImgRegionByCameraNo(img, camera_no):
    x_lower_bound = int((len(img) / 3) * math.floor((camera_no - 1) / 3)) + 2
    x_upper_bound = int((len(img) / 3) * (math.floor(camera_no / 4) + 1)) - 2

    y_lower_bound = int((len(img[0]) / 3) * ((camera_no - 1) % 3)) + 2
    y_upper_bound = int((len(img[0]) / 3) * (((camera_no - 1) % 3) + 1)) - 2

    return img[x_lower_bound:x_upper_bound, y_lower_bound:y_upper_bound, :]


# Method used to calibrate the cameras to ensure objects on the ground at different places in the image appear the same
# size

# All in one signifies to calibrate the cameras using the different angles of chessboards from all of them to produce
# the transformation matrix

def calibrateCamera(all_in_one=False, objpoints=None, imgpoints=None, visualize=True, photo_path="Vision/Calibration Pictures/*.jpg"):
    start_time = time.time()

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    grid_range = [(i, j) for i in range(3, 9) for j in range(3, 7)]
    grid_range.sort(key=sum, reverse=True)

    # Arrays to store object points and image points from all the images.
    if objpoints is None and imgpoints is None:
        if all_in_one:
            objpoints = []
            imgpoints = []
        else:
            objpoints = [[], [], [], []]  # 3d point in real world space
            imgpoints = [[], [], [], []]  # 2d points in image plane.

    images = glob.glob(photo_path)

    i = 1
    # For each CCTV image
    for fname in images:
        original_img = cv2.imread(fname)
        # Try and find a chessboard in each camera
        for camera_no in range(0, 4):
            # Try every possible subsize of the actual size of the chessboard, in case it is partially obscured
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
                        objpoints.append(objp)
                    else:
                        objpoints[camera_no].append(objp)

                    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                    if all_in_one:
                        imgpoints.append(corners2)
                    else:
                        imgpoints[camera_no].append(corners2)

                    # Draw and display the corners
                    focused_img = cv2.drawChessboardCorners(focused_img, grid_val, corners2, ret)
                    break
        if visualize:
            # Show where open-cv found the chessboard on each camera
            cv2.imshow('img', original_img)
            cv2.waitKey(10)
        print("%.2f mins: Found chessboards on image %s of %s" % ((time.time() - start_time) / 60, i, len(images)))
        i += 1

    # Compute the matrices to transform each image

    if all_in_one:
        _, mtxs, dists, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],
                                                   None, None)
    else:
        mtxs = []
        dists = []
        for camera_no in range(0, 4):
            _, mtx, dist, _, _ = cv2.calibrateCamera(objpoints[camera_no], imgpoints[camera_no], gray.shape[::-1],
                                                     None, None)
            print("%.2f mins: Determined mtx and dst for camera %s" % ((time.time() - start_time) / 60, camera_no))
            mtxs.append(mtx)
            dists.append(dist)

    # Show the result of the transform for each image

    if visualize:
        for fname in images:
            original_img = cv2.imread(fname)
            dsts = []
            dsts2 = []
            for camera_no in range(0, 4):
                img = getImgRegionByCameraNo(original_img, camera_no + 1)
                h, w = img.shape[:2]
                if all_in_one:
                    newcameramtx, _ = cv2.getOptimalNewCameraMatrix(mtxs, dists, (w, h), 1, (w, h))
                    dst = cv2.undistort(img, mtxs, dists, None, newcameramtx)
                else:
                    newcameramtx, _ = cv2.getOptimalNewCameraMatrix(mtxs[camera_no], dists[camera_no], (w, h), 1,
                                                                    (w, h))
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

    return mtxs, dists, objpoints, imgpoints
