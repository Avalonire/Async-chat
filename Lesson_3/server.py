import json
from socket import *

from metaclasses import ServerVerifier
from json_msgs import response_200_msg
from database import Storage
import argparse
import logging
import server_log_config
from log_decor import logged
import select


logger = logging.getLogger('server')


@logged(name='server')
def get_params():
    parser = argparse.ArgumentParser(description="port and address")

    parser.add_argument("-a", dest="addr", default='')
    parser.add_argument("-p", dest="port", default=7777, type=int)

    args = parser.parse_args()
    return args


class DescriptorPort:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f'Server can not approve {value} port. Allowed address: from 1024 to 65535')
            exit(1)
        else:
            instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Server(metaclass=ServerVerifier):
    port = DescriptorPort()

    def __init__(self, address, port, database):
        self.socket = None
        self.addr = address
        self.port = port
        self.clients = []
        self.database = database

    @logged(name='server')
    def get_msg(self, client):
        # logger.info('получение сообщения от клиента')
        print('Получаем запрос на соединение:', client)
        data = client.recv(100000)
        data_decoded = json.loads(data.decode('utf-8'))
        print('Было получено сообщение: ', data_decoded)
        if data_decoded['action'] == 'quit':
            client.close()
            return
        if data_decoded['action'] == 'presence':
            # logger.info('отправка ответа клиенту')
            msg = response_200_msg
            client.send(json.dumps(msg).encode('utf-8'))
        return data_decoded

    @logged(name='server')
    def socket_init(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.addr, self.port))
        s.settimeout(0.5)
        s.listen(10)
        self.socket = s

    def main(self):
        self.socket_init()

        while True:
            try:
                client, client_address = self.socket.accept()
            except OSError:
                pass
            else:
                self.clients.append(client)
                client_ip, client_port = client.getpeername()
                self.database.user_login(client, client_ip, client_port)
            recv_data_lst = []

            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass
            if recv_data_lst:
                for client in recv_data_lst:
                    try:
                        self.get_msg(client)
                    except Exception:
                        self.clients.remove(client)
                        self.database.user_logout(client)


if __name__ == '__main__':
    try:
        database = Storage()
        params = get_params()
        server = Server(params.addr, params.port, database)
        server.main()
    except Exception as e:
        logger.error(e)
    with open('logs/module.log', 'a', encoding='utf-8') as f:
        f.write('-' * 100 + '\n')
