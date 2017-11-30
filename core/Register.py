import os

from core.Command import Command


def gethostname():
    sys = os.name
    if sys == 'nt':
        hostname = os.getenv('computername')
        return hostname
    elif sys == 'posix':
        host = os.popen('echo $HOSTNAME')
        try:
            hostname = host.read()
            return hostname
        finally:
            host.close()
    else:
        return 'Unkwon hostname'


class Register(object):
    def __init__(self, client):
        self.__client = client

    def register(self):
        device_name = gethostname()
        command = Command()
        command.set_type(0x10000001)
        command.set_target(0x00000000)
        command.set_data_length(len(device_name.encode('utf-8')))
        command.set_data(device_name.encode('utf-8'))
        self.__client.send_command(command)
