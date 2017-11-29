class Command(object):
    def __init__(self):
        self.__type = 0
        self.__data_length = 0
        self.__data = bytes()

    def set_type(self, command_type):
        self.__type = command_type

    def get_type(self):
        return self.__type

    def set_data_length(self, data_length):
        self.__data_length = data_length

    def get_data_length(self):
        return self.__data_length

    def set_data(self, data):
        self.__data = data

    def get_data(self):
        return self.__data
