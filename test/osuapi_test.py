import os
import unittest

import osuapi


class OsuApiTest(unittest.TestCase):

    def setUp(self):
        self.api = osuapi.OsuApi(
            key=os.environ['OSU_API_KEY'],
            connector=osuapi.ReqConnector())

    def test_get_user(self):
        self.api.get_user("peppy")

    def test_get_user_best(self):
        self.api.get_user_best("peppy")

    def test_get_user_recent(self):
        self.api.get_user_recent("peppy")

    def test_get_scores(self):
        self.api.get_scores(774965, username="cookiezi")

    def test_get_beatmaps(self):
        self.api.get_beatmaps(limit=1)
