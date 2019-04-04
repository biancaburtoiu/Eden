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
template = imutils.resize(template, width=int(template.shape[1] * 0.4))
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
left_time=0
right_time=0
count=0
camera=PiCamera()
camera.resolution=(360,240)
location= [[],[],[],[],[],[],[]]
new_location= [[],[],[],[],[],[],[]]
logo_number=0
is_centre= False
is_rotating= False
is_not_seeing= False
loc=0
got_result =0
running=False
rotate_time=0
logos_in_range=[]

def init():
    global location
    global logo_number
    global is_centre
    global is_rotating
    global loc
    global got_result
    global running
    global new_location
    global count
    left_time=0
    right_time=0
    count=0

    logos_in_range=[]
    location= [[],[],[],[],[],[],[]]
    new_location= [[],[],[],[],[],[],[]]
    logo_number=0
    rotate_time=0
    is_centre= False
    is_rotating= False
    loc=0
    got_result =False
    running=False
    is_not_seeing=False


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
    global is_centre
    global is_rotating
    global got_result
    global running
    global new_location
    global is_not_seeing
    global rotate_time
    global logos_in_range
    global loc
    location = [[],[],[],[],[],[],[]]




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
        W = endX - startX
        F = 100 # need measure
        H = 0.08
        D = H * F / W

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
                            continue
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


    #print(af_wr-bf_wr)
    #print(timexx-curt
    new_location= location
    print(new_location)
    print(D)
    if running:
        loc=0
        if  len(location[logo_number])!=0:
            loc = np.average(location[logo_number])

        logos_in_range = [True if l>140 and l<200 else False for l in location[logo_number]]

        print(len(location[logo_number]))
        if  len(location[logo_number])!=0 and is_not_seeing :
            is_not_seeing = False
            client.publish("pi-start-instruction","s",qos=2)
            time.sleep(0.1)
            print("stop turning1")

        if is_not_seeing and ((time.time()-rotate_time)>(5*count)):
            client.publish("pi-start-instruction","s",qos=2)
            print("it wont stop")



        if (loc>140 and loc<200) or any(logos_in_range):
            is_centre=True
            print("Is_centre")

        if is_rotating and is_centre:
            is_rotating=False
            client.publish("pi-start-instruction","s",qos=2)
            print("is not rotating")

        if is_centre and (not is_rotating):
            if len(location[logo_number])!= 0 and D>0.17 :
                client.publish("pi-start-instruction","m,0,0.03",qos=2)
                print("forward")

            elif len(location[logo_number])!= 0 and D<=0.17 :
                client.publish("pi-start-instruction","s",qos=2)
                client.publish("sonar-creeping","1",qos=2)
                print("stop forward")
                running=False
                print("everything is fine")

        elif(loc>140 and loc<200):
            is_centre=True
            client.publish("pi-start-instruction","s",qos=2)
            time.sleep(0.1)
            is_rotating=False
            print("turn stop")


    if len(location[logo_number])!=0:
        got_result =2
    else:
        got_result = min(2,got_result+1)
    return location





def vision():
    while (1):
        start_capture()






def color_detection(image):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    x = image.shape[0]
    y = image.shape[1]
    e = 3
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
    lower_red = np.array([160, 50, 50])
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
        location[0].append((startX + endX)/2)
    if Logo == 2:
        location[1].append((startX + endX)/2)
    if Logo == 3:
        location[2].append((startX + endX)/2)
    if Logo == 4:
        location[3].append((startX + endX)/2)
    if Logo == 5:
        location[4].append((startX + endX)/2)
    if Logo == 6:
        location[5].append((startX + endX)/2)
    if Logo == 7:
        location[6].append((startX + endX)/2)

def setup_mqtt():
    client = mqtt.Client("Pi")
    client.on_connect=onConnect
    client.on_message=onMessage
    client.connect("129.215.3.65")

    return client

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)
    client.subscribe("pi-finish-instruction")
    client.subscribe("close-navigate")
    client.subscribe("logo-detection")




def onMessage(client,userdata,msg):
    global new_location
    global logo_number
    global running
    if msg.topic =="close-navigate":
        init()
        logo_number=int(msg.payload.decode())
        print("logo number")
        logo_number=logo_number-1
        print (logo_number)
        client.publish("pi-start-instruction","reverse",qos=2)

    if msg.topic =="logo-detection":
        global running
        running = True
        send_message()
        print("logo-detection")

    elif running:
        if msg.topic=="pi-finish-instruction":
            while got_result!=2:
                time.sleep(0.1)
            if len(new_location[logo_number]) == 0:
                send_message()
                print("finish-instruction 1")
                print(new_location)

            else:
                loc = np.average(new_location[logo_number])
                print("finish-instruction 2")

            if(loc <140 or loc>200):
                send_message()
                print("finish-instruction 3")
            #else:
                #is_centre=True
                #print("finish-instruction 4")








def send_message():
    global logo_number
    global count
    global left_time
    global right_time
    global is_centre
    global is_rotating
    global got_result
    global is_not_seeing
    global rotate_time
    if len(new_location[logo_number])==0:
        if count<4:
            count = count +1

        is_not_seeing=True

        if count % 2 != 0 :
            #left_time = right_time+400
            client.publish("pi-start-instruction","rc,l,0.08",qos=2)
            print("not seeing,turn left")
            got_result=False
            rotate_time=0
            rotate_time=time.time()


        else:
            #right_time = left_time+400
            client.publish("pi-start-instruction","rc,r,0.08",qos=2)
            print("not seeing,turn right")
            got_result=False
            rotate_time=0
            rotate_time=time.time()


    else:
        is_not_seeing=False

        loc = np.average(new_location[logo_number])

        if (loc<140):
            client.publish("pi-start-instruction","rc,r,0.02",qos=2)
            print("turn constantly right")
            is_rotating=True

        if (loc>200):
            client.publish("pi-start-instruction","rc,l,0.02",qos=2)
            print("turn constantly left")
            is_rotating=True







client = setup_mqtt()
client.loop_start()
start_capture()
time.sleep(3)
vision()
