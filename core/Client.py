# -*- coding: UTF-8 -*-

import socket
import struct
import threading
import time

from core.Command import Command


class Client(object):
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__mutex = threading.Lock()
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect((self.__ip, self.__port))
        self.__socket = _socket
        self.heartbeat()
        self.__data = bytes()
        self.__headerSize = 8
        self.__delimiter = 'IMPALER'
        self.__delimiter_bytes = self.__delimiter.encode('utf-8')

    def receive(self):
        self.__data += self.__socket.recv(1024)
        if len(self.__data) < self.__headerSize:
            return ''
        command_type = struct.unpack("!i", self.__data[:4])[0]
        data_length = struct.unpack("!i", self.__data[4:8])[0]
        if len(self.__data) < self.__headerSize + data_length + len(self.__delimiter_bytes):
            return ''
        command_data = self.__data[self.__headerSize: self.__headerSize + data_length]
        self.__data = self.__data[self.__headerSize + data_length + len(self.__delimiter_bytes):len(self.__data)]
        command = Command()
        command.set_type(command_type)
        command.set_data_length(data_length)
        command.set_data(command_data)
        return command

    def send_command(self, command):
        self.__mutex.acquire()
        self.__socket.send(struct.pack("!i", command.get_type()))
        self.__socket.send(struct.pack("!i", command.get_data_length()))
        self.__socket.send(command.get_data())
        self.__socket.send('IMPALER'.encode('utf-8'))
        self.__mutex.release()

    def heartbeat(self):
        t = threading.Thread(target=self.send_ping, name='HeartbeatThread')
        t.start()

    def send_ping(self):
        while True:
            command = Command()
            command.set_type(0)
            command.set_data_length(0)
            command.set_data(bytes())
            self.send_command(command)
            time.sleep(20)
