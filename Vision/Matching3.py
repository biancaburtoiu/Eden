# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2
from enum import Enum

# This code is written to be run in commond line


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True, help="Path to template image")
ap.add_argument("-i", "--images", required=True,
                help="Path to images where template will be matched")
ap.add_argument("-v", "--visualize",
                help="Flag indicating whether or not to visualize each iteration")
args = vars(ap.parse_args())

# load the image image, convert it to grayscale, and detect edges
template = cv2.imread(args["template"])
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
count2 = 0


class LOGO(Enum):
    no = 0
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    fail = 4


# may be not centers?

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
    print("B {}".format(len(contours)))
    cv2.imshow("m2", maskb)

    lower_yellow = np.array([22, 50, 50])
    upper_yellow = np.array([38, 255, 255])
    masky = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    masky = cv2.dilate(masky, kernel=k, iterations=d)
    masky = cv2.erode(masky, kernel=k, iterations=e)

    (contours, _) = cv2.findContours(masky, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 1:
        return False, LOGO.no
    cx = None
    cy = None
    for c in contours:
        # compute the center of the contour
        m = cv2.moments(c)
        if m["m00"] == 0:
            return False, LOGO.no
        cx = int(m["m10"] / m["m00"])
        cy = int(m["m01"] / m["m00"])
    x_r, y_r = cx / x, cy / y
    if x_r <= 0.28 or x_r >= 0.72 or y_r >= 0.72 or y_r <= 0.28:
        return False, LOGO.no
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
    cv2.imshow("m1", maskr)
    cv2.imshow("img", image)

    R = len(contours)
    print("R {}".format(len(contours)))

    # cv2.waitKey(0)
    if (R + B) != 6:
        return False, LOGO.no
    if len(contours) == 1:
        return True, LOGO.one
    if len(contours) == 2:
        return True, LOGO.two
    if len(contours) == 3:
        return True, LOGO.three
    if len(contours) == 4:
        return True, LOGO.four
    if len(contours) == 5:
        return True, LOGO.five
    if len(contours) == 6:
        return True, LOGO.six
    if len(contours) == 0:
        return True, LOGO.seven
    return False, LOGO.no


def mark_logo(Img, Logo, startX, startY, endX, endY):
    if Logo == LOGO.one:
        cv2.rectangle(Img, (startX, startY), (endX, endY), (0, 0, 255), 2)  # red
    if Logo == LOGO.two:
        cv2.rectangle(Img, (startX, startY), (endX, endY), (0, 255, 0), 2)  # green
    if Logo == LOGO.three:
        cv2.rectangle(Img, (startX, startY), (endX, endY), (255, 0, 0), 2)  # blue
    if Logo == LOGO.four:
        cv2.rectangle(Img, (startX, startY), (endX, endY), (255, 255, 0), 2)  # aqua
    if Logo == LOGO.five:
        cv2.rectangle(Img, (startX, startY), (endX, endY), (255, 0, 255), 2)  # pink
    if Logo == LOGO.six:
        cv2.rectangle(Img, (startX, startY), (endX, endY), (0, 255, 255), 2)  # yellow
    if Logo == LOGO.seven:
        cv2.rectangle(Img, (startX, startY), (endX, endY), (255, 255, 255), 2)  # white


# loop over the images to find the template in
for imagePath in glob.glob(args["images"] + "/*.jpg"):
    # load the image, convert it to grayscale, and initialize the
    # bookkeeping variable to keep track of the matched region
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None
    all_found = None
    final_result = None

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

        # update it if one portion get the maximal probability
        # check to see if the iteration should be visualized
        if args.get("visualize", False):
            # draw a bounding box around the detected region
            clone = np.dstack([edged, edged, edged])
            cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
                          (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
            # cv2.imshow("Visualize", clone)
            cv2.waitKey(1000)

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

    image2 = image.copy()
    print("Now pic {} has {}".format(count2, len(all_found[0])))

    image3 = image.copy()

    print("shape {}".format(final_result.shape))
    for pt in zip(*all_found[::-1]):
        counter = counter + 1
        (startX, startY) = (int(pt[0] * r), int(pt[1] * r))
        (endX, endY) = (int((pt[0] + tW) * r), int((pt[1] + tH) * r))
        print("previous label:{} ps_X: {}".format(p_logo, ps_X))

        if color_detection(image3[startY:endY, startX: endX])[0]:
            cv2.rectangle(image2, (startX, startY), (endX, endY), (0, 0, 255), 2)
        # at corner

        # print("X {} Y {}".format(startX, startY))
        if (pt[0] <= 1 or pt[0] >= final_result.shape[1] - 1) or (pt[1] <= 1 or pt[1] >= final_result.shape[0] - 1):
            print("edge discard")
            continue

        # only one logo
        if total == 1:
            detected, Logo = color_detection(image3[startY:endY, startX: endX])
            print(Logo)
            if detected:
                mark_logo(image, Logo, startX, startY, endX, endY)
                # cv2.waitKey(0)
                cv2.imshow("changed", image)
                print("The very location of this rec is {} {} {} {}".format(startX, startY, endX, endY))
            else:
                print("logo is not detected")
            continue
        # get local infomation
        img = final_result[pt[1]-1: pt[1] + 1, pt[0] - 1: pt[0] + 1]
        if previous is None:
            detected, Logo = color_detection(image3[startY:endY, startX: endX])
            print(Logo)
            if detected:
                print("previous got")
                previous = np.argmax(img)
                (ps_X, ps_Y) = (startX, startY)
                (pe_X, pe_Y) = (endX, endY)
                p_logo = Logo
                continue
            print("previous not got")
            continue

        if ps_X - 2 <= startX <= ps_X + 2:
            if counter < total:
                print("too close discard again")
                continue
            else:
                detected, Logo = color_detection(image3[ps_Y:pe_Y, ps_X: pe_X])
                print(Logo)
                if detected:
                    mark_logo(image, Logo, ps_X, ps_Y, pe_X, pe_Y)
                    cv2.imshow("changed", image)
                print("last found")
                # print("The location of this rec is {} {} {} {}".format(startX, startY, endX, endY))
                continue

        if ps_X - int(tW) * r <= startX <= ps_X + int(tW) * r:
            print("overlapped")
            current = np.argmax(img)
            if current < previous:
                print("not replace")
                if counter == total:
                    print("last one")
                    mark_logo(image, p_logo, ps_X, ps_Y, pe_X, pe_Y)
                    cv2.imshow("changed", image)
                continue
            else:
                detected, Logo = color_detection(image3[startY:endY, startX: endX])
                print(Logo)
                if detected:
                    print("replace")
                    if counter == total:
                        mark_logo(image, Logo, startX, startY, endX, endY)
                        continue
                    else:
                        previous = np.argmax(img)
                        (ps_X, ps_Y) = (startX, startY)
                        (pe_X, pe_Y) = (endX, endY)
                        p_logo = Logo
                        continue
                else:
                    if counter == total:
                        print("last one ")
                        detected, Logo = color_detection(image3[ps_Y:pe_Y, ps_X: pe_X])
                        print(Logo)
                        if detected:
                            mark_logo(image, Logo, ps_X, ps_Y, pe_X, pe_Y)
                            cv2.imshow("changed", image)
                    else:
                        continue

        # draw a bounding box around the detected result and display the image
        detected, Logo = color_detection(image3[ps_Y:pe_Y, ps_X: pe_X])
        print(Logo)
        if detected:
            mark_logo(image, Logo, ps_X, ps_Y, pe_X, pe_Y)
            cv2.imshow("changed", image)
            print("certain")
        # print("The location of this rec is {} {} {} {}".format(ps_X, ps_Y, ps_X, pe_Y))
        detected, Logo = color_detection(image3[startY:endY, startX: endX])
        if detected:
            previous = np.argmax(img)
            (ps_X, ps_Y) = (startX, startY)
            (pe_X, pe_Y) = (endX, endY)
            p_logo = Logo
        else:
            previous = None
        if counter == total:
            print("last one")
            detected, Logo = color_detection(image3[startY:endY, startX: endX])
            print(Logo)
            if detected:
                mark_logo(image, Logo, startX, startY, endX, endY)

            # print("The location of this rec is {} {} {} {}".format(startX, startY, endX, endY))

    cv2.imwrite("image/fram%d.jpg" % count2, image)  # save frame as JPEG file
    cv2.imwrite("image/framx%d.jpg" % count2, image2)  # save frame as JPEG file
    count2 = count2 + 1
