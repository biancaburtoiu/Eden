import cv2


def set_res(cap, x, y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def show_webcam():
    cam = cv2.VideoCapture(0)
    set_res(cam, 1920, 1080)
    i = 0
    while True:
        ret_val, img = cam.read()
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 48:
            cv2.imwrite("%s.jpg" % i, img)
            i += 1
    cv2.destroyAllWindows()


def main():
    show_webcam()


if __name__ == '__main__':
    main()
