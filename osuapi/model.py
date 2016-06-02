"""Different classes to parse dicts/lists returned from json into meaningful data objects."""

from enum import Enum
from .dictmodel import AttributeModel, Attribute, JsonList, Nullable, PreProcessInt, DateConverter
from .flags import Flags


class OsuMode(Enum):
    """Enum representing osu! game mode."""

    osu = 0, "osu!standard"
    taiko = 1, "osu!taiko"
    ctb = 2, "osu!catchthebeat"
    mania = 3, "osu!mania"

    def __new__(cls, value, display):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display
        return obj

    def __str__(self):
        return self.display_name


class OsuMod(Flags):
    """Bitwise Flags representing osu! mods.


    Usage
    -----

    FIXME - IDK how to inline code
    ```py
    # Check if a given flag is set.
    OsuMod.HardRock in flags

    # Check if a given flag is not set.
    OsuMod.HardRock not in flags

    # Check if all given flags are set.
    flags.all_set(OsuMod.Hidden | OsuMod.HardRock)

    # Check if any of given flags are set.
    OsuMod.keyMod in flags
    ```

    """
    NoMod = 0
    NoFail = 1, "NF"
    Easy = 2, "EZ"
    NoVideo = 4
    Hidden = 8, "HD"
    HardRock = 16, "HR"
    SuddenDeath = 32, "SD"
    DoubleTime = 64, "DT"
    Relax = 128, "RX"
    HalfTime = 256, "HT"
    Nightcore = 512, "NC"  # Only set along with DoubleTime. i.e: NC only gives 576
    Flashlight = 1024, "FL"
    Autoplay = 2048
    SpunOut = 4096, "SO"
    Relax2 = 8192, "AP"  # Autopilot?
    Perfect = 16384, "PF"
    Key4 = 32768, "4K"
    Key5 = 65536, "5K"
    Key6 = 131072, "6K"
    Key7 = 262144, "7K"
    Key8 = 524288, "8K"
    FadeIn = 1048576, "FI"
    Random = 2097152, "RD"
    LastMod = 4194304
    Key9 = 16777216, "9K"
    Key10 = 33554432, "10K"
    Key1 = 67108864, "1K"
    Key3 = 134217728, "3K"
    Key2 = 268435456, "2K"

    def __init__(self, value, shortname=""):
        Flags.__init__(self, value)
        self._shortname = shortname

    def __str__(self):
        return self.longname

    @property
    def shortname(self):
        return "".join(tpl[0]._shortname for tpl in self.enabled_flags)

    @property
    def longname(self):
        return " ".join(tpl[1] for tpl in self.enabled_flags)

    def __format__(self, format_spec):
        """Format an OsuMod.

        Formats
        -------
        s
            shortname e.g. HDHR
        l
            longname e.g. Hidden HardRock"""
        if format_spec == "s":
            return self.shortname
        elif format_spec == "l":
            return self.longname
        else:
            return self.__str__()

OsuMod.keyMod = OsuMod.Key4 | OsuMod.Key5 | OsuMod.Key6 | OsuMod.Key7 | OsuMod.Key8
OsuMod.FreeModAllowed = OsuMod.NoFail | OsuMod.Easy | OsuMod.Hidden | OsuMod.HardRock | OsuMod.SuddenDeath | OsuMod.Flashlight | OsuMod.FadeIn | OsuMod.Relax | OsuMod.Relax2 | OsuMod.SpunOut | OsuMod.keyMod


class Score(AttributeModel):
    """Abstract class representing a score."""
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
    """Class representing a score in a multiplayer team game."""
    slot = Attribute(int)
    team = Attribute(int)
    passed = Attribute(bool, name="pass")

    def __repr__(self):
        return "<{0.__module__}.TeamScore user_id={0.user_id} team={0.team}>".format(self)


class SoloScore(Score):
    """Class represeting a score in singleplayer."""
    beatmap_id = Attribute(str)
    pp = Attribute(float)
    enabled_mods = Attribute(PreProcessInt(OsuMod))
    date = Attribute(DateConverter)

    def __repr__(self):
        return "<{0.__module__}.SoloScore user_id={0.user_id} beatmap_id={0.beatmap_id} date={0.date}>".format(self)


class User(AttributeModel):
    """Class representing a user."""
    user_id = Attribute(int)
    username = Attribute(str)
    count300 = Attribute(Nullable(int))
    count100 = Attribute(Nullable(int))
    count50 = Attribute(Nullable(int))
    playcount = Attribute(Nullable(int))
    ranked_score = Attribute(Nullable(int))
    total_score = Attribute(Nullable(int))
    pp_rank = Attribute(Nullable(int))
    level = Attribute(Nullable(float))
    pp_raw = Attribute(Nullable(float))
    accuracy = Attribute(Nullable(float))
    count_rank_ss = Attribute(Nullable(int))
    count_rank_s = Attribute(Nullable(int))
    count_rank_a = Attribute(Nullable(int))
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
    """Enum representing the ranked status of a beatmap."""
    graveyard = -2
    wip = -1
    pending = 0
    ranked = 1
    approved = 2
    qualified = 3


class BeatmapGenre(Enum):
    """Enum represeting the genre of a beatmap."""
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
    """Enum represeting the language of a beatmap."""
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
    """Class represeting a beatmap."""
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
    """Class representing info about a match."""
    match_id = Attribute(int)
    name = Attribute(str)
    start_time = Attribute(DateConverter)
    end_time = Attribute(Nullable(DateConverter))

    def __repr__(self):
        return "<{0.__module__}.MatchMetadata id={0.match_id} name={0.name} start_time={0.start_time}>".format(self)


class ScoringType(Enum):
    """Enum representing the scoring type of a multiplayer game."""
    score = 0
    accuracy = 1
    combo = 2
    score_v2 = 3


class TeamType(Enum):
    """Enum representing the team type of a multiplayer game."""
    head_to_head = 0
    tag_coop = 1
    team_vs = 2
    tag_team_vs = 3


class Game(AttributeModel):
    """Class representing an individual multiplayer game."""
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
    """Class representing a match's info and collection of games."""
    match = Attribute(MatchMetadata)
    games = Attribute(JsonList(Game))
