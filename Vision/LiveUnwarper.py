#!/usr/bin/env python3
import glob

import cv2
import imutils
import numpy as np
import math

import Vision.CamerasUnwarper
from Vision import Gridify
from Vision.Finder import RobotFinder
from pathfinding.graph import getInstructionsFromGrid

from matplotlib import pyplot as plt

import paho.mqtt.client as mqtt

import Vision.firebase_interaction as fbi

def set_res(cap, x, y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


class Unwarper:

    def __init__(self):
        # Note for cameras 3 and 4 we use the calibration matrices of camera 1, this is because the calibration matrix
        # produced for it actually performed better than those trained for cameras 3 and 4
        self.mtxs = np.load("Vision/mtxs.npy")
        self.mtxs[2] = self.mtxs[0]
        self.mtxs[3] = self.mtxs[0]
        self.dists = np.load("Vision/dists.npy")
        self.dists[2] = self.dists[0]
        self.dists[3] = self.dists[0]
        self.H_c1_and_c2 = np.load("Vision/H_c1_and_c2.npy")
        self.stitcher = Stitcher()
        self.errors = self.where_error(
            [(np.load("Vision/lhs_adj_errors.npy"), [125, 7]), (np.load("Vision/rhs_adj_errors.npy"), [104, 140])])
        self.robot_finder = RobotFinder()

        self.mqtt=mqtt.Client("PathCommunicator")
        self.mqtt.on_connect=self.on_connect
        self.mqtt.connect("129.215.202.200")
        self.overhead_image = None
        fbi.start_script(self)
        self.path = None
        self.overlap_area = None

    def get_overhead_image(self):
        return self.overhead_image

    # Give a numpy array of erroneous pixels, return the location of pixels adjacent to them
    # error_descriptions is a list of tuples, the first element of each tuple should be another tuple in the format
    # output by np.where, the second argument of each tuple should be a list containing [y,x] where each corresponds to the
    # arguments in np.where(arr[y:i,x:j==some_condition)

    def where_error(self, error_descritpions):
        # Find the locations of the errors in the image
        errors = []
        if type(error_descritpions) != list:
            error_descritpions = list(error_descritpions)
        for error_descritpion in error_descritpions:
            relative_y_pos = error_descritpion[1][0]
            relative_x_pos = error_descritpion[1][1]
            error_array = error_descritpion[0]
            for i in range(0, error_array[0].shape[0], 3):
                errors.append((int(error_array[0][i]) + relative_y_pos, int(error_array[1][i]) + relative_x_pos))
        # Create a list of the pixels adjacent to the errors
        adjacent_to_error = []
        for error in errors:
            for i in [error[0] - 1, error[0] + 1]:
                for j in [error[1] - 1, error[1] + 1]:
                    if (i, j) not in errors and (i, j) not in adjacent_to_error:
                        adjacent_to_error.append((i, j))
        errors += adjacent_to_error
        # Convert the errors and pixels adjacent back into a list of coordinates we can use to address them by index
        x_errors = []
        y_errors = []
        z_errors = []
        for error in errors:
            for z in range(0, 3):
                x_errors.append(error[0])
                y_errors.append(error[1])
                z_errors.append(z)
        return np.array(x_errors), np.array(y_errors), np.array(z_errors)

    # Take CCTV view and unwarp each camera, returning result, if only_camera is set to 0,1,2, or 3, it will unwarp only
    # the respective camera
    def unwarp_image(self, original_img, only_camera=None):
        if only_camera is not None:

            img = Vision.CamerasUnwarper.getImgRegionByCameraNo(original_img, only_camera)

            h, w = img.shape[:2]
            newcameramtx, _ = cv2.getOptimalNewCameraMatrix(self.mtxs[only_camera - 1], self.dists[only_camera - 1],
                                                            (w, h), 1,
                                                            (w, h))
            dst = cv2.undistort(img, self.mtxs[only_camera - 1], self.dists[only_camera - 1], None, newcameramtx)
            return dst
            # cv2.imshow("origin", img)
            # cv2.imshow("processed", img_thresh)
            # cv2.waitKey(1)
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

    def find_path(self, graph, to, frm):
        if frm[0] is not None:
            if self.path is None:
                _, self.path, _, _ = getInstructionsFromGrid(graph, frm, to)
            else:
                path_broken = False
                closest = float('inf')
                for node in self.path:
                    x, y = node.pos
                    if abs(x - frm[0]) + abs(y - frm[1]) < closest:
                        closest = abs(x - frm[0]) + abs(y - frm[1])
                    if graph[y][x] == 1:
                        path_broken = True
                        break
                if path_broken or closest > 0:
                    _, self.path, _, _ = getInstructionsFromGrid(graph, frm, to)
        else:
            self.path = None

    # Unwarp all 4 cameras and merge them into a single image in real time
    def live_unwarp(self):
        cam = cv2.VideoCapture(0)
        set_res(cam, 1920, 1080)
        i = 1
        counter = 0
        
        while True & counter < 100:
            _, img = cam.read()
            if i > 20:
                unwarp_img = self.unwarp_image(img)
                merged_img = self.stitch_one_two_three_and_four(img)
                self.overhead_image = merged_img
                thresh_merged_img = self.stitch_one_two_three_and_four(img, thresh=True)
                if merged_img is not None:
                    cv2.imshow('1. raw', cv2.resize(img, (0, 0), fx=0.33, fy=0.33))
                    cv2.imshow('2. unwarped', cv2.resize(unwarp_img, (0, 0), fx=0.5, fy=0.5))
                    cv2.imshow('3. merged', merged_img)
                    cv2.imshow('4. thresholded', thresh_merged_img)
                    object_graph = Gridify.convert_thresh_to_map(thresh_merged_img, shift_amount=6, visualize=True)
                    search_graph = Gridify.convert_thresh_to_map(thresh_merged_img, shift_amount=6, cell_length=6)
                    robot_pos = self.robot_finder.find_robot(merged_img)
                    if robot_pos[0] is not None:
                        self.mqtt.publish("pos", "%f,%f" % (robot_pos[0], robot_pos[1]))
                        robot_pos = tuple([int(math.floor(i / 6)) for i in robot_pos])
                        object_graph[robot_pos[1] - 2:robot_pos[1] + 2, robot_pos[0] - 2:robot_pos[0] + 2] = np.array(
                            [0, 0, 255], dtype=np.uint8)
                        for j in range(robot_pos[1] - 2, robot_pos[1] + 3):
                            for k in range(robot_pos[0] - 2, robot_pos[0] + 3):
                                search_graph[j][k] = 0
                    cv2.imshow("search graph", np.array(search_graph, dtype=np.uint8) * np.uint8(255))
                    self.find_path(search_graph, (45, 9), robot_pos)
                    if self.path is not None:
                        for node in self.path:
                            x, y = node.pos
                            object_graph[y][x] = np.array([255, 0, 0], dtype=np.uint8)
                    cv2.imshow('6. object graph', cv2.resize(object_graph, (0, 0), fx=6, fy=6))
                    cv2.waitKey(1)
            i += 1

    def static_unwarp(self, photo_path="Vision/Calibrated Pictures/*.jpg"):
        images = glob.glob(photo_path)

        for fname in images:
            img = cv2.imread(fname)
            unwarp_img = self.unwarp_image(img)
            merged_img = self.stitch_one_two_three_and_four(img)
            thresh_merged_img = self.stitch_one_two_three_and_four(img, thresh=True)
            grid = Gridify.convert_thresh_to_map(thresh_merged_img)
            if merged_img is not None:
                cv2.imshow('1. raw', cv2.resize(img, (0, 0), fx=0.33, fy=0.33))
                cv2.imshow('2. unwarped', cv2.resize(unwarp_img, (0, 0), fx=0.5, fy=0.5))
                cv2.imshow('3. merged', merged_img)
                cv2.imshow('4. thresholded', thresh_merged_img)
                cv2.waitKey()

    def camera_one_segment(self, original_img):
        unwarped_camera = self.unwarp_image(original_img, 1)
        x_lower_bound = 360
        x_upper_bound = 540
        y_lower_bound = 120
        y_upper_bound = 255
        segment = unwarped_camera[y_lower_bound:y_upper_bound, x_lower_bound:x_upper_bound]
        return segment

    def camera_two_segment(self, original_img):
        unwarped_camera = self.unwarp_image(original_img, 2)
        x_lower_bound = 25
        x_upper_bound = 400
        y_lower_bound = 200
        y_upper_bound = 390
        segment = unwarped_camera[y_lower_bound:y_upper_bound, x_lower_bound:x_upper_bound]
        return segment

    def stitch_one_and_two(self, img, thresh=False):
        img_1 = self.camera_one_segment(img)
        img_2 = self.camera_two_segment(img)
        new_img = self.stitcher.stitch((img_1, img_2), self.H_c1_and_c2, thresh=thresh)
        return new_img

    def camera_three_segment(self, original_img):
        unwarped_camera = self.unwarp_image(original_img, 3)
        x_lower_bound = 379
        x_upper_bound = 492
        y_lower_bound = 90
        y_upper_bound = 210
        segment = unwarped_camera[y_lower_bound:y_upper_bound, x_lower_bound:x_upper_bound]
        return segment

    def camera_four_segment(self, original_img):
        unwarped_camera = self.unwarp_image(original_img, 4)
        x_lower_bound = 275
        x_upper_bound = 505
        y_lower_bound = 78
        y_upper_bound = 211
        segment = unwarped_camera[y_lower_bound:y_upper_bound, x_lower_bound:x_upper_bound]
        return segment

    def stich_three_and_four(self, img, thresh=False):
        img_1 = self.camera_three_segment(img)
        img_2 = self.camera_four_segment(img)
        img_2 = cv2.resize(img_2, (0, 0), fx=0.903846154, fy=0.903846154)
        if thresh:
            img_1 = cv2.cvtColor(cv2.Canny(img_1, 100, 255), cv2.COLOR_GRAY2RGB)
            img_2 = cv2.cvtColor(cv2.Canny(img_2, 100, 255), cv2.COLOR_GRAY2RGB)
        img_1 = np.concatenate(
            (np.zeros((img_2.shape[0] - img_1.shape[0], img_1.shape[1], 3), dtype=np.uint8), img_1), axis=0)
        new_img = np.concatenate((img_1, img_2), axis=1)
        return new_img

    def stitch_one_two_three_and_four(self, img, thresh=False):
        # Get the top of the image
        img_1 = self.stitch_one_and_two(img, thresh=thresh)
        # Take a portion of top image to line walls up with bottom one
        img_1 = img_1[:, 13:326, :]
        # Get the bottom of the image
        img_2 = self.stich_three_and_four(img, thresh=thresh)
        # Add to the width of top image to make it the same width as the bottom one
        img_1 = np.concatenate(
            (img_1, np.zeros((img_1.shape[0], img_2.shape[1] - img_1.shape[1], 3), dtype=np.uint8)), axis=1)
        # Overlap between top and bottom image, so we say we want the bottom one to overlap the top one by 45 pixels
        amount_to_move_bottom_img_up = 45
        # Create a copy of the bottom image with it aligned to its desired new position, set space which top image will take up as black
        img_2_merge_canvas = np.zeros(
            (img_1.shape[0] + img_2.shape[0] - amount_to_move_bottom_img_up, img_2.shape[1], 3), dtype=np.uint8)
        img_2_merge_canvas[img_1.shape[0] - amount_to_move_bottom_img_up:
                           img_1.shape[0] + img_2.shape[0] - amount_to_move_bottom_img_up, :, :] = img_2
        # Add to the top image space for the non-overlapping part of the bottom image
        img_1 = np.concatenate(
            (img_1, np.zeros((img_2.shape[0] - amount_to_move_bottom_img_up, img_1.shape[1], 3), dtype=np.uint8)),
            axis=0)
        # For all pixels in the top image that will be overlapped by the bottom image, we set their value to 0
        if not thresh or self.overlap_area is None:
            self.overlap_area = np.where(img_2_merge_canvas != [0, 0, 0])
            if thresh:
                print("WARNING: self.overlap_area undefined, this is likely due to not merging the colour image first")
        img_1[self.overlap_area] = np.zeros(img_1.shape, dtype=np.uint8)[self.overlap_area]
        # New top and bottom image are then the same size, and each respective pixel is black in one image, and the desired colour
        # in the other, meaning we can just add the matrices values and return the result for our merged image
        img_1 += img_2_merge_canvas

        if thresh:
            # Canny edge detection detects the edge of the images as edges, which can lead to false positives for objects
            # in the vision system. To get around this we recorded the errenous pixels positions in one frame. We then marked
            # all adjacent pixels to this errenous pixtures as well (as the errors can move around slightly). self.errors
            # lists the positions of all these pixels, and we set them to black to get rid of the false positives.
            img_1[self.errors] = np.uint8(0)
            # There were a few pixels that were still errenously white after the postprocessing above, so we manual
            # set these to black
            img_1[132, 67] = np.array([0, 0, 0], dtype=np.uint8)
            img_1[133, 87] = np.array([0, 0, 0], dtype=np.uint8)
            img_1[134, 88] = np.array([0, 0, 0], dtype=np.uint8)

        return img_1
    def on_connect(client,userdata,flags,rc):
        print("connected")

# The stitcher class is a varitation of the one found in the tutorial here https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/

class Stitcher:
    def __init__(self):
        # determine if we are using OpenCV v3.X
        self.isv3 = imutils.is_cv3()

    def find_h(self, images, ratio=0.75, reprojThresh=4.0):
        (imageB, imageA) = images
        # unpack the images, then detect keypoints and extract
        # local invariant descriptors from them
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)

        # match features between the two images
        M = self.matchKeypoints(kpsA, kpsB,
                                featuresA, featuresB, ratio, reprojThresh)

        # if the match is None, then there aren't enough matched
        # keypoints to create a panorama
        if M is None:
            return None, None
        # otherwise, apply a perspective warp to stitch the images
        # together
        (matches, H, status) = M

        if H is None:
            return None, None

        return (self.stitch(images, H), H)

    def stitch(self, images, H, thresh=False):
        (imageB, imageA) = images

        result = cv2.warpPerspective(imageA, H,
                                     (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))

        if thresh:
            result = cv2.cvtColor(cv2.Canny(result, 100, 255), cv2.COLOR_GRAY2RGB)
            imageB = cv2.cvtColor(cv2.Canny(imageB, 100, 255), cv2.COLOR_GRAY2RGB)

        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        # return the stitched image
        return result

    def detectAndDescribe(self, image):
        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # check to see if we are using OpenCV 3.X
        if self.isv3:
            # detect and extract features from the image
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(image, None)

        # otherwise, we are using OpenCV 2.4.X
        else:
            # detect keypoints in the image
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)

            # extract features from the image
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)

        # convert the keypoints from KeyPoint objects to NumPy
        # arrays
        kps = np.float32([kp.pt for kp in kps])

        # return a tuple of keypoints and features
        return (kps, features)

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
                       ratio, reprojThresh):
        # compute the raw matches and initialize the list of actual
        # matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []

        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each
            # other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        # computing a homography requires at least 4 matches
        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
                                             reprojThresh)

            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (matches, H, status)

        # otherwise, no homograpy could be computed
        return None

    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # initialize the output visualization image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB

        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the keypoint was successfully
            # matched
            if s == 1:
                # draw the match
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

        # return the visualization
        return vis

