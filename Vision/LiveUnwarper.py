import cv2
import Vision.CamerasUnwarper
import numpy as np
import imutils


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

    # Unwarp all 4 cameras and merge them into a single image in real time
    def live_unwarp(self):
        cam = cv2.VideoCapture(0)
        set_res(cam, 1920, 1080)
        i = 1
        while True:
            _, img = cam.read()
            if i > 20:
                unwarp_img = self.unwarp_image(img)
                merged_img = self.stitch_one_two_three_and_four(img)
                if merged_img is not None:
                    cv2.imshow('1. raw', cv2.resize(img, (0,0), fx=0.33, fy=0.33))
                    cv2.imshow('2. unwarped', cv2.resize(unwarp_img, (0,0), fx=0.5, fy=0.5))
                    cv2.imshow('3. merged', merged_img)
                    k = cv2.waitKey(1)
            i += 1

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

    def stitch_one_and_two(self, img):
        img_1 = self.camera_one_segment(img)
        img_2 = self.camera_two_segment(img)
        new_img = self.stitcher.stitch((img_1, img_2), self.H_c1_and_c2)
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

    def stich_three_and_four(self, img):
        img_1 = self.camera_three_segment(img)
        img_2 = self.camera_four_segment(img)
        img_2 = cv2.resize(img_2, (0, 0), fx=0.903846154, fy=0.903846154)
        img_1 = np.concatenate(
            (np.zeros((img_2.shape[0] - img_1.shape[0], img_1.shape[1], 3), dtype=np.uint8), img_1), axis=0)
        new_img = np.concatenate((img_1, img_2), axis=1)
        return new_img

    def stitch_one_two_three_and_four(self, img):
        # Get the top of the image
        img_1 = self.stitch_one_and_two(img)
        # Take a portion of top image to line walls up with bottom one
        img_1 = img_1[:, 13:326, :]
        # Get the bottom of the image
        img_2 = self.stich_three_and_four(img)
        # Add to the width of top image to make it the same width as the bottom one
        img_1 = np.concatenate(
            (img_1, np.zeros((img_1.shape[0], img_2.shape[1] - img_1.shape[1], 3), dtype=np.uint8)), axis=1)
        # Overlap between top and bottom image, so we say we want the bottom one to overlap the top one by 45 pixels
        amount_to_move_bottom_img_up = 45
        # Create a copy of the bottom image with it aligned to its desired new position, set space which top image will take up as black
        img_2_merge_canvas = np.zeros((img_1.shape[0] + img_2.shape[0] - amount_to_move_bottom_img_up, img_2.shape[1], 3), dtype=np.uint8)
        img_2_merge_canvas[img_1.shape[0] - amount_to_move_bottom_img_up:
                           img_1.shape[0] + img_2.shape[0] - amount_to_move_bottom_img_up, :, :] = img_2
        # Add to the top image space for the non-overlapping part of the bottom image
        img_1 = np.concatenate((img_1, np.zeros((img_2.shape[0] - amount_to_move_bottom_img_up, img_1.shape[1], 3), dtype=np.uint8)), axis=0)
        # For all pixels in the top image that will be overlapped by the bottom image, we set their value to 0
        mask = np.where(img_2_merge_canvas != [0, 0, 0])
        img_1[mask] = np.zeros(img_1.shape, dtype=np.uint8)[mask]
        # New top and bottom image are then the same size, and each respective pixel is black in one image, and the desired colour
        # in the other, meaning we can just add the matrices values and return the result for our merged image
        img_1 += img_2_merge_canvas
        return img_1


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

    def stitch(self, images, H):
        (imageB, imageA) = images

        result = cv2.warpPerspective(imageA, H,
                                     (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
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
