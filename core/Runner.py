# -*- coding: UTF-8 -*-

import threading

from app.QQMusic import QQMusic
from core.Camera import Camera
from core.Client import Client
from core.Register import Register
from core.Screen import Screen


class Runner(object):
    def __init__(self, ip, port):
        self.__client = Client(ip, port)
        Register(self.__client).register()
        self.__music = QQMusic()

    def start(self):
        while True:
            command_list = self.__client.receive()
            for command in command_list:
                if command.get_type() == 0x00000001:
                    print('Heartbeat: Pong')
                elif command.get_type() == 0x00000002:
                    thread = threading.Thread(target=self.execute_string(command), name='ExecuteStringThread')
                    thread.start()
                elif command.get_type() == 0x00000003:
                    thread = threading.Thread(target=self.execute_image(command), name='ExecuteImageThread')
                    thread.start()
                elif command.get_type() == 0x00000004:
                    thread = threading.Thread(target=self.execute_screen(command), name='ExecuteScreenThread')
                    thread.start()
                elif command.get_type() == 0x00000005:
                    thread = threading.Thread(target=self.execute_camera(command), name='ExecuteCameraThread')
                    thread.start()
                elif command.get_type() == 0x00000006:
                    print("Register: " + command.get_data().decode('utf-8'))
                elif command.get_type() == 0x00000007:
                    print("Client List: " + command.get_data().decode('utf-8'))
                else:
                    print(command.get_type())
                    print("This is error command")

    def execute_string(self, command):
        message = command.get_data().decode('utf-8')
        print(message)

    def execute_screen(self, command):
        Screen(command, self.__client).capture()

    def execute_camera(self, command):
        Camera(command, self.__client).shoot()

    def execute_image(self, command):
        with open('capture.jpg', 'wb') as f:
            f.write(command.get_data())
