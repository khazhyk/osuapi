try:
    import asyncio
except ImportError:
    pass
from .model import User, Score, JsonList
from . import endpoints


class OsuApi:
    def __init__(self, key, *, connector):
        """
        Pass requests or aiohttp or anything that implements get (session, etc)
        """
        self.connector = connector
        self.key = key

        self._process = self._process_sync
        try:
            asyncio
            self._process = self._process_unk
        except NameError:
            pass

    def _create_request(self, endpoint, data):
        return self.connector.get(endpoint, params=data)

    def _process_sync(self, resp, type_):
        data = resp.json()
        return type_(data)

    async def _process_async(self, resp, type_):
        resp = await resp
        data = await resp.json()
        return type_(data)

    def _process_unk(self, resp, type_):
        if (asyncio.iscoroutine(resp)):
            self._process = self._process_async
        else:
            self._process = self._process_sync
        return self._process(resp, type_)

    def _make_req(self, endpoint, data, type_):
        return self._process(self._create_request(endpoint, data), type_)

    def get_user(self, username, *, type="string", mode=0):
        return self._make_req(endpoints.USER, dict(
            k=self.key,
            u=username,
            type=type,
            m=mode
            ), JsonList(User))

    def get_user_best(self, username, *, type="string", mode=0):
        return self._make_req(endpoints.USER_BEST, dict(
            k=self.key,
            u=username,
            type=type,
            m=mode
            ), JsonList(Score))
