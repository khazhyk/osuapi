"""osu! api client."""

from .model import User, SoloScore, JsonList, OsuMode, Beatmap, Match
from . import endpoints
from .connectors import *
import warnings


class OsuApi:
    """osu! api client."""

    def __init__(self, key, *, connector):
        """Pass requests or aiohttp or anything that implements get (session, etc)."""

        if not hasattr(connector, "process_request"):
            # dirty backwards compatability
            try:
                import aiohttp
                if connector is aiohttp or isinstance(connector, aiohttp.ClientSession):
                    connector = AHConnector(connector)
                    warnings.warn("Connector should now be a connector class, not aiohttp or a ClientSession directly. See use osuapi.AHConnector", Warning)
            except ImportError:
                pass
            try:
                import requests
                if connector is requests or isinstance(connector, requests.Session):
                    connector = ReqConnector(connector)
                    warnings.warn("Connector should now be a connector class, not requests or a Session directly. See use osuapi.ReqConnector", Warning)
            except ImportError:
                pass

        self.connector = connector
        self.key = key

    def _make_req(self, endpoint, data, type_):
        return self.connector.process_request(endpoint, data, type_)

    @staticmethod
    def _username_type(username):
        if username is None:
            return None
        return "int" if isinstance(username, int) else "string"

    def get_user(self, username, *, mode=OsuMode.osu):
        """get a user's information.

        :username may be a string representing the player's username, or an int representing the id.
        :mode for which osu mode to look up
        """
        return self._make_req(endpoints.USER, dict(
            k=self.key,
            u=username,
            type=self._username_type(username),
            m=mode.value
            ), JsonList(User))

    def get_user_best(self, username, *, mode=OsuMode.osu, limit=50):
        """get a user's best scores.

        :username as in get_user
        :mode as in get_user
        :limit defaults to 50, number of results to return
        """
        return self._make_req(endpoints.USER_BEST, dict(
            k=self.key,
            u=username,
            type=self._username_type(username),
            m=mode.value,
            limit=limit
            ), JsonList(SoloScore))

    def get_user_recent(self, username, *, mode=OsuMode.osu, limit=10):
        """get a user's most recent scores.

        :username as in get_user
        :mode as in get_user
        :limit defaults to 10, max 50
        """
        return self._make_req(endpoints.USER_RECENT, dict(
            k=self.key,
            u=username,
            type=self._username_type(username),
            m=mode.value,
            limit=limit
            ), JsonList(Score))

    def get_scores(self, beatmap_id, *, username=None, mode=OsuMode.osu, mods=None, limit=50):
        """get top scores for a given beatmap.

        :beatmap_id must be a valid beatmap (not beatmapset) id.
        :username may be optionally provided to get a specific user's score
        :mode as in get_user
        :mods may be optionally provided to get a scores with specific mods enabled
        :limit number of results to return
        """
        return self._make_req(endpoints.SCORES, dict(
            k=self.key,
            b=beatmap_id,
            u=username,
            type=self._username_type(username),
            m=mode.value,
            mods=mods,
            limit=limit), JsonList(Score))

    def get_beatmaps(self, *, since=None, beatmapset_id=None, beatmap_id=None, username=None, mode=OsuMode.osu,
                     include_converted=False, beatmap_hash=None, limit=500):
        """get beatmaps.

        :since only get beatmaps after this date
        :beatmapset_id get betamaps for a specific set
        :beatmap_id get a specific beatmap
        :username get beatmaps by a specific user
        :mode which mode of osu to get a beatmap for
        :include_converted include autoconverts (default false)
        :beatmap_hash get a beatmap by it's hash
        :limit number of results to return
        """
        return self._make_req(endpoints.BEATMAPS, dict(
            k=self.key,
            s=beatmapset_id,
            b=beatmap_id,
            u=username,
            type=self._username_type(username),
            m=mode.value,
            a=include_converted,
            h=beatmap_hash,
            limit=limit
            ), JsonList(Beatmap))

    def get_match(self, match_id):
        """get a multiplayer match.

        :match_id the id of the match to retrieve"""
        return self._make_req(endpoints.MATCH, dict(
            k=self.key,
            mp=match_id), Match)
