import json
from socket import *
from json_msgs import response_200_msg
import argparse
import logging
import server_log_config
from log_decor import logged
import select

logger = logging.getLogger('server')


def get_params():
    parser = argparse.ArgumentParser(description="port and address")

    parser.add_argument("-a", dest="addr", default='')
    parser.add_argument("-p", dest="port", default=7777, type=int)

    args = parser.parse_args()
    return args


# @logged(name='server')
# def run_socket(addr, port, listen_num: int = None):
#     # logger.debug('Реализация сокета %s, порт: %d', addr, port)
#     s = socket(AF_INET, SOCK_STREAM)
#     s.bind((addr, port))
#     if listen_num:
#         s.listen(listen_num)
#     return s


# @logged(name='server')
# def get_client(params):
#     # logger.debug('подключение клиента %s, порт: %d', params.addr, params.port)
#     client, addr = run_socket(params.addr, params.port, 5).accept()
#     return client


@logged(name='server')
def get_msg(client):
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


def main():
    params = get_params()
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((params.addr, params.port))
    s.settimeout(0.5)
    s.listen(10)

    clients = []

    while True:
        try:
            client, client_address = s.accept()
        except OSError:
            pass
        else:
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass
        if recv_data_lst:
            for client in recv_data_lst:
                try:
                    get_msg(client)
                except Exception:
                    clients.remove(client)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e)
    with open('logs/module.log', 'a', encoding='utf-8') as f:
        f.write('-' * 100 + '\n')
