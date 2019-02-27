# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2

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

def color_detection(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    e = 3
    d = 3

    lower_blue = np.array([75, 50, 50])
    upper_blue = np.array([130, 255, 255])
    maskB = cv2.inRange(img_hsv, lower_blue, upper_blue)

    maskB = cv2.dilate(maskB, kernel=(5, 5), iterations=d)
    maskB = cv2.erode(maskB, kernel=(5,5), iterations=e)

    (contours, _) = cv2.findContours(maskB, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    print("contour number is {}".format(len(contours)))

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        print("B corners are x: {}, y: {}, w: {}, h: {}".format(x, y, w, h))

    cv2.imshow("m2", maskB)
    if len(maskB[maskB>0]) == 0:
        return False

    lower_yellow = np.array([22, 50, 50])
    upper_yellow = np.array([38, 255, 255])
    maskY = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    maskY = cv2.dilate(maskY, kernel=(5, 5), iterations=d)
    maskY = cv2.erode(maskY, kernel=(5,5), iterations=e)

    (contours, _) = cv2.findContours(maskY, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    print("contour number is {}".format(len(contours)))

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        print("Y corners are x: {}, y: {}, w: {}, h: {}".format(x, y, w, h))
    cv2.imshow("m3", maskY)
    if len(maskY[maskY>0]) == 0:
        return False


    # upper mask (170-180)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_red, upper_red)

    maskR = mask1 + mask2

    res, maskR = cv2.threshold(maskR, 127, 255, 0)

    maskR = cv2.dilate(maskR, kernel=(5, 5), iterations=d)
    maskR = cv2.erode(maskR, kernel=(5,5), iterations=e)

    (contours, _) = cv2.findContours(maskR, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    print("contour number is {}".format(len(contours)))

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        print("R corners are x: {}, y: {}, w: {}, h: {}".format(x, y, w, h))

    cv2.imshow("m1", maskR)

    if len(maskR[maskR>0]) == 0:
        return False

    cv2.waitKey(0)
    return True



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
        threshold = 0.40*maxVal
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

    previous = None # previous possible template place
    ps_X = None
    ps_Y = None
    pe_X = None
    pe_Y = None

    (_, maxLoc, r) = found
    Y, X = all_found

    indice = np.argsort(X)
    all_found = (Y[indice], sorted(X))

    total = len(all_found[0])
    counter = 0
    # cv2.imshow("template", final_result)

    image2 = image.copy()
    print("Now pic {} has {}".format(count2, len(all_found[0])))

    print("shape {}".format(final_result.shape))
    for pt in zip(*all_found[::-1]):
        print("pt in final {}".format(pt))

        counter = counter + 1
        (startX, startY) = (int(pt[0] * r), int(pt[1] * r))
        (endX, endY) = (int((pt[0] + tW) * r), int((pt[1] + tH) * r))

        if color_detection(image2[startY:endY, startX: endX]):
            cv2.rectangle(image2, (startX, startY), (endX, endY), (0, 0, 255), 2)
        # at corner

        # print("X {} Y {}".format(startX, startY))
        if (pt[0] <= 1 or pt[0] >= final_result.shape[1] - 1) or (pt[1] <= 1 or pt[1] >= final_result.shape[0] - 1):
            print("edge discard")
            continue

        # only one
        if (total == 1):
            if color_detection(image[startY:endY, startX: endX]):
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
            print("The very location of this rec is {} {} {} {}".format(startX, startY, endX, endY))
            continue

        # get local infomation
        img = final_result[pt[1]-1: pt[1]+ 1, pt[0]- 1: pt[0]+ 1]

        if previous is None:
            print("previous got")
            previous = np.argmax(img)
            (ps_X, ps_Y) = (startX, startY)
            (pe_X, pe_Y) = (endX, endY)
            continue

        if (startX >= ps_X - 5 and startX <= ps_X + 5):
            if (counter < total):
                print("too close discard again")
                continue
            else:
                if color_detection(image[startY:endY, startX: endX]):
                    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                print("last found")
                # print("The location of this rec is {} {} {} {}".format(startX, startY, endX, endY))
                continue
        if ( startX >= ps_X - int(tW) * r and startX <= ps_X + int(tW) * r ):
            print("overlapped")
            current = np.argmax(img)
            # print("previous {} current {}".format(previous, current))

            if current < previous:
                if counter == total:
                    if color_detection(image[ps_Y:pe_Y, ps_X: pe_X]):
                        cv2.rectangle(image, (ps_X, ps_Y), (pe_X, pe_Y), (0, 0, 255), 2)
                continue
            else:
                if counter == total:
                    if color_detection(image[startY:endY, startX: endX]):
                        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    continue
                previous = np.argmax(img)
                (ps_X, ps_Y) = (int(pt[0] * r), int(pt[1] * r))
                (pe_X, pe_Y) = (int((pt[0] + tW) * r), int((pt[1] + tH) * r))
                continue
        # draw a bounding box around the detected result and display the image
        if color_detection(image[ps_Y:pe_Y, ps_X: pe_X]):
            cv2.rectangle(image, (ps_X, ps_Y), (pe_X, pe_Y), (0, 0, 255), 2)
        print("certain")
        # print("The location of this rec is {} {} {} {}".format(ps_X, ps_Y, ps_X, pe_Y))
        previous = np.argmax(img)
        (ps_X, ps_Y) = (startX, startY)
        (pe_X, pe_Y) = (endX, endY)
        if (counter == total):
            if color_detection(image[startY:endY, startX: endX]):
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
            # print("The location of this rec is {} {} {} {}".format(startX, startY, endX, endY))



    # cv2.imshow("Image", image)
    cv2.imwrite("image/fram%d.jpg" % count2, image)  # save frame as JPEG file
    # cv2.imwrite("image/framx%d.jpg" % count2, image2)  # save frame as JPEG file
    count2 = count2 + 1
    # cv2.waitKey(0)