# -*- coding: UTF-8 -*-

import struct
import threading
import time

from app.QQMusic import QQMusic
from core.Client import Socket
from core.Screenshots import Screenshots


class Runner(object):
    def __init__(self, ip, port):
        self.__socket = Socket(ip, port)
        self.__music = QQMusic()

    def start(self):
        while True:
            command = self.__socket.receive()
            if command == '':
                pass
            elif command.get_type() == 1:
                print('Heartbeat: Pong')
            elif command.get_type() == 2:
                thread = threading.Thread(target=self.execute_string(command), name='ExecuteStringThread')
                thread.start()
            elif command.get_type() == 0x7FFFFFFF:
                print('Receive: OK')
            else:
                print("This is error command")
            time.sleep(1)

    def execute_string(self, command):
        message = struct.unpack("!s", command.get_data())
        if message == 'screenshots':
            self.screenshots()
        else:
            self.__music.run(message)

    def screenshots(self):
        Screenshots(self.__socket).capture()
