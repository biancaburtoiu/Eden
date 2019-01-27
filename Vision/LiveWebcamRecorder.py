import cv2
import math


def set_res(cap, x, y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def record_on_zero(path="record_output/", start_i=0):
    cam = cv2.VideoCapture(0)
    set_res(cam, 1920, 1080)
    i = start_i
    while True:
        ret_val, img = cam.read()
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 48:
            cv2.imwrite(path + "%s.jpg" % i, img)
            i += 1


def constant_record(path="record_output/", fps=2):
    cam = cv2.VideoCapture(0)
    set_res(cam, 1920, 1080)
    i = 0
    while True:
        ret_val, img = cam.read()
        cv2.imshow('my webcam', img)
        if i % math.ceil(10 / fps) == 0:
            cv2.imwrite(path + "%s.jpg" % i, img)
        i += 1


def main():
    record_on_zero(start_i=32)


if __name__ == '__main__':
    main()
