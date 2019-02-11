import numpy as np
import cv2
import glob


class FindRobot:

    def __init__(self):

        # Input colour in RGB format, and then array order is flipped (using [::-1]) to give BGR format,
        # as that is the format cv2 uses for colour

        self.lower = np.array([180, 70, 120])[::-1]
        self.upper = np.array([255, 220, 240])[::-1]

    def view_thresh_robot(self):
        images_paths = glob.glob("Vision/Robot ID Pictures/*_merged.jpg")

        for path in images_paths:
            img = cv2.imread(path)
            thresh = cv2.inRange(img, self.lower, self.upper)
            cv2.imshow("Raw", img)
            cv2.imshow("Thresh", thresh)
            cv2.waitKey()
