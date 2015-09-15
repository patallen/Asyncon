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

logfile = open('codes.log', 'w')
@asyncio.coroutine
def coroutine(url):
    code = '000' 
    furl = 'http://{}/'.format(url)
    print('Starting {}'.format(furl))
    try:
        res = yield from asyncio.wait_for(aiohttp.request('GET', furl), 10)
        code = res.status
        yield from res.read_and_close()
    except Exception as e:
        logfile.write('URL: {1} Error: {0}\n'.format(e, url))

    print(code)



if __name__ == '__main__':
    f = FaviconSeeder()
    f.load_from_csv('alexa.csv', 1000)
    tasks = [coroutine(url) for url in f.get_urls()]

    start = datetime.datetime.now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.stop()
    loop.run_forever()
    loop.close()
    stop = datetime.datetime.now()
    time = stop-start

    print('TIME: {}'.format(time))
    print('EST: {}'.format(time * (200000/1000)))
