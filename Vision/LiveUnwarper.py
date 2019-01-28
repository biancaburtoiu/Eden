import cv2
import Vision.CamerasUnwarper
import numpy as np


def set_res(cap, x, y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


class Unwarper:

    def __init__(self):
        self.mtxs = np.load("Vision/mtxs.npy")
        self.dists = np.load("Vision/dists.npy")

    def unwarp_image(self, original_img, only_camera=None):
        if only_camera is not None:
            img = Vision.CamerasUnwarper.getImgRegionByCameraNo(original_img, only_camera)
            h, w = img.shape[:2]
            newcameramtx, _ = cv2.getOptimalNewCameraMatrix(self.mtxs[only_camera - 1], self.dists[only_camera - 1],
                                                            (w, h), 1,
                                                            (w, h))
            dst = cv2.undistort(img, self.mtxs[only_camera - 1], self.dists[only_camera - 1], None, newcameramtx)
            return dst
        else:
            for camera_no in range(0, 4):
                img = Vision.CamerasUnwarper.getImgRegionByCameraNo(original_img, camera_no + 1)
                h, w = img.shape[:2]
                newcameramtx, _ = cv2.getOptimalNewCameraMatrix(self.mtxs[camera_no], self.dists[camera_no], (w, h), 1,
                                                                (w, h))
                dst = cv2.undistort(img, self.mtxs[camera_no], self.dists[camera_no], None, newcameramtx)
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

    def live_unwarp(self, only_camera=None):
        cam = cv2.VideoCapture(0)
        set_res(cam, 1920, 1080)
        while True:
            ret_val, img = cam.read()
            img = self.unwarp_image(img, only_camera)
            #img = self.camera_two_segment(img)
            cv2.imshow('my webcam', img)
            cv2.waitKey(100)

    def camera_one_segment(self, original_img):
        unwarped_camera_one = self.unwarp_image(original_img, 1)
        x_lower_bound = 360
        x_upper_bound = 490
        y_lower_bound = 120
        y_upper_bound = 250
        segment = unwarped_camera_one[y_lower_bound:y_upper_bound, x_lower_bound:x_upper_bound]
        return segment

    def camera_two_segment(self, original_img):
        unwarped_camera_one = self.unwarp_image(original_img, 2)
        x_lower_bound = 125
        x_upper_bound = 400
        y_lower_bound = 200
        y_upper_bound = 360
        segment = unwarped_camera_one[y_lower_bound:y_upper_bound, x_lower_bound:x_upper_bound]
        return segment
