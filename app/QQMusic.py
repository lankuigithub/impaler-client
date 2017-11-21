import os
from pykeyboard import PyKeyboard


class QQMusic(object):
    def __init__(self):
        self.__k = PyKeyboard()

    def start(self):
        os.system('open /Applications/QQMusic.app')

    def play_pause(self):
        self.__k.press_keys(['Control', 'Command', self.__k.space])

    def next(self):
        self.__k.press_keys(['Control', 'Command', '.'])

    def prev(self):
        self.__k.press_keys(['Control', 'Command', ','])

    def volume_up(self):
        self.__k.press_keys(['Control', 'Command', ';'])

    def volume_down(self):
        self.__k.press_keys(['Control', 'Command', "'"])

    def mini(self):
        self.__k.press_keys(['Control', 'Command', 's'])

    def run(self, command):
        if command == 'start':
            self.start()
        elif command == 'play' or command == 'pause':
            self.play_pause()
        elif command == 'next':
            self.next()
        elif command == 'prev':
            self.prev()
        elif command == 'mini':
            self.mini()
        elif command == '+':
            self.volume_up()
        elif command == '-':
            self.volume_down()
