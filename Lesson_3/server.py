import json
from socket import *
import time
import argparse

parser = argparse.ArgumentParser(description="port and address")

parser.add_argument("-p", dest="port", default=7777, type=int)
parser.add_argument("-a", dest="addr", default='')

args = parser.parse_args()


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((args.addr, args.port))
    s.listen(5)

    client, addr = s.accept()
    print('Получаем запрос на соединение:', addr)

    data = client.recv(100000)
    data_decoded = json.loads(data.decode('utf-8'))
    print('Было получено сообщение: ', data_decoded)
    if data_decoded['action'] == 'quit':
        client.close()
        return
    if data_decoded['action'] == 'presence':
        re_msg = {
            "response": 200,
            "time": time.time(),
        }
        client.send(json.dumps(re_msg).encode('utf-8'))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
