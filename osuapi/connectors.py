from .errors import HTTPError

try:
    import aiohttp

    class AHConnector:
        def __init__(self, sess=None):
            self.sess = sess or aiohttp

        async def _process_request(self, endpoint, data, type_):
            resp = await self.sess.get(endpoint, params=data)
            if resp.code != 200:
                raise HTTPError(resp.status, resp.reason, await resp.text())
            data = await resp.json()
            return type_(data)

        def process_request(self, *args, **kw):
            return self._process_request(self, *args, **kw)
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
