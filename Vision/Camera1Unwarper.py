import numpy as np
import cv2

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((5 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.


def set_res(cap, x, y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def main():
    cam = cv2.VideoCapture(0)
    set_res(cam, 1920, 1080)
    i = 0
    while i < 100:
        ret_val, img = cam.read()
        i += 1
    new_img = img[1:int(len(img) / 3), 1:int(len(img[0]) / 3), :]

    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("", gray)
    # cv2.waitKey()
    print("YOOT")
    ret, corners = cv2.findChessboardCorners(gray, (7, 5), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print("troot")

        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(new_img, (7, 5), corners2, ret)
        cv2.imshow('img', new_img)
        cv2.waitKey()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    h, w = img.shape[:2]
    # undistort
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    cv2.imshow("", dst)
    cv2.waitKey()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
