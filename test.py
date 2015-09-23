import unittest
from main import AsyncRequestHandler
import collections


class TestAsyncRequestHandler(unittest.TestCase):

    def setUp(self):
        self.hdl = AsyncRequestHandler()
        self._url_list = ['google.com', 'yahoo.com', 'abc.com']

    def test_load_from_list_loads_list(self):
        self.hdl.load_from_list(self._url_list)
        self.assertEqual(collections.Counter(self._url_list),
                         collections.Counter(self.hdl._url_list))

    def test_load_from_csv(self):
        test_list = ['google.com', 'facebook.com', 'youtube.com']
        csv_file = 'alexa.csv'
        self.hdl.load_from_csv(csv_file, 3)
        self.assertEqual(self.hdl.get_urls(), test_list)

    def test_add_subdomain(self):
        self.hdl.add_subdomain('blog')
        self.assertIn('blog', self.hdl._subdomains)

    def test_add_existing_subdomain(self):
        self.hdl.add_subdomain('www')
        self.assertEqual(len(self.hdl._subdomains), 1)

    def test_get_status(self):
        code = yield from self.hdl._get_status('http://google.com/')
        self.assertEqual(code, 200)


if __name__ == '__main__':
    unittest.main()
