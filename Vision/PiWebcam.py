from paramiko import SSHClient
from scp import SCPClient
import os
import cv2
import time
import numpy as np
from scp import SCPException


class Client:
    def __init__(self, IO):
        print('[Toddler] I am toddler playing in a sandbox')
        self.camera = IO.camera.initCamera('pi', 'high')
        self.getInputs = IO.interface_kit.getInputs
        self.getSensors = IO.interface_kit.getSensors
        self.mc = IO.motor_control
        self.sc = IO.servo_control

    def control(self):
        print('{}\t{}'.format(self.getSensors(), self.getInputs()))
        time.sleep(0.05)

    def vision(self):
        image = self.camera.getFrame()
        self.camera.imshow('Camera', image)
        cv2.imwrite("last_frame.png", image)
        time.sleep(1)


class ImageServer:
    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.connect("rattata", username="student", password="password")

        # SCPCLient takes a paramiko transport as an argument
        self.scp = SCPClient(self.ssh.get_transport())
        self.img_path = '%s/last_frame.png' % os.getcwd()

    def get_img(self):
        try:
            img = None
            while img is None:
                self.scp.get('/home/student/last_frame.png', local_path=self.img_path)
                img = cv2.imread(self.img_path)
            return img
        except SCPException:
            self.scp = SCPClient(self.ssh.get_transport())
            return self.get_img()

    def live_cam(self):
        while True:
            img = self.get_img()
            cv2.imshow("Webcam Image", img)
            cv2.waitKey(1000)