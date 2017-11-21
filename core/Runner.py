# -*- coding: UTF-8 -*-

import threading
import time

from app import QQMusic
from core import Socket


class Runner(object):
    def __init__(self, ip, port):
        self.__socket = Socket.Socket(ip, port)
        self.__music = QQMusic.QQMusic()

    def start(self):
        while True:
            command = self.__socket.receive()
            if command == 'pong':
                print('Heartbeat: Pong')
            else:
                print('Command: ' + command)
                thread = threading.Thread(target=self.execute(command), name='ExecuteCommandThread')
                thread.start()
            time.sleep(1)

    def execute(self, command):
        self.__music.run(command)
