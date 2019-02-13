import cv2
from matplotlib import pyplot as plt
import numpy

template1 = cv2.imread("Eden/Vision/Background/background.jpg")
cv2.imshow("logo1", template1)
cv2.waitKey(1)