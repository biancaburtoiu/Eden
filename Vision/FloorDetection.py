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


def floorDetection(n, m):
    image = cv2.imread("Calibration Pictures/"+str(n)+".jpg")
    img = getImgRegionByCameraNo(image, m)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    histH = cv2.calcHist(hsv, [0], None, [180], [0, 180])

    # histS = cv2.calcHist(hsv, [1], None, [255], [0, 255])
    # histV = cv2.calcHist(hsv, [2], None, [255], [0, 255])

    img_hist = threshHistSmooth(histH, 20, 5, 1)

    # Threshold in hsv space in order to deal with varying light.
    # Since the background is almost grey, the hue value is from 0 to 360(0 to 180 in opencv)
    # The saturation is set to 0 to 50, higher value add more noise
    # If assumption can be made the light condition is good, also adjust V for white and dark object
    # add texture information may help but that is difficult

    lower = (0, 0, 60) # lower bound
    higher = (180, 60, 200) # change if white is not acceptable
    # blurred = cv2.GaussianBlur(hsv, (5,5),0)

    threshold = cv2.inRange(hsv, lower, higher)
    dst = cv2.bitwise_not(threshold)
    dst = cv2.erode(dst, (49, 49), iterations=7)
    dst = cv2.dilate(dst, (64,64), iterations=3)

    # Canny graph for boundary?
    # canny = cv2.Canny(dst, 0, 255)

    cv2.imwrite("Floor Pictures/"+str(n)+ str(m)+"t.jpg", dst)
    cv2.imwrite("Floor Pictures/"+str(n)+ str(m)+"o.jpg", img)
    # cv2.imwrite("Threshold picture/"+str(n)+ str(m)+".jpg", dst)
    # cv2.imwrite("Threshold picture/"+str(n)+ str(m)+"c.jpg", canny)

for i in range(3, 40):
    for j in range(1, 5):
        floorDetection(i ,j)


# floorDetection(1, 4)