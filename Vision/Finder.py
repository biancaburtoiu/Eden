import numpy as np
import cv2
import glob
import requests


class RobotFinder:

    def __init__(self):
        # Input colour in RGB format, and then array order is flipped (using [::-1]) to give BGR format,
        # as that is the format cv2 uses for colour

        self.lower = np.array([180, 70, 120])[::-1]
        self.upper = np.array([255, 220, 240])[::-1]

        # Set the parameters for the simple blob detector and create it

        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 10 * 10
        params.maxArea = 20 * 20
        params.filterByCircularity = True
        params.minCircularity = 0.7
        params.maxCircularity = 1
        params.filterByInertia = False
        params.filterByColor = False
        params.filterByConvexity = False

        self.robot_detector = cv2.SimpleBlobDetector_create(params)

    # Given the merged image, find the position of the pink circle that gives us the position of the robot

    def find_robot(self, img, return_image_pos=False):

        # Threshold the image to the specified BGR range

        thresh = cv2.inRange(img, self.lower, self.upper)

        # Errode the image to get rid of noise in the thresholded image

        kernel = np.ones((2, 2), np.uint8)
        thresh_img_errode = cv2.erode(thresh, kernel, iterations=1)

        # Invert the colour scheme, as our blobs are white and simple blob detector looks for black blobs

        inverted_thresh_img = 255 - thresh_img_errode

        # Find the blobs

        keypoints = self.robot_detector.detect(inverted_thresh_img)

        if len(keypoints) > 0:

            if len(keypoints) > 1:
                print("ROBOT FINDER FOUND MORE THAN ONE POSSIBLE POSITION FOR THE ROBOT, USING FIRST FOUND")

            # We assume there will only ever be one blob, as the simple blob detector filters the blobs based on their
            # circularity and area. So we can say the robot is at the centre of the first blob

            robot_pos = keypoints[0].pt

            if return_image_pos:
                # Draw the blob onto the thresholded image to make it easier to understand where it is
                thresh_robot = cv2.drawKeypoints(inverted_thresh_img, keypoints, np.array([]), (0, 0, 255),
                                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                return robot_pos, thresh_robot
            else:
                return robot_pos

        elif len(keypoints) == 0:
            print("ROBOT FINDER COULD NOT FIND THE ROBOT, RETURNING POSITION AS NONE")

            robot_pos = (None, None)

            if return_image_pos:
                return inverted_thresh_img, robot_pos
            else:
                return robot_pos

    # Given a set of images, find the robot in them and display the result

    def view_thresh_robot(self, path="Vision/Robot ID Pictures/*_merged.jpg"):
        images_paths = glob.glob(path)

        for path in images_paths:
            img = cv2.imread(path)
            cv2.imshow("Raw", img)
            robot_pos, thresh_robot = self.find_robot(img, return_found_pos=True)
            cv2.imshow("Thresh Robot", thresh_robot)
            cv2.waitKey()

def find_plant(img):
    params = {
        'features': 'OBJECT_LOCALIZATION'
    }
