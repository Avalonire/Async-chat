import json
from socket import *
import time
import argparse

parser = argparse.ArgumentParser(description="port and address")

parser.add_argument("-a", dest="addr", required=True)
parser.add_argument("-p", dest="port", default=7777, type=int)

args = parser.parse_args()


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((args.addr, args.port))

    presence_msg = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": "Avalon",
            "status": "I'm here!"
        }
    }

    msg_enc = json.dumps(presence_msg).encode('utf-8')
    s.send(msg_enc)
    data = s.recv(10000)
    data_decoded = json.loads(data.decode('utf-8'))
    print('Сервер: ', data_decoded['response'])


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
