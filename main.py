import csv
import asyncio
import aiohttp
import datetime

CONCURRENT_REQUESTS = 15
REQ_TIMEOUT = 3


class AsyncRequestHandler:
    _url_list = []
    _results = []

    def __init__(self):
        self._concurrent_requests = 15
        self._req_timeout = 3

    def load_from_csv(self, csvfile, limit):
        with open(csvfile) as csvfile:
            r = csv.reader(csvfile, delimiter=',')
            self._url_list = [row[1] for row in r][:limit]

    def get_urls(self):
        return self._url_list

    @asyncio.coroutine
    def _get_status(self, url, semaphore):
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

    def run(self):
        sem = asyncio.Semaphore(self._concurrent_requests)
        loop = asyncio.get_event_loop()

        coros = []
        for url in self._url_list:
            coros.append(asyncio.async(self._get_status(url, sem)))

        loop.run_until_complete(asyncio.wait(coros))
        loop._default_executor.shutdown(wait=True)
        loop.close()
