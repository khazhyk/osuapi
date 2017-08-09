"""Build in connectors.


Connectors have to implement `process_request`.
"""
from .errors import HTTPError


def _bad_import_class(msg):
    class _BadImportClass:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError(msg)
    return _BadImportClass

try:
    import aiohttp
    import asyncio

    class AHConnector:
        """Connector implementation using aiohttp."""
        def __init__(self, sess=None, loop=None):
            self.loop = loop or asyncio.get_event_loop()
            self.sess = sess or aiohttp.ClientSession(loop=self.loop)
            self.closed = False

        def close(self):
            self.closed = True
            self.sess.close()

        @asyncio.coroutine
        def process_request(self, endpoint, data, type_, retries=5):
            """Make and process the request.

            Parameters
            -----------
            endpoint : `str`
                The HTTP endpoint to make a request to
            data : `dict`
                The parameters for making the HTTP request
            type_ : `type`
                A converter to which to pass the response json and return.
            """

            while retries:
                try:
                    resp = yield from self.sess.get(endpoint, params=data)
                    if resp.status == 200:
                        data = yield from resp.json()
                        return type_(data)
                    elif resp.status == 504 and retries:
                        # Retry on 504
                        retries -= 1
                        yield from asyncio.sleep(1)
                    else:
                        break
                finally:
                    resp.close()
            raise HTTPError(resp.status, resp.reason,
                            (yield from resp.text()))
except ImportError:
    AHConnector = _bad_import_class(
        "You need to install `aiohttp` to use osuapi.AHConenctor")

try:
    import requests
    import time

    class ReqConnector:
        """Connector implementation using requests."""
        def __init__(self, sess=None):
            self.sess = sess or requests.Session()

        def close(self):
            self.sess.close()

        def process_request(self, endpoint, data, type_, retries=5):
            """Make and process the request.

            Parameters
            -----------
            endpoint : `str`
                The HTTP endpoint to make a request to
            data : `dict`
                The parameters for making the HTTP request
            type_ : `type`
                A converter to which to pass the response json and return.
            """
            while retries:
                try:
                    resp = self.sess.get(endpoint, params=data)
                    if resp.status_code == 200:
                        return type_(resp.json())
                    elif resp.status_code == 504 and retries:
                        retries -= 1
                        time.sleep(1)
                    else:
                        break
                finally:
                    resp.close()
            raise HTTPError(resp.status_code, resp.reason, resp.text)
except ImportError:
    ReqConnector = _bad_import_class(
        "You need to install `requests` to use osuapi.ReqConnector")
