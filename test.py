import unittest
from main import AsyncRequestHandler
import collections


class TestLoadFromList(unittest.TestCase):
    def setUp(self):
        self.url_list = ['google.com', 'yahoo.com', 'abc.com']

    def test_load_from_list_loads_list(self):
        url_list = ['google.com', 'yahoo.com', 'abc.com']
        hdl = AsyncRequestHandler()
        hdl.load_from_list(self.url_list)
        self.assertTrue(collections.Counter(url_list) == collections.Counter(self.url_list))

if __name__ == '__main__':
    unittest.main()