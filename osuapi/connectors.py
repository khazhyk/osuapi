from .errors import HTTPError

try:
    import aiohttp
    import asyncio

    class AHConnector:
        def __init__(self, sess=None):
            self.sess = sess or aiohttp

        @asyncio.coroutine
        def _process_request(self, endpoint, data, type_):
            resp = yield from self.sess.get(endpoint, params=data)
            if resp.status != 200:
                raise HTTPError(resp.status, resp.reason, (yield from resp.text()))
            data = yield from resp.json()
            return type_(data)

        def process_request(self, *args, **kw):
            return self._process_request(*args, **kw)
except ImportError:
    pass

try:
    import requests

    class ReqConnector:
        def __init__(self, sess=None):
            self.sess = sess or requests

        def process_request(self, endpoint, data, type_):
            resp = self.sess.get(endpoint, params=data)
            if resp.status_code != 200:
                raise HTTPError(resp.status_code, resp.reason, resp.text)
            data = resp.json()
            return type_(data)
except ImportError:
    pass
