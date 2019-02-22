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
        threshold = 0.72*maxVal
        loc = np.where(result >= threshold)

        # update it if one portion get the maximal probability
        # check to see if the iteration should be visualized
        if args.get("visualize", False):
            # draw a bounding box around the detected region
            clone = np.dstack([edged, edged, edged])
            cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
                          (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
            cv2.imshow("Visualize", clone)
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

    cv2.imshow("template", final_result)
    cv2.waitKey(0)


    for pt in zip(*all_found[::-1]):
        counter = counter + 1
        (startX, startY) = (int(pt[0] * r), int(pt[1] * r))
        (endX, endY) = (int((pt[0] + tW) * r), int((pt[1] + tH) * r))
        print(startX)
        print(startY)

        if (total == 1):
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
            print("The location of this rec is {} {} {} {}".format(startX, startY, endX, endY))
            continue
        img = final_result[startY-5: startY+5 , startX-5: startX+5]
        cv2.imshow("sub", img)
        cv2.waitKey(0)

        if previous is None:
            previous = np.argmax(img)
            (ps_X, ps_Y) = (startX, startY)
            (pe_X, pe_Y) = (endX, endY)
            continue
        if (startX >= ps_X - 5 and startX <= ps_X + 5):
            if (counter < total):
                continue
            else:
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                print("The location of this rec is {} {} {} {}".format(startX, startY, endX, endY))
                continue
        if ( startX >= ps_X - int(tW) * r and startX <= ps_X + int(tW) * r ):
            print("overlapped")
            current = np.argmax(img)
            print("previous {} current {}".format(previous, current))

            if current < previous:
                continue
            else:
                previous = np.argmax(img)
                (ps_X, ps_Y) = (int(pt[0] * r), int(pt[1] * r))
                (pe_X, pe_Y) = (int((pt[0] + tW) * r), int((pt[1] + tH) * r))
                continue
        # draw a bounding box around the detected result and display the image
        cv2.rectangle(image, (ps_X, ps_Y), (pe_X, pe_Y), (0, 0, 255), 2)
        print("The location of this rec is {} {} {} {}".format(ps_X, ps_Y, ps_X, pe_Y))
        previous = np.argmax(img)
        (ps_X, ps_Y) = (startX, startY)
        (pe_X, pe_Y) = (endX, endY)
        if (counter == total):
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
            print("The location of this rec is {} {} {} {}".format(startX, startY, endX, endY))



    cv2.imshow("Image", image)
    cv2.waitKey(0)