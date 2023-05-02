import unittest
from client import get_params


class TestServerFunctions(unittest.TestCase):
    def test_default_get_params(self):
        self.assertEqual((get_params().addr, get_params().port), ('', 7777))


if __name__ == '__main__':
    unittest.main()
