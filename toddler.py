# import the necessary packages
#!/usr/bin/env python
from __future__ import division
from __future__ import absolute_import
import numpy as np
import time
import imutils
import paho.mqtt.client as mqtt
import cv2
from itertools import izip
from picamera import PiCamera

import argparse

import glob

from enum import Enum




template = cv2.imread("/home/student/logo.jpg")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
left_time=0
rigt_time=0
count=0
camera=PiCamera()
camera.resolution=(360,240)
location= np.zeros(7)
logo_number=0

def start_capture():
    curt=time.time()
    bf_wr =time.time()
    camera.capture("image.jpg")
    image= cv2.imread("/home/student/image.jpg")
    cv2.imshow('Camera',image)
    af_wr = time.time()
    time.sleep(0.05)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None
    all_found = None
    final_result = None
    global location
    location = np.zeros(7)




    # loop over the scales of the image
    for scale in np.linspace(0.1, 1.0, 30)[::-1]:
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])

        # if the resized image is smaller than the template, then break
        # from the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break
        # detect edges in the resized, grayscale image and apply template
        # matching to find the template in the image
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)

        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        threshold = 0.20*maxVal
        loc = np.where(result >= threshold)

        # if we have found a new maximum correlation value, then update
        # the bookkeeping variable

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)
            all_found = loc
            final_result = result

    # unpack the bookkeeping variable and compute the (x, y) coordinates
    # of the bounding box based on the resized ratio
    previous = None  # previous possible template place
    ps_X = None
    ps_Y = None
    pe_X = None
    pe_Y = None
    p_logo = None

    (_, maxLoc, r) = found
    Y, X = all_found

    indice = np.argsort(X)
    all_found = (Y[indice], sorted(X))

    total = len(all_found[0])
    counter = 0

    image3 = image.copy()

    for pt in izip(*all_found[::-1]):
        counter = counter + 1
        (startX, startY) = (int(pt[0] * r), int(pt[1] * r))
        (endX, endY) = (int((pt[0] + tW) * r), int((pt[1] + tH) * r))

        # at corner
        if (pt[0] <= 1 or pt[0] >= final_result.shape[1] - 1) or (pt[1] <= 1 or pt[1] >= final_result.shape[0] - 1):
            continue

        # only one logo
        if total == 1:
            detected, Logo = color_detection(image3[startY:endY, startX: endX])
            if detected:
                mark_logo(Logo, startX, endX, location)
            continue
        # get local infomation
        img = final_result[pt[1]-1: pt[1] + 1, pt[0] - 1: pt[0] + 1]
        if previous is None:
            detected, Logo = color_detection(image3[startY:endY, startX: endX])
            if detected:
                previous = np.argmax(img)
                (ps_X, ps_Y) = (startX, startY)
                (pe_X, pe_Y) = (endX, endY)
                p_logo = Logo
                continue
            continue

        if ps_X - 2 <= startX <= ps_X + 2:
            if counter < total:
                continue
            else:
                detected, Logo = color_detection(image3[ps_Y:pe_Y, ps_X: pe_X])
                if detected:
                    mark_logo( Logo, ps_X, pe_X, location)
                continue

        if ps_X - int(tW) * r <= startX <= ps_X + int(tW) * r:
            current = np.argmax(img)
            if current < previous:
                if counter == total:
                    mark_logo(p_logo, ps_X, pe_X, location)
                continue
            else:
                detected, Logo = color_detection(image3[startY:endY, startX: endX])
                if detected:
                    if counter == total:
                        mark_logo(Logo, startX, endX, location)
                        continue
                    else:
                        previous = np.argmax(img)
                        (ps_X, ps_Y) = (startX, startY)
                        (pe_X, pe_Y) = (endX, endY)
                        p_logo = Logo
                        continue
                else:
                    if counter == total:
                        detected, Logo = color_detection(image3[ps_Y:pe_Y, ps_X: pe_X])
                        if detected:
                            mark_logo(Logo, ps_X, pe_X, location)
                    else:
                        continue

        # draw a bounding box around the detected result and display the image
        detected, Logo = color_detection(image3[ps_Y:pe_Y, ps_X: pe_X])

        if detected:
            mark_logo(Logo, ps_X, pe_X, location)

        detected, Logo = color_detection(image3[startY:endY, startX: endX])
        if detected:
            previous = np.argmax(img)
            (ps_X, ps_Y) = (startX, startY)
            (pe_X, pe_Y) = (endX, endY)
            p_logo = Logo
        else:
            previous = None
        if counter == total:
            detected, Logo = color_detection(image3[startY:endY, startX: endX])
            if detected:
                mark_logo(Logo, startX, startY, location)

    timexx=time.time()
    print(af_wr-bf_wr)
    print(timexx-curt)
    print(location)
    return (location)





