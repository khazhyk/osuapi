"""Build in connectors.


Connectors have to implement `process_request`.
"""
from .errors import HTTPError

try:
    import aiohttp
    import asyncio

    class AHConnector:
        """Connector implementation using aiohttp."""
        def __init__(self, sess=None, loop=None):
            self.loop = loop or asyncio.get_event_loop()
            self.sess = sess or aiohttp.ClientSession(loop=self.loop)
            self.closed = False

        def __del__(self):
            if not self.closed:
                self.close()

        def close(self):
            self.closed = True
            self.sess.close()

        @asyncio.coroutine
        def process_request(self, endpoint, data, type_):
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
            resp = yield from self.sess.get(endpoint, params=data)
            if resp.status != 200:
                raise HTTPError(resp.status, resp.reason, (yield from resp.text()))
            data = yield from resp.json()
            resp.close()
            return type_(data)
except ImportError:
    pass

try:
    import requests

    class ReqConnector:
        """Connector implementation using requests."""
        def __init__(self, sess=None):
            self.sess = sess or requests.Session()

        def __del__(self):
            self.close()

        def close(self):
            self.sess.close()

        def process_request(self, endpoint, data, type_):
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
            resp = self.sess.get(endpoint, params=data)
            if resp.status_code != 200:
                raise HTTPError(resp.status_code, resp.reason, resp.text)
            data = resp.json()
            resp.close()
            return type_(data)
except ImportError:
    pass
