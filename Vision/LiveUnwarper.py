import cv2
import Vision.CamerasUnwarper
import numpy as np


def set_res(cap, x, y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def unwarp_image(mtxs, dists, original_img, only_camera=None):
    if only_camera is not None:
        img = Vision.CamerasUnwarper.getImgRegionByCameraNo(original_img, only_camera)
        h, w = img.shape[:2]
        newcameramtx, _ = cv2.getOptimalNewCameraMatrix(mtxs[only_camera - 1], dists[only_camera - 1], (w, h), 1,
                                                        (w, h))
        dst = cv2.undistort(img, mtxs[only_camera - 1], dists[only_camera - 1], None, newcameramtx)
        return dst
    else:
        for camera_no in range(0, 4):
            img = Vision.CamerasUnwarper.getImgRegionByCameraNo(original_img, camera_no + 1)
            h, w = img.shape[:2]
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
        return dsts


def live_unwarp(only_camera=None):
    cam = cv2.VideoCapture(0)
    set_res(cam, 1920, 1080)
    mtxs = np.load("Vision/mtxs.npy")
    dists = np.load("Vision/dists.npy")
    while True:
        ret_val, img = cam.read()
        img = unwarp_image(mtxs, dists, img, only_camera)
        cv2.imshow('my webcam', img)
        cv2.waitKey(100)
