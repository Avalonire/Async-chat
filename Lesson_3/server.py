import json
from socket import *
from json_msgs import response_200_msg
import argparse
import logging
import server_log_config

logger = logging.getLogger('server')


def get_params():
    parser = argparse.ArgumentParser(description="port and address")

    parser.add_argument("-a", dest="addr", default='')
    parser.add_argument("-p", dest="port", default=7777, type=int)

    args = parser.parse_args()
    return args


def run_socket(addr, port, listen_num: int = None):
    logger.debug('Реализация сокета %s, порт: %d', addr, port)
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    if listen_num:
        s.listen(listen_num)
    return s


def get_client(params):
    logger.debug('подключение клиента %s, порт: %d', params.addr, params.port)
    client, addr = run_socket(params.addr, params.port, 5).accept()
    return client


def get_msg(client):
    logger.info('получение сообщения от клиента')
    print('Получаем запрос на соединение:', client)
    data = client.recv(100000)
    data_decoded = json.loads(data.decode('utf-8'))
    print('Было получено сообщение: ', data_decoded)
    if data_decoded['action'] == 'quit':
        client.close()
        return
    if data_decoded['action'] == 'presence':
        logger.info('отправка ответа клиенту')
        msg = response_200_msg
        client.send(json.dumps(msg).encode('utf-8'))
    return data_decoded


def main():
    params = get_params()
    client = get_client(params)
    get_msg(client)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e)
