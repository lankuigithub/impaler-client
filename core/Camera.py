import os
import time

import cv2
from PIL import  Image

from core.Command import Command


class Camera(object):
    def __init__(self, command, client):
        self.__command = command
        self.__client = client
        self.__camera_file = 'camera.jpg'
        self.__camera_thumbnail_file = 'camera_thumbnail.jpg'

    def shoot(self):
        # create camera image
        cap = cv2.VideoCapture(0)
        time.sleep(1)
        ret, frame = cap.read()
        cv2.imwrite(self.__camera_file, frame)
        cap.release()
        # create the thumbnail
        img = Image.open(self.__camera_file)
        w, h = img.size
        img.thumbnail((w // 10, h // 10))
        img.save(self.__camera_thumbnail_file)
        self.send()

    def send(self):
        command = Command()
        command.set_type(3)
        command.set_data_length(os.path.getsize(self.__camera_thumbnail_file))
        with open(self.__camera_thumbnail_file, 'rb') as f:
            command.set_data(f.read())
        self.__client.send_command(command)
