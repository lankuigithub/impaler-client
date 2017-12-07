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
        hostname = gethostname().replace("\n", "")
        message = '{"code":0,"msg":"request","data":{"name":"' + hostname + '"}}'
        print(message)
        command = Command()
        command.set_type(0x00000006)
        command.set_target(0x00000000)
        command.set_data_length(len(message.encode('utf-8')))
        command.set_data(message.encode('utf-8'))
        self.__client.send_command(command)
