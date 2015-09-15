import csv
import asyncio
import aiohttp
import datetime


class FaviconSeeder:
    _url_list = []
    _results = []

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def load_from_csv(self, csvfile, limit):
        with open(csvfile) as csvfile:
            r = csv.reader(csvfile, delimiter=',')
            self._url_list = [row[1] for row in r][:limit]

    def get_urls(self):
        return self._url_list


@asyncio.coroutine
def coroutine(url):
    code = 0
    furl = 'http://{}/'.format(url)
    try:
        res = yield from aiohttp.request('GET', furl)
        code = res.status
        res.close()
    except:
        pass
    print(code)
    return code


if __name__ == '__main__':
    f = FaviconSeeder()
    f.load_from_csv('alexa.csv', 800)
    tasks = [coroutine(url) for url in f.get_urls()]

    loop = asyncio.get_event_loop()
    start = datetime.datetime.now()
    loop.run_until_complete(asyncio.wait(tasks))
    stop = datetime.datetime.now()
    loop.close()
    print(stop-start)