def vision():
    while(1):
        start_capture()






def color_detection(image):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    x = image.shape[0]
    y = image.shape[1]
    e = 5
    d = 1
    k = None
    lower_blue = np.array([75, 50, 50])
    upper_blue = np.array([130, 255, 255])
    maskb = cv2.inRange(img_hsv, lower_blue, upper_blue)

    maskb = cv2.dilate(maskb, kernel=k, iterations=d)
    maskb = cv2.erode(maskb, kernel=k, iterations=e)

    (contours, _) = cv2.findContours(maskb, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    B = len(contours)

    lower_yellow = np.array([22, 50, 50])
    upper_yellow = np.array([38, 255, 255])
    masky = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    masky = cv2.dilate(masky, kernel=k, iterations=d)
    masky = cv2.erode(masky, kernel=k, iterations=e)

    (contours, _) = cv2.findContours(masky, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 1:
        return False, -1
    cx = None
    cy = None
    for c in contours:
        # compute the center of the contour
        m = cv2.moments(c)
        if m[u"m00"] == 0:
            return False, -1
        cx = int(m[u"m10"] / m[u"m00"])
        cy = int(m[u"m01"] / m[u"m00"])
    x_r, y_r = cx / x, cy / y
    if x_r <= 0.28 or x_r >= 0.72 or y_r >= 0.72 or y_r <= 0.28:
        return False, -1
    # upper mask (170-180)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_red, upper_red)

    maskr = mask1 + mask2

    maskr = cv2.dilate(maskr, kernel=k, iterations=d)
    maskr = cv2.erode(maskr, kernel=k, iterations=e)
    (contours, _) = cv2.findContours(maskr, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    R = len(contours)

    if (R + B) != 6:
        return False, -1
    if len(contours) == 1:
        return True, 1
    if len(contours) == 2:
        return True, 2
    if len(contours) == 3:
        return True, 3
    if len(contours) == 4:
        return True, 4
    if len(contours) == 5:
        return True, 5
    if len(contours) == 6:
        return True, 6
    if len(contours) == 0:
        return True, 7
    return False, -1


def mark_logo(Logo, startX, endX, location):
    if Logo == 1:
        location[0] = (startX + endX)/2
    if Logo == 2:
        location[1] = (startX + endX)/2
    if Logo == 3:
        location[2] = (startX + endX)/2
    if Logo == 4:
        location[3] = (startX + endX)/2
    if Logo == 5:
        location[4] = (startX + endX)/2
    if Logo == 6:
        location[5] = (startX + endX)/2
    if Logo == 7:
        location[6] = (startX + endX)/2

def setup_mqtt():
    client = mqtt.Client("Pi")
    client.on_connect=onConnect
    client.on_message=onMessage
    client.connect("129.215.3.65")

    return client

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)
    client.subscribe("pi-finish-instruction")


def onMessage(client,userdata,msg):
    global location
    global logo_number
    if msg.topic=="pi-finish-instruction":
        if(location[logo_number]==0 | location[logo_number]<130 | location[logo_number]>190):
            send_message()
        else:
            stop()




def send_message():
    global logo_number
    global count
    global left_time
    global rigt_time
    if (location[logo_number]==0):
        count = count +1

        if count % 2 == 0 :
            left_time = right_time+2
            client.publish("pi-start-instruction","rt,l,"+str(left_time),qos=2)

        else:
            rigt_time = left_time+2
            client.publish("pi-start-instruction","rt,r,"+str(rigt_time),qos=2)

    else:
        if (location[logo_number]<130):

            client.publish("pi-start-instruction","rc,r",qos=2)

        if (location[logo_number]>190):
            client.publish("pi-start-instruction","rc,l",qos=2)


def stop():
    return 0


client = setup_mqtt()
location=start_capture()
send_message()
vision()
