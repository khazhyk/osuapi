from .model import User, BeatmapScore, RecentScore, Score, SoloScore, JsonList, OsuMode, Beatmap, Match
from . import endpoints
from .connectors import *
import warnings

def _username_type(username):
    if username is None:
        return None
    return "id" if isinstance(username, int) else "string"

class OsuApi:
    """osu! api client.

    Parameters
    ----------
    key
        The osu! api key used for authorization.
    connector
        The osuapi connector used for making requests. The library comes with
        two implementations, :class:`osuapi.connectors.AHConnector` for using aiohttp, and
        :class:`osuapi.connectors.ReqConnector` for using requests."""

    def __init__(self, key, *, connector):
        self.connector = connector
        self.key = key

    def close(self):
        self.connector.close()

    def _make_req(self, endpoint, data, type_):
        return self.connector.process_request(endpoint, {k: v for k, v in data.items() if v is not None}, type_)

    def get_user(self, username, *, mode=OsuMode.osu, event_days=31):
        """Get a user profile.

        Parameters
        ----------
        username : str or int
            A `str` representing the user's username, or an `int` representing the user's id.
        mode : :class:`osuapi.enums.OsuMode`
            The osu! game mode for which to look up. Defaults to osu!standard.
        event_days : int
            The number of days in the past to look for events. Defaults to 31 (the maximum).
        """
        return self._make_req(endpoints.USER, dict(
            k=self.key,
            u=username,
            type=_username_type(username),
            m=mode.value,
            event_days=event_days
            ), JsonList(User))

    def get_user_best(self, username, *, mode=OsuMode.osu, limit=50):
        """Get a user's best scores.

        Parameters
        ----------
        username : str or int
            A `str` representing the user's username, or an `int` representing the user's id.
        mode : :class:`osuapi.enums.OsuMode`
            The osu! game mode for which to look up. Defaults to osu!standard.
        limit
            The maximum number of results to return. Defaults to 50, maximum 100.
        """
        return self._make_req(endpoints.USER_BEST, dict(
            k=self.key,
            u=username,
            type=_username_type(username),
            m=mode.value,
            limit=limit
            ), JsonList(SoloScore))

    def get_user_recent(self, username, *, mode=OsuMode.osu, limit=10):
        """Get a user's most recent scores, within the last 24 hours.

        Parameters
        ----------
        username : str or int
            A `str` representing the user's username, or an `int` representing the user's id.
        mode : :class:`osuapi.enums.OsuMode`
            The osu! game mode for which to look up. Defaults to osu!standard.
        limit
            The maximum number of results to return. Defaults to 10, maximum 50.
        """
        return self._make_req(endpoints.USER_RECENT, dict(
            k=self.key,
            u=username,
            type=_username_type(username),
            m=mode.value,
            limit=limit
            ), JsonList(RecentScore))

    def get_scores(self, beatmap_id, *, username=None, mode=OsuMode.osu, mods=None, limit=50):
        """Get the top scores for a given beatmap.

        Parameters
        ----------
        beatmap_id
            Individual Beatmap ID to lookup.
        username : str or int
            A `str` representing the user's username, or an `int` representing the user's id. If specified, restricts returned scores to the specified user.
        mode : :class:`osuapi.enums.OsuMode`
            The osu! game mode for which to look up. Defaults to osu!standard.
        mods : :class:`osuap:class:`osuapi.enums.OsuMod`
            If specified, restricts returned scores to the specified mods.
        limit
            Number of results to return. Defaults to 50, maximum 100.
        """
        return self._make_req(endpoints.SCORES, dict(
            k=self.key,
            b=beatmap_id,
            u=username,
            type=_username_type(username),
            m=mode.value,
            mods=mods.value if mods else None,
            limit=limit), JsonList(BeatmapScore))

    def get_beatmaps(self, *, since=None, beatmapset_id=None, beatmap_id=None, username=None, mode=None,
                     include_converted=False, beatmap_hash=None, limit=500):
        """Get beatmaps.

        Parameters
        ----------
        since : datetime
            If specified, restrict results to beatmaps *ranked* after this date.
        beatmapset_id
            If specified, restrict results to a specific beatmap set.
        beatmap_id
            If specified, restrict results to a specific beatmap.
        username : str or int
            A `str` representing the user's username, or an `int` representing the user's id.
            If specified, restrict results to a specific user.
        mode : :class:`osuapi.enums.OsuMode`
            If specified, restrict results to a specific osu! game mode.
        include_converted : bool
            Whether or not to include autoconverts. Defaults to false.
        beatmap_hash
            If specified, restricts results to a specific beatmap hash.
        limit
            Number of results to return. Defaults to 500, maximum 500.
        """
        return self._make_req(endpoints.BEATMAPS, dict(
            k=self.key,
            s=beatmapset_id,
            b=beatmap_id,
            u=username,
            since="{:%Y-%m-%d %H:%M:%S}".format(since) if since is not None else None,
            type=_username_type(username),
            m=mode.value if mode else None,
            a=int(include_converted),
            h=beatmap_hash,
            limit=limit
            ), JsonList(Beatmap))

    def get_match(self, match_id):
        """Get a multiplayer match.

        Parameters
        ----------
        match_id
            The ID of the match to retrieve. This is the ID that you see in a online multiplayer match summary.
            This does not correspond the in-game game ID."""
        return self._make_req(endpoints.MATCH, dict(
            k=self.key,
            mp=match_id), Match)
