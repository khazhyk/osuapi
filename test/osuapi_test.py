import asyncio
import os
import unittest
import warnings

import osuapi
import osuapi.dictmodel


def async_test(f):
    def wrapper(*args, **kwargs):
        coro = f(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(coro)
    return wrapper


class OsuApiTest(unittest.TestCase):

    def setUp(self):
        self.api = osuapi.OsuApi(
            key=os.environ['OSU_API_KEY'],
            connector=osuapi.ReqConnector())
        warnings.simplefilter("error")

    def tearDown(self):
        self.api.close()

    def test_get_user(self):
        res = self.api.get_user("cookiezi")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    def test_get_user_best(self):
        res = self.api.get_user_best("khazhyk")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    def test_get_user_recent(self):
        for usr in ["cookiezi", "filsdelama", "Vaxei", 39828, "Azer"]:
            res = self.api.get_user_recent(usr)
            if res:
                break
        if not res:
            self.skipTest("No one plays this game anymore.")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    def test_get_scores(self):
        res = self.api.get_scores(774965, username="cookiezi")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    def test_get_loved_scores(self):
        res = self.api.get_scores(1343925, username=39828)

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)


    def test_get_beatmaps(self):
        res = self.api.get_beatmaps(limit=1)

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)


class OsuApiAsyncTest(unittest.TestCase):

    def setUp(self):
        self.api = osuapi.OsuApi(
            key=os.environ['OSU_API_KEY'],
            connector=osuapi.AHConnector())
        # aiohttp can't decide if close() is a coro or not
        warnings.simplefilter("ignore")

    def tearDown(self):
        self.api.close()

    @async_test
    async def test_get_user(self):
        res = await self.api.get_user("cookiezi")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    @async_test
    async def test_get_user_best(self):
        res = await self.api.get_user_best("khazhyk")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    @async_test
    async def test_get_user_recent(self):
        for usr in ["cookiezi", "filsdelama", "Vaxei", 39828, "Azer"]:
            res = await self.api.get_user_recent(usr)
            if res:
                break
        if not res:
            self.skipTest("No one plays this game anymore.")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    @async_test
    async def test_get_scores(self):
        res = await self.api.get_scores(774965, username="cookiezi")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    @async_test
    async def test_get_loved_scores(self):
        res = await self.api.get_scores(1343925, username=39828)

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    @async_test
    async def test_get_beatmaps(self):
        res = await self.api.get_beatmaps(limit=1)

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)
