import json
import sys
from socket import *
from json_msgs import presence_msg
import argparse
import logging
import client_log_config
from log_decor import logged
import threading
from time import sleep

logger = logging.getLogger('client')


@logged(name='client')
def get_params():
    parser = argparse.ArgumentParser(description="port and address")

    parser.add_argument("-a", dest="addr", default='localhost')
    parser.add_argument("-p", dest="port", default=7777, type=int)
    args = parser.parse_args()
    return args


# @logged(name='client')
# def connect_socket(addr, port):
#     s = socket(AF_INET, SOCK_STREAM)
#     s.connect((addr, port))
#     # logger.debug('Соединение с сервером %s, порт: %d', addr, port)
#     return s


@logged(name='client')
def main():
    try:
        s = socket(AF_INET, SOCK_STREAM)
        params = get_params()
        s.connect((params.addr, params.port))
        msg_enc = json.dumps(presence_msg).encode('utf-8')
        logger.info('отправка сообщения от клиента')
        s.send(msg_enc)
        logger.info('сообщение от клиента отправлено')
        data = s.recv(10000)
        data_decoded = json.loads(data.decode('utf-8'))
        print('Сервер: ', data_decoded['response'])
    except (ConnectionRefusedError, ConnectionError):
        logger.error(ConnectionError, ConnectionRefusedError)
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error('Формат JSON не распознан')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=data_decoded, args=(s, params.name))
        receiver.daemon = True
        receiver.start()
        while True:
            sleep(1)
            if receiver.is_alive():
                continue
            break


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e)
