import csv
import asyncio
import aiohttp
import datetime

CONCURRENT_REQUESTS = 15
REQ_TIMEOUT = 3


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
def get_status(url, semaphore):
    code = '000' 
    with (yield from semaphore):
        try:
            furl = 'http://{}/'.format(url)
            res = yield from asyncio.wait_for(aiohttp.get(furl), REQ_TIMEOUT)
            res.close()
            code = res.status
        except:
            pass

    print(str(code) + ":" + url)


def main():
    sem = asyncio.Semaphore(CONCURRENT_REQUESTS)
    f = FaviconSeeder()
    f.load_from_csv('alexa.csv', 400)
    urls =  f.get_urls()

    coros = []
    for url in urls:
        coros.append(asyncio.async(get_status(url, sem)))
    yield from asyncio.gather(*coros)


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop._default_executor.shutdown(wait=True)
    loop.close()
    elapsed_time = datetime.datetime.now()-start_time

    print('TIME: {}'.format(elapsed_time))
    print('EST: {}'.format(elapsed_time * (200000/400)))
