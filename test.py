import unittest
from main import AsyncRequestHandler
import collections


class TestAsyncRequestHandler(unittest.TestCase):
    def setUp(self):
        self._url_list = ['google.com', 'yahoo.com', 'abc.com']

    def test_load_from_list_loads_list(self):
        hdl = AsyncRequestHandler()
        hdl.load_from_list(self._url_list)
        self.assertTrue(collections.Counter(self._url_list) == collections.Counter(hdl._url_list))

    def test_load_from_csv(self):
        hdl = AsyncRequestHandler()
        csv_file = 'alexa.csv'
        hdl.load_from_csv(csv_file, 3)
        self.assertTrue(len(hdl._url_list) == 3)

if __name__ == '__main__':
    unittest.main()
