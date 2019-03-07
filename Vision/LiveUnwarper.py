#!/usr/bin/env python3
import glob

import copy

import cv2
import imutils
import numpy as np
import paho.mqtt.client as mqtt
import random
import math

import Vision.CamerasUnwarper
import Vision.firebase_interaction as fbi
from Vision import Gridify
from Vision.Finder import RobotFinder
from pathfinding.graph import getInstructionsFromGrid

global robot_moving
robot_moving = False
global robot_rotating
robot_rotating = False
global global_robot_pos
global_robot_pos = None
global robot_angle
robot_angle = None
global robot_direction
robot_direction = None
global robot_target
robot_target = None
global expected_end_angle
expected_end_angle = None
global insts
insts = []
global square_length
square_length = None
global goal_pos
goal_pos = None
global search_graph
search_graph = None
global path
path = None
global cell_length
cell_length = 30
global shift_amount
shift_amount = 4

# QA vars
global start_pos
start_pos = None
global original_goal
original_goal = None


def set_res(cap, x, y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def on_connect(client, userdata, flags, rc):
    print("connected")
    client.subscribe("finish-instruction")
    client.subscribe("battery-update")


def check_on_path(graph, to, frm_dec):
    print(1)
    try:
        global path
        global insts

    except Exception as e:
        print(e.message, e.args)
        sys.exit()
        raise


def count_diff_target(start_pos, robot_pos, robot_target):
    f = open("Vision/QAResults/diff_target.txt", "a")
    try:
        f.write(
            "%s %s %s (%s,%s)\n" % (
                start_pos, robot_pos, robot_target, robot_pos[0] - robot_target[0], robot_pos[1] - robot_target[1]))
        f.close()
    except:
        f.close()

def convert_orientation_inst_to_rotation(next_inst):
    if next_inst == "u":
        expected_end_angle = 0
    elif next_inst == "r":
        expected_end_angle = 90
    elif next_inst == "d":
        expected_end_angle = 180
    elif next_inst == "l":
        expected_end_angle = 270
    angle_to_turn = (expected_end_angle - robot_angle) % 360
    if angle_to_turn > 180:
        angle_to_turn -= 360
    next_inst = "r,%s" % round(angle_to_turn)
    return next_inst

def on_message(client, userdata, msg):
    global robot_moving
    global robot_rotating
    global robot_angle
    global expected_end_angle
    global robot_direction
    global robot_target
    global global_robot_pos
    global search_graph
    global goal_pos
    global path
    global insts
    global start_pos
    global original_goal
    print("HEARD DONE")
    try:
        if msg.topic == "finish-instruction":
            robot_was_moving = robot_moving
            robot_was_rotating = robot_rotating
            robot_moving = False
            robot_rotating = False
            if robot_was_moving:
                count_diff_target(start_pos, global_robot_pos, original_goal)
                path_broken = False
                closest = float('inf')
                print(path)
                grid_robot_pos = tuple([(i - (cell_length / 2)) / shift_amount for i in global_robot_pos])
                print("SHAPE: (%s, %s)" % (len(search_graph), len(search_graph[0])))
                for node in path:
                    x, y = node.pos
                    # Add 0.5 as we want robot to be in centre of each square
                    if math.sqrt((x + 0.5 - grid_robot_pos[0]) ** 2 + (y + 0.5 - grid_robot_pos[1]) ** 2) < closest:
                        closest = abs(x - grid_robot_pos[0]) + abs(y - grid_robot_pos[1])

                    print("QUERYING: (%s, %s)" % (y, x))
                    if search_graph[y][x] == 1:
                        path_broken = True
                        break
                print(str(grid_robot_pos))
                print("CLOSEST IS %s" % closest)
                if path_broken or closest > 3:
                    frm = tuple([round(i) for i in grid_robot_pos])
                    _, path, _, insts = getInstructionsFromGrid(search_graph, target=goal_pos, start=frm,
                                                                upside_down=True)
            if robot_was_rotating:
                if abs(robot_angle - expected_end_angle) > 5:
                    robot_rotating = True
                    angle_to_turn = (expected_end_angle - robot_angle) % 360
                    if angle_to_turn > 180:
                        angle_to_turn -= 360
                    client.publish("start-instruction", "%s,%s" % ("r", round(angle_to_turn)), qos=2)
                    return
            # robot_direction = 0 if facing south, 1 if facing west, 2 if facing north, 3 if facing east
            robot_direction = round((int(robot_angle) % 360) / 90)
            if len(insts) != 0:
                next_inst = insts.pop(0)
                if type(next_inst) is not tuple:
                    robot_rotating = True
                    client.publish("start-instruction", convert_orientation_inst_to_rotation(next_inst), qos=2)
                else:
                    if next_inst[0] == "m":
                        print("pos: %s, square_length: %s" % (str(global_robot_pos), str(square_length)))
                        distance = next_inst[1] * square_length
                        robot_target = list(global_robot_pos)
                        # up
                        if robot_direction == 0:
                            robot_target[1] -= distance
                        # right
                        if robot_direction == 1:
                            robot_target[0] += distance
                        # down
                        if robot_direction == 2:
                            robot_target[1] += distance
                        # left
                        if robot_direction == 3:
                            robot_target[0] -= distance
                        robot_target = tuple(robot_target)
                        robot_moving = True
                    if next_inst[0] == "r":
                        robot_rotating = True
                    start_pos = global_robot_pos
                    original_goal = robot_target
                    client.publish("start-instruction", "%s,%s" % next_inst, qos=2)
                print("TOLD TO DO %s" % str(next_inst))
    except Exception as e:
        print(e)
        raise
        sys.exit()
    if (msg.topic == "battery-update"):
        print("sending battery update to firebase")
        # decode status and send it to db using fbi method
        new_battery_status = msg.payload.decode()
        fbi.update_battery_status_in_db(new_battery_status)


print("ON MESSAGE FINISHED")


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

        self.mqtt = mqtt.Client("PathCommunicator")
        self.mqtt.on_connect = on_connect
        self.mqtt.on_message = on_message
        self.mqtt.connect("129.215.3.65")
        self.mqtt.loop_start()
        self.overhead_image = None
        fbi.start_script(self)
        self.overlap_area = None

        # TESTING VARIABLES
        self.visibility = []

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

    def determine_new_path(self, graph, to, frm):
        global insts
        global path
        global robot_rotating
        _, path, _, insts = getInstructionsFromGrid(graph, target=goal_pos, start=frm, upside_down=True)
        print(str(insts))
        if not robot_rotating and not robot_moving and insts != []:
            next_inst = insts.pop(0)
            next_inst = convert_orientation_inst_to_rotation(next_inst)
            self.mqtt.publish("start-instruction", next_inst, qos=2)
            robot_rotating = True
            print("TOLD TO DO %s" % str(next_inst))

    def check_robot_at_target(self, robot_pos):
        global robot_target
        global robot_moving
        global robot_direction
        global square_length
        # print("ROBOT POS IS %s AND TARGET POS IS %s" % (str(robot_pos), str(robot_target)))
        if robot_moving and robot_pos[0] is not None and robot_pos[1] is not None:
            # up
            if robot_direction == 0:
                dist_to_target = robot_pos[1] - robot_target[1]
            # right
            elif robot_direction == 1:
                dist_to_target = robot_target[0] - robot_pos[0]
            # down
            elif robot_direction == 2:
                dist_to_target = robot_target[1] - robot_pos[1]
            # left
            elif robot_direction == 3:
                dist_to_target = robot_pos[0] - robot_target[0]
            if dist_to_target < 16:
                self.mqtt.publish("start-instruction", "s", qos=2)
                print("TOLD TO STOP")
                if len(insts) == 0:
                    pass
                    # self.set_random_target(robot_pos)

    def set_random_target(self, robot_pos):
        global goal_pos
        possible_goals = [(x, y) for x in range(20, 39) for y in range(6, 18)] + [(x, y) for x in range(5, 39) for y in
                                                                                  range(17, 30)] + [(x, y) for x in
                                                                                                    range(38, 44) for y
                                                                                                    in range(10, 30)]
        goal_pos = random.choice(possible_goals)
        self.determine_new_path(search_graph, goal_pos, tuple([round(i) for i in robot_pos]))

    def count_visibility(self, visible):
        if visible:
            self.visibility.append(1)
        else:
            self.visibility.append(0)
        if len(self.visibility) == 100:
            count = sum(self.visibility)
            # Writes out of the last 100 frames the number of times how many of them the spot was visible
            f = open("Vision/QAResults/spot_visibility_count_out_of_100.txt", "a")
            try:
                f.write("%s\n" % count)
                f.close()
            except:
                f.close()
            self.visibility = []

    def find_path(self, graph, to, frm_dec):
        global insts
        global path
        global search_graph
        global global_robot_pos
        if frm_dec[0] is not None:
            if path is None:
                self.determine_new_path(graph, to, tuple([round(i) for i in frm_dec]))
            else:
                '''
                path_broken = False
                for node in path:
                    x, y = node.pos
                    if search_graph[y][x] == 1:
                        path_broken = True
                        break
                if path_broken:
                    self.determine_new_path(graph, to, tuple([round(i) for i in frm_dec]))
                '''

    # Unwarp all 4 cameras and merge them into a single image in real time

    def live_unwarp(self):
        global goal_pos
        global search_graph
        global global_robot_pos
        global robot_angle
        '''
        possible_goals = [(x, y) for x in range(20, 39) for y in range(6, 18)] + [(x, y) for x in range(5, 39) for y in
                                                                                  range(17, 30)] + [(x, y) for x in
                                                                                                    range(38, 44) for y
                                                                                                    in range(10, 30)]
        goal_pos = random.choice(possible_goals)
        '''
        count = 6
        # (23, 6)
        # goal_pos = (9, 28)
        goal_pos = (30, 10)
        cam = cv2.VideoCapture(0)
        set_res(cam, 1920, 1080)
        i = 1
        visible = 0
        global square_length
        square_length = shift_amount
        while True:
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
                    robot_pos_dec, robot_angle = self.robot_finder.find_robot(merged_img)
                    if global_robot_pos is not None:
                        thresh_merged_img[round(global_robot_pos[1] - 20):round(global_robot_pos[1] + 20),
                        round(global_robot_pos[0] - 20):round(global_robot_pos[0] + 20), :] = np.zeros((40, 40, 3),
                                                                                                       dtype=np.uint8)
                    if robot_angle is not None:
                        cv2.imshow('4. thresholded', thresh_merged_img)
                    object_graph = Gridify.convert_thresh_to_map(thresh_merged_img, shift_amount=shift_amount,
                                                                 cell_length=cell_length,
                                                                 visualize=True)
                    search_graph = Gridify.convert_thresh_to_map(thresh_merged_img, shift_amount=shift_amount,
                                                                 cell_length=cell_length)
                    search_graph_copy = copy.deepcopy(search_graph)
                    if robot_pos_dec[0] is not None and robot_pos_dec[1] is not None:
                        global_robot_pos = robot_pos_dec
                    self.count_visibility(robot_pos_dec[0] is not None)
                    self.check_robot_at_target(robot_pos_dec)
                    if robot_pos_dec[0] is not None:
                        robot_pos_dec = tuple([(i - (cell_length / 2)) / shift_amount for i in robot_pos_dec])
                        '''
                        if abs(robot_pos[0] - last_robot_pos_sent[0]) > 0.1 or abs(
                                robot_pos[1] - last_robot_pos_sent[1]) > 0.1:
                            self.mqtt.publish("pos", "%f,%f" % (robot_pos[0], robot_pos[1]), qos=2)
                            last_robot_pos_sent = robot_pos
                            print("sending robot position: (%f,%f)" % (robot_pos))
                        '''
                        robot_pos = tuple([round(i) for i in robot_pos_dec])

                        object_graph[robot_pos[1] - 3:robot_pos[1] + 3, robot_pos[0] - 3:robot_pos[0] + 3] = np.array(
                            [0, 0, 255], dtype=np.uint8)
                        object_graph[robot_pos[1], robot_pos[0]] = np.array([0, 0, 0], dtype=np.uint8)
                        # for j in range(robot_pos[1] - 4, robot_pos[1] + 5):
                        #    for k in range(robot_pos[0] - 4, robot_pos[0] + 5):
                        #        if k >= 0 and j >= 0 and j < len(search_graph) and k < len(search_graph[0]):
                        #            pass
                        #            # search_graph[j][k] = 0
                        # search_graph[robot_pos[1]][robot_pos[0]] = 0
                        self.find_path(search_graph, goal_pos, robot_pos_dec)

                    # cv2.imshow("search graph", np.array(search_graph, dtype=np.uint8) * np.uint8(255))
                    # print(path)
                    # print(insts)
                    # time.sleep(100000)
                    cv2.imshow("search graph", np.array(search_graph_copy, dtype=np.uint8) * 255)
                    if path is not None:
                        for node in path:
                            x, y = node.pos
                            object_graph[y][x] = np.array([255, 0, 0], dtype=np.uint8)
                        if len(path) != 0:
                            object_graph[y][x] = np.array([0, 255, 0], dtype=np.uint8)
                    cv2.imshow('6. object graph', object_graph)  # cv2.resize(object_graph, (0, 0), fx=6, fy=6))
                    if cv2.waitKey(1) == 48:
                        cv2.imwrite("Vision/record_output/%s.jpg" % count, merged_img)
                        count += 1
                    # time.sleep(0.1)
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
