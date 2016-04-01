"""Different classes to parse dicts/lists returned from json into meaningful data objects."""

import warnings
import datetime
from enum import Enum


def JsonList(oftype):
    """Generate a converter that accepts a list of :oftype.

    field = JsonList(int) would expect to be passed a list of things to convert to int"""
    class _:
        def __new__(cls, lis):
            return [oftype(entry) for entry in lis]
    return _


def Nullable(oftype):
    """Generate a converter that may be None, or :oftype.

    field = Nullable(DateConverter) would expect either null or something to convert to date"""
    class _:
        def __new__(cls, it):
            if it is None:
                return None
            else:
                return oftype(it)
    return _


def PreProcessInt(oftype):
    """Generate a converter that first converts the input to int before passing to :oftype.

    field = PreProcessInt(MyEnum) if field is a string in the json response to be interpteded as int"""
    class _:
        def __new__(cls, it):
            return oftype(int(it))
    return _


class DateConverter:
    """Converter to convert osu! api's date type into datetime."""

    def __new__(cls, val):
        return datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S")


class JsonObjWrapper:
    """Base class for data objects parsed from json objects."""

    def __init__(self, dic):
        for k, v in dic.items():
            try:
                setattr(self, k, getattr(self, k)(v))
            except AttributeError:
                warnings.warn("Unknown attribute {} in API response for type {}".format(k, type(self)), Warning)
            except:
                warnings.warn("Error processing {} value {}".format(k, v), Warning)
                raise


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
    date = DateConverter
    rank = str
    pp = float

    def __repr__(self):
        return "<{0.__module__}.Score user_id={0.user_id} beatmap_id={0.beatmap_id} date={0.date}>".format(self)

class TeamScore(Score):
    slot = int
    team = int
setattr(TeamScore, "pass", bool) # hack

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

    def __repr__(self):
        return "<{0.__module__}.User username={0.username} user_id={0.user_id}>".format(self)

    def __str__(self):
        return username


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
    approved_date = Nullable(DateConverter)
    last_update = DateConverter
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

    def __repr__(self):
        return "<{0.__module__}.Beatmap title={0.title} creator={0.creator} id={0.beatmap_id}>".format(self)

class MatchMetadata(JsonObjWrapper):
    match_id = int
    name = str
    start_time = DateConverter
    end_time = Nullable(DateConverter)

    def __repr__(self):
        return "<{0.__module__}.MatchMetadata id={0.match_id} name={0.name} start_time={0.start_time}>".format(self)

class Game(JsonObjWrapper):
    game_id = int
    start_time = DateConverter
    end_time = DateConverter
    beatmap_id = int
    play_mode = PreProcessInt(OsuMode)
    match_type = str # not sure what this is?
    scoring_type = int # TODO: Make enumerate
    team_type = int # TODO: Make enumerate
    mods = int # TODO: Make mods type
    scores = JsonList(TeamScore)

class Match(JsonObjWrapper):
    match = MatchMetadata
    games = JsonList(Game)


