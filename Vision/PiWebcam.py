from paramiko import SSHClient
from scp import SCPClient
import os
import cv2


class ImageServer:
    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.connect("rattata", username="student", password="password")

        # SCPCLient takes a paramiko transport as an argument
        self.scp = SCPClient(self.ssh.get_transport())
        self.img_path = '%s/last_frame.png' % os.getcwd()

    def get_img(self):
        self.scp.get('/home/student/last_frame.png', local_path=self.img_path)
        img = cv2.imread(self.img_path)
        return img
