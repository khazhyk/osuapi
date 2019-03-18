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
    import inspect

    class AHConnector:
        """Connector implementation using aiohttp."""
        def __init__(self, sess=None, loop=None):
            self.loop = loop or asyncio.get_event_loop()
            self.sess = sess or aiohttp.ClientSession(loop=self.loop)
            self.closed = False

        def close(self):
            self.closed = True
            # there is no reason for sess.close to be a coroutine, and
            # in older versions of aiohttp, it isn't. In newer versions
            # close returns an awaitable whose only purpose is to warn you
            # if you don't await it, so... await it... I guess???
            aiohttp_is_silly = self.sess.close()
            if inspect.isawaitable(aiohttp_is_silly):
                asyncio.ensure_future(aiohttp_is_silly)

        @asyncio.coroutine
        def process_request(self, endpoint, data, type_, retries=5):
            """Make and process the request.

            This can raise anything aiohttp.get() can raise, or
            osuapi.HTTPError if we run out of retries.

            Parameters
            -----------
            endpoint : `str`
                The HTTP endpoint to make a request to
            data : `dict`
                The parameters for making the HTTP request
            type_ : `type`
                A converter to which to pass the response json and return.
            retries: `int`
                Maximum number of times to try request.
            """

            while retries:
                resp = yield from self.sess.get(endpoint, params=data)
                try:
                    if resp.status == 200:
                        data = yield from resp.json()
                        return type_(data)
                    elif resp.status == 504:
                        # Retry on 504
                        retries -= 1
                        yield from asyncio.sleep(1)
                    else:
                        break
                finally:
                    if not retries or resp.status not in {200, 504}:
                        error_text = yield from resp.text()
                    resp.close()
            raise HTTPError(resp.status, resp.reason, error_text)
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

            This can raise anything requests.get() can raise, or
            osuapi.HTTPError if we run out of retries.

            Parameters
            -----------
            endpoint : `str`
                The HTTP endpoint to make a request to
            data : `dict`
                The parameters for making the HTTP request
            type_ : `type`
                A converter to which to pass the response json and return.
            retries: `int`
                Maximum number of times to try request.
            """
            while retries:
                resp = self.sess.get(endpoint, params=data)
                try:
                    if resp.status_code == 200:
                        return type_(resp.json())
                    elif resp.status_code == 504:
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
