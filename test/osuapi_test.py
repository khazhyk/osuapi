import os
import unittest
import warnings
import osuapi
import osuapi.dictmodel

class OsuApiTest(unittest.TestCase):

    def setUp(self):
        self.api = osuapi.OsuApi(
            key=os.environ['OSU_API_KEY'],
            connector=osuapi.ReqConnector())
        warnings.simplefilter("error")

    def test_get_user(self):
        res = self.api.get_user("khazhyk")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    def test_get_user_best(self):
        res = self.api.get_user_best("khazhyk")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    def test_get_user_recent(self):
        res = self.api.get_user_recent("khazhyk")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    def test_get_scores(self):
        res = self.api.get_scores(774965, username="cookiezi")

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)

    def test_get_beatmaps(self):
        res = self.api.get_beatmaps(limit=1)

        for k, v in dict(res[0]).items():
            self.assertFalse(isinstance(v, osuapi.dictmodel.Attribute), k)
