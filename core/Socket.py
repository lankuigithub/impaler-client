# -*- coding: UTF-8 -*-

import socket
import threading
import time


class Socket(object):
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__mutex = threading.Lock()
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect((self.__ip, self.__port))
        self.__socket = _socket
        self.heartbeat()

    def receive(self):
        data = self.__socket.recv(1024)
        if data == '':
            return data
        else:
            command = data.decode('utf-8')
            command = command.replace('\r\n', '')
            return command

    def send(self, message):
        self.__mutex.acquire()
        self.__socket.send((message + '\r\n').encode('utf-8'))
        self.__mutex.release()

    def heartbeat(self):
        t = threading.Thread(target=self.send_ping, name='HeartbeatThread')
        t.start()

    def send_ping(self):
        while True:
            self.send('ping')
            time.sleep(20)
