"""Different classes to parse dicts/lists returned from json into meaningful data objects."""

import datetime
from enum import Enum
from .dictmodel import AttributeModel, Attribute
from .flags import Flags


def JsonList(oftype):
    """Generate a converter that accepts a list of :oftype.

    field = JsonList(int) would expect to be passed a list of things to convert to int"""
    def _(lst):
        return [oftype(entry) for entry in lst]

    return _


def Nullable(oftype):
    """Generate a converter that may be None, or :oftype.

    field = Nullable(DateConverter) would expect either null or something to convert to date"""
    def _(it):
        if it is None:
            return None
        else:
            return oftype(it)

    return _


def PreProcessInt(oftype):
    """Generate a converter that first converts the input to int before passing to :oftype.

    field = PreProcessInt(MyEnum) if field is a string in the json response to be interpteded as int"""
    def _(it):
        return oftype(int(it))
    return _


def DateConverter(val):
    """Converter to convert osu! api's date type into datetime."""
    return datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S")


class OsuMode(Enum):
    osu = 0
    taiko = 1
    ctb = 2
    mania = 3


class OsuMod(Flags):
    NoMod = 0
    NoFail = 1
    Easy = 2
    NoVideo = 4
    Hidden = 8
    HardRock = 16
    SuddenDeath = 32
    DoubleTime = 64
    Relax = 128
    HalfTime = 256
    Nightcore = 512  # Only set along with DoubleTime. i.e: NC only gives 576
    Flashlight = 1024
    Autoplay = 2048
    SpunOut = 4096
    Relax2 = 8192  # Autopilot?
    Perfect = 16384
    Key4 = 32768
    Key5 = 65536
    Key6 = 131072
    Key7 = 262144
    Key8 = 524288
    keyMod = Key4 | Key5 | Key6 | Key7 | Key8
    FadeIn = 1048576
    Random = 2097152
    LastMod = 4194304
    FreeModAllowed = NoFail | Easy | Hidden | HardRock | SuddenDeath | Flashlight | FadeIn | Relax | Relax2 | SpunOut | keyMod
    Key9 = 16777216
    Key10 = 33554432
    Key1 = 67108864
    Key3 = 134217728
    Key2 = 268435456


class Score(AttributeModel):
    score = Attribute(int)
    maxcombo = Attribute(int)
    count50 = Attribute(int)
    count100 = Attribute(int)
    count300 = Attribute(int)
    countmiss = Attribute(int)
    countkatu = Attribute(int)
    countgeki = Attribute(int)
    perfect = Attribute(bool)
    user_id = Attribute(int)
    rank = Attribute(str)


class TeamScore(Score):
    slot = Attribute(int)
    team = Attribute(int)
    passed = Attribute(bool, name="pass")

    def __repr__(self):
        return "<{0.__module__}.TeamScore user_id={0.user_id} team={0.team}>".format(self)


class SoloScore(Score):
    beatmap_id = Attribute(str)
    pp = Attribute(float)
    enabled_mods = Attribute(PreProcessInt(OsuMod))
    date = Attribute(DateConverter)

    def __repr__(self):
        return "<{0.__module__}.SoloScore user_id={0.user_id} beatmap_id={0.beatmap_id} date={0.date}>".format(self)


class User(AttributeModel):
    user_id = Attribute(int)
    username = Attribute(str)
    count300 = Attribute(int)
    count100 = Attribute(int)
    count50 = Attribute(int)
    playcount = Attribute(int)
    ranked_score = Attribute(int)
    total_score = Attribute(int)
    pp_rank = Attribute(int)
    level = Attribute(float)
    pp_raw = Attribute(float)
    accuracy = Attribute(float)
    count_rank_ss = Attribute(int)
    count_rank_s = Attribute(int)
    count_rank_a = Attribute(int)
    country = Attribute(str)
    pp_country_rank = Attribute(int)
    events = Attribute(JsonList(str))

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


class Beatmap(AttributeModel):
    approved = Attribute(PreProcessInt(BeatmapStatus))
    approved_date = Attribute(Nullable(DateConverter))
    last_update = Attribute(DateConverter)
    artist = Attribute(str)
    beatmap_id = Attribute(int)
    beatmapset_id = Attribute(int)
    bpm = Attribute(float)
    creator = Attribute(str)
    difficultyrating = Attribute(float)
    diff_size = Attribute(float)
    diff_overall = Attribute(float)
    diff_approach = Attribute(float)
    diff_drain = Attribute(float)
    hit_length = Attribute(int)
    source = Attribute(str)
    genre_id = Attribute(PreProcessInt(BeatmapGenre))
    language_id = Attribute(PreProcessInt(BeatmapLanguage))
    title = Attribute(str)
    total_length = Attribute(int)
    version = Attribute(str)
    file_md5 = Attribute(str)
    mode = Attribute(PreProcessInt(OsuMode))
    tags = Attribute(str)
    favourite_count = Attribute(int)
    playcount = Attribute(int)
    passcount = Attribute(int)
    max_combo = Attribute(Nullable(int))

    def __repr__(self):
        return "<{0.__module__}.Beatmap title={0.title} creator={0.creator} id={0.beatmap_id}>".format(self)


class MatchMetadata(AttributeModel):
    match_id = Attribute(int)
    name = Attribute(str)
    start_time = Attribute(DateConverter)
    end_time = Attribute(Nullable(DateConverter))

    def __repr__(self):
        return "<{0.__module__}.MatchMetadata id={0.match_id} name={0.name} start_time={0.start_time}>".format(self)


class ScoringType(Enum):
    score = 0
    accuracy = 1
    combo = 2
    score_v2 = 3


class TeamType(Enum):
    head_to_head = 0
    tag_coop = 1
    team_vs = 2
    tag_team_vs = 3


class Game(AttributeModel):
    game_id = Attribute(int)
    start_time = Attribute(DateConverter)
    end_time = Attribute(DateConverter)
    beatmap_id = Attribute(int)
    play_mode = Attribute(PreProcessInt(OsuMode))
    match_type = Attribute(str)  # not sure what this is?
    scoring_type = Attribute(PreProcessInt(ScoringType))
    team_type = Attribute(PreProcessInt(TeamType))
    mods = Attribute(PreProcessInt(OsuMod))
    scores = Attribute(JsonList(TeamScore))

    def __repr__(self):
        return "<{0.__module__}.Game id={0.game_id} beatmap_id={0.beatmap_id} start_time={0.start_time}".format(self)


class Match(AttributeModel):
    match = Attribute(MatchMetadata)
    games = Attribute(JsonList(Game))
