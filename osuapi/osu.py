try:
    import asyncio
except ImportError:
    pass
from .model import User, Score, JsonList, OsuMode, Beatmap
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

    @staticmethod
    def _username_type(username):
        if username is None:
            return None
        return "int" if isinstance(username, int) else "string"

    def get_user(self, username, *, mode=OsuMode.osu):
        return self._make_req(endpoints.USER, dict(
            k=self.key,
            u=username,
            type=self._username_type(username),
            m=mode
            ), JsonList(User))

    def get_user_best(self, username, *, mode=OsuMode.osu, limit=50):
        return self._make_req(endpoints.USER_BEST, dict(
            k=self.key,
            u=username,
            type=self._username_type(username),
            m=mode,
            limit=limit
            ), JsonList(Score))

    def get_scores(self, beatmap_id, *, username=None, mode=OsuMode.osu, mods=None, limit=50):
        return self._make_req(endpoints.SCORES, dict(
            k=self.key,
            b=beatmap_id,
            u=username,
            type=self._username_type(username),
            m=mode,
            mods=mods,
            limit=limit), JsonList(Score))

    def get_beatmaps(self, *, since=None, beatmapset_id=None, beatmap_id=None, username=None, mode=OsuMode.osu,
                     include_converted=False, beatmap_hash=None, limit=500):
        return self._make_req(endpoints.BEATMAPS, dict(
            k=self.key,
            s=beatmapset_id,
            b=beatmap_id,
            u=username,
            type=self._username_type(username),
            m=mode,
            a=include_converted,
            h=beatmap_hash,
            limit=limit
            ), JsonList(Beatmap))
