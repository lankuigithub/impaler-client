# -*- coding: UTF-8 -*-

import struct
import threading
import time

from app.QQMusic import QQMusic
from core.Client import Client
from core.Screen import Screen
from core.Camera import Camera


class Runner(object):
    def __init__(self, ip, port):
        self.__client = Client(ip, port)
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
            elif command.get_type() == 0x7FFFFFFF:
                print('Receive: OK')
            else:
                print("This is error command")
            time.sleep(1)

    def execute(self, command):
        message = command.get_data().decode('utf-8')
        print('Receive: ' + message)
        if message == 'screen':
            Screen(command, self.__client).capture()
        if message == 'camera':
            Camera(command, self.__client).shoot()
        else:
            self.__music.run(message)
