# -*- coding: UTF-8 -*-

import struct
import threading
import time

from app import QQMusic
from core import Client


class Runner(object):
    def __init__(self, ip, port):
        self.__socket = Client.Socket(ip, port)
        self.__music = QQMusic.QQMusic()

    def start(self):
        while True:
            command = self.__socket.receive()
            if command == '':
                pass
            elif command.get_type() == 1:
                print('Heartbeat: Pong')
            elif command.get_type() == 0x7FFFFFFF:
                print('Receive: OK')
            else:
                thread = threading.Thread(target=self.execute(command), name='ExecuteCommandThread')
                thread.start()
            time.sleep(1)

    def execute(self, command):
        if command.get_type() == 2 and command.get_data_length() > 0:
            message = struct.unpack("!s", command.get_data())
            self.__music.run(message)
