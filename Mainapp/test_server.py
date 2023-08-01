import unittest
import time
from server import get_params, run_socket, get_msg
from socket import socket, AF_INET, SOCK_STREAM
import json
import threading


class TestServerFunctions(unittest.TestCase):
    def setUp(self):
        print(f'Старт теста {time.time()}')

    def tearDown(self):
        print(f'Окончание теста {time.time()}')

    def test_default_get_params(self):
        self.assertEqual((get_params().addr, get_params().port), ('', 7777))

    def test_run_socket(self):
        s = run_socket('localhost', 7777)
        self.assertTrue(s)
        s.close()

    # def test_get_msg(self):
    #     s = socket(AF_INET, SOCK_STREAM)
    #     s.bind(('localhost', 44444))
    #     s.listen(1)
    #     client, addr = s.accept()
    #     s2 = socket(AF_INET, SOCK_STREAM)
    #     s2.connect(('localhost', 44444))
    #     s2.send(json.dumps('TEST_MESSAGE').encode('utf-8'))
    #     self.assertEqual(get_msg(client), 'TEST_MESSAGE')


if __name__ == '__main__':
    unittest.main()
