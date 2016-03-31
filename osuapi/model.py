import warnings
import datetime
from enum import Enum


def JsonList(oftype):
    class _:
        def __new__(cls, lis):
            return [oftype(entry) for entry in lis]
    return _


def Nullable(oftype):
    class _:
        def __new__(cls, it):
            if it is None:
                return None
            else:
                return oftype(it)
    return _


def PreProcessInt(oftype):
    class _:
        def __new__(cls, it):
            return oftype(int(it))
    return _


class JsonDateTime:
    def __new__(cls, val):
        return datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S")


class JsonObjWrapper:
    def __init__(self, dic):
        for k, v in dic.items():
            try:
                setattr(self, k, getattr(self, k)(v))
            except AttributeError:
                warnings.warn("Unknown attribute in API response: {}".format(k), Warning)


class OsuMode(Enum):
    osu = 0
    taiko = 1
    mania = 2
    ctb = 3


class Score(JsonObjWrapper):
    beatmap_id = str
    score = int
    maxcombo = int
    count50 = int
    count100 = int
    count300 = int
    countmiss = int
    countkatu = int
    countgeki = int
    perfect = bool
    enabled_mods = int
    user_id = int
    date = JsonDateTime
    rank = str
    pp = float


class User(JsonObjWrapper):
    user_id = int
    username = str
    count300 = int
    count100 = int
    count50 = int
    playcount = int
    ranked_score = int
    total_score = int
    pp_rank = int
    level = float
    pp_raw = float
    accuracy = float
    count_rank_ss = int
    count_rank_s = int
    count_rank_a = int
    country = str
    pp_country_rank = int
    events = JsonList(str)

    @property
    def total_hits(self):
        return self.count300 + self.count100 + self.count50


class BeatmapStatus(Enum):
    graveyard = -2
    wip = -1
    pending = 0
    ranked = 1
    approved = 2
    qualified = 3


class BeatmapGenre(Enum):
    any = 0
    unspecified = 1
    video_game = 2
    anime = 3
    rock = 4
    pop = 5
    other = 6
    novelty = 7
    hip_hop = 9
    electronic = 10


class BeatmapLanguage(Enum):
    any = 0
    other = 1
    english = 2
    japanese = 3
    chinese = 4
    instrumental = 5
    korean = 6
    french = 7
    german = 8
    swedish = 9
    spanish = 10
    italian = 11


class Beatmap(JsonObjWrapper):
    approved = PreProcessInt(BeatmapStatus)
    approved_date = Nullable(JsonDateTime)
    last_update = JsonDateTime
    artist = str
    beatmap_id = int
    beatmapset_id = int
    bpm = float
    creator = str
    difficultyrating = float
    diff_size = float
    diff_overall = float
    diff_approach = float
    diff_drain = float
    hit_length = int
    source = str
    genre_id = PreProcessInt(BeatmapGenre)
    language_id = PreProcessInt(BeatmapLanguage)
    title = str
    total_length = int
    version = str
    file_md5 = str
    mode = PreProcessInt(OsuMode)
    tags = str
    favourite_count = int
    playcount = int
    passcount = int
    max_combo = Nullable(int)

    def __str__(self):
        return "<{}.Beatmap title={} creator={}>".format(self.__module__, self.title, self.creator)
