import asyncio
import http
import multiprocessing
import unittest
import warnings

import osuapi


def async_test(f):
    def wrapper(*args, **kwargs):
        coro = f(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(coro)
    return wrapper


class FiveOhFourHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_error(504, "FiveOhFour")


def run_504_server():
    address = ('', 6969)
    httpd = http.server.HTTPServer(address, FiveOhFourHandler)
    httpd.serve_forever()


class AHConnectorTest(unittest.TestCase):
    def setUp(self):
        self.connector = osuapi.AHConnector()
        self.server = multiprocessing.Process(target=run_504_server)
        self.server.daemon = True
        self.server.start()
        # aiohttp can't decide if close() is a coro or not
        warnings.simplefilter("ignore")

    def tearDown(self):
        self.server.terminate()
        self.connector.close()

    @async_test
    async def test_fail_correctly_out_of_retries(self):
        with self.assertRaises(osuapi.HTTPError):
            res = await self.connector.process_request(
                "http://localhost:6969/504", {}, int, retries=3)


class ReqConnectorTest(unittest.TestCase):
    def setUp(self):
        self.connector = osuapi.ReqConnector()
        self.server = multiprocessing.Process(target=run_504_server)
        self.server.daemon = True
        self.server.start()

    def tearDown(self):
        self.server.terminate()
        self.connector.close()

    def test_fail_correctly_out_of_retries(self):
        with self.assertRaises(osuapi.HTTPError):
            res = self.connector.process_request(
                "http://localhost:6969/504", {}, int, retries=3)
