import numpy as np
import cv2
import math

# Assume that camera 1 is labelled camera_no=1
def getImgRegionByCameraNo(img, camera_no):
    x_lower_bound = int((len(img) / 3) * math.floor((camera_no - 1) / 3))
    x_upper_bound = int((len(img) / 3) * (math.floor(camera_no / 4) + 1))

    y_lower_bound = int((len(img[0]) / 3) * ((camera_no - 1) % 3))
    y_upper_bound = int((len(img[0]) / 3) * (((camera_no - 1) % 3) + 1))

    return img[x_lower_bound:x_upper_bound, y_lower_bound:y_upper_bound, :]


# Create a gaussian smoothing window and applies it to histogram
def threshHistSmooth(img_hist, n, w, sigma):
    nn = int((n - 1) / 2)
    gauss = np.asarray([(w / n) * x ** 2 for x in range(-nn, nn + 1)], dtype=float)
    gauss = np.exp(-gauss / (2 * sigma ** 2))
    the_filter = gauss / sum(gauss)
    hist_convolve = np.convolve(np.ravel(img_hist), the_filter)
    return hist_convolve

def segmentation(img):
    img = cv2.GaussianBlur(img,(5,5),0)
    img[:,:,2] = 255
    image = img.reshape((-1, 3))
    image = np.float32(image)
    criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_EPS, 10, 1.0)
    K = 20
    ret, label, center = cv2.kmeans(image, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    print(center)
    res = center[label.flatten()]
    res2 = res.reshape((360,640, 3))
    cv2.imshow('res2', res2)
    cv2.waitKey(0)




def floorDetection(n, m):
    image = cv2.imread("Calibration Pictures/"+str(n)+".jpg")
    img = getImgRegionByCameraNo(image, m)

    # cv2.imshow('origin', img)

    # normalize RGB not working since light intensity is not even
    # R = img[:,:,0]
    # G = img[:,:,1]
    # B = img[:,:,2]
    # deno = np.sqrt(R*R+B*B+G*G)
    # deno[deno<=0] = 255
    # img[:,:,0] = R/deno*255
    # img[:,:,1] = G/deno*255
    # img[:,:,2] = B/deno*255
    # cv2.imshow("", img)
    # cv2.waitKey(0)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # cv2.imshow("blurred", blurred)

    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1)
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    # cv2.imshow("gradient", gradient)

    blurred = cv2.GaussianBlur(gradient, (23, 23), 0)
    (_, thresh) = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)

    # cv2.imshow("thresh", thresh)


    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=2)

    # cv2.imshow("closed", closed)

    # segmentation(0,0,hsv)
    # histH = cv2.calcHist(hsv, [0], None, [180], [0, 180])

    # histS = cv2.calcHist(hsv, [1], None, [255], [0, 255])
    # histV = cv2.calcHist(hsv, [2], None, [255], [0, 255])

    # img_hist = threshHistSmooth(histH, 20, 5, 1)

    # Threshold in hsv space in order to deal with varying light.
    # Since the background is almost grey, the hue value is from 0 to 360(0 to 180 in opencv)
    # The saturation is set to 0 to 50, higher value add more noise
    # If assumption can be made the light condition is good, also adjust V for white and dark object
    # add texture information may help but that is difficult

    img = cv2.pyrMeanShiftFiltering(img, 50, 20, maxLevel=2)
    # kernel = np.ones((25, 25), np.float32) / 625
    # img = cv2.filter2D(img, -1, kernel)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower = (0, 0, 60) # lower bound
    higher = (180, 50, 230) # change if white is not acceptable, s can not be smaller than 50

    threshold2 = cv2.inRange(hsv, lower, higher)
    reverse = cv2.bitwise_not(threshold2)
    # cv2.imshow("img", img)
    # cv2.imshow("thresh1", reverse)
    reverse = cv2.erode(reverse, None, iterations=3)
    reverse = cv2.dilate(reverse, None, iterations=1)

    reverse = cv2.bitwise_or(reverse, closed)
    reverse = cv2.morphologyEx(reverse, cv2.MORPH_CLOSE, kernel)

    # cv2.imshow("final", reverse)

    # Canny graph for boundary?
    # canny = cv2.Canny(dst, 0, 255)

    cv2.imwrite("Floor Pictures/"+str(n)+ str(m)+"t.jpg", reverse)
    cv2.imwrite("Floor Pictures/"+str(n)+ str(m)+"o.jpg", img)

    result = np.array(reverse)
    result[result>0] = 1
    print(result.shape)

    # cv2.waitKey()

for i in range(3, 40):
    for j in range(1, 5):
        floorDetection(i ,j)

floorDetection(3, 1)

# image = cv2.imread("Calibration Pictures/"+str(3)+".jpg")

