import cv2
import numpy as np


def main():
    img = cv2.imread("0x.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh1 = cv2.threshold(img, 133, 255, cv2.THRESH_BINARY_INV)[1]
    avr_SA = 0
    avr_OR = 0
    avr_UR = 0
    for i in range(0,101):
        image = cv2.imread("QA_Chair1/" + str(i) + ".jpg")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh2 = cv2.threshold(image, 133, 255, cv2.THRESH_BINARY_INV)[1]

        floor1 = cv2.countNonZero(thresh1) # expert
        floor2 = cv2.countNonZero(thresh2) # test


        # cv2.imshow("floor", thresh1)
        # cv2.waitKey(0)
        over = np.count_nonzero(thresh2[thresh1==0]) # not supposed to be ground
        total = thresh2[thresh1>0].sum()/255
        mis = np.count_nonzero(thresh1[thresh1 > 0])
        result = mis - total
        UR = result/(floor1+over)
        # print("result" + str(result))
        OR = over / (over+floor1)
        SA = (1-np.abs(floor2- total)/total)
        avr_OR = OR + avr_OR
        avr_SA = SA + avr_SA
        avr_UR = SA + avr_UR
        # print(over)
        # print(floor1)
        # print(floor2)
        print(SA)
        print(OR)
        print(UR)
        print("")
    print(avr_SA/ 101)
    print(avr_OR/ 101)
    print(avr_UR/ 101)


if __name__ == '__main__':
    main()