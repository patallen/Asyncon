import csv
import asyncio
import aiohttp
import datetime
import concurrent


class AsyncRequestHandler:

    def __init__(self):
        self._url_list = []
        self._results = []
        self._concurrent_requests = 50
        self._req_timeout = 4
        self._num_retries = 3
        self._subdomains = ['www']
        self._connector = aiohttp.TCPConnector(verify_ssl=False)

    def load_from_csv(self, csvfile, limit):
        with open(csvfile) as csvfile:
            r = csv.reader(csvfile, delimiter=',')
            self._url_list = [row[1] for row in r][:limit]

    def get_urls(self):
        return self._url_list

    def add_subdomain(self, subdomain):
        # Check that the sub domain does not exist
        if subdomain not in self._subdomains:
            self._subdomains.append(subdomain)
        else:
            print('Subdomain already loaded.')

    @asyncio.coroutine
    def _get_status(self, url, semaphore):
        code = '000'
        subs = ['']
        [subs.append('{}.'.format(sub)) for sub in self._subdomains]
        con = self._connector
        timeout = self._req_timeout

        with (yield from semaphore):
            for sub in subs:
                try:
                    furl = 'http://{}{}/'.format(sub, url)
                    res = yield from asyncio.wait_for(aiohttp.get(furl, connector=con), timeout)
                    res.close()
                    code = res.status
                    break
                except:
                    pass
        self._results.append(code)
        print(str(code) + ":" + url)

    def get_results(self):
        status_ok = 0
        total = 0
        status_none = 0
        status_other = 0

        for result in self._results:
            total += 1
            if result == '000':
                status_none += 1
            elif result == 200:
                status_ok += 1
            else:
                status_other += 1
        print('Total: {}'.format(total))
        print('200 : {0} : {1}'.format(status_ok, (status_ok / total * 100)))
        print('000 : {0} : {1}'.format(status_none, (status_none / total * 100)))

    def run(self):
        sem = asyncio.Semaphore(self._concurrent_requests)
        loop = asyncio.get_event_loop()

        coros = []
        for url in self._url_list:
            coros.append(asyncio.async(self._get_status(url, sem)))

        start_time = datetime.datetime.now()

        executor = concurrent.futures.ThreadPoolExecutor(10)
        loop.set_default_executor(executor)
        loop.run_until_complete(asyncio.wait(coros))
        executor.shutdown(wait=True)
        time_elapsed = datetime.datetime.now() - start_time
        est_time = time_elapsed * 200000 / len(coros)
        self._connector.close()
        loop.close()

        # Print results
        print('Elapsed: {}'.format(time_elapsed))
        print('Estimated: {}'.format(est_time))
        self.get_results()


if __name__ == '__main__':
    handler = AsyncRequestHandler()
    handler.load_from_csv('alexa.csv', 400)
    handler.run()
