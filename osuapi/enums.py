"""Enums and flags."""
from enum import Enum
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


    Notes
    -----

    .. code:: python

        # Check if a given flag is set.
        OsuMod.HardRock in flags

        # Check if a given flag is not set.
        OsuMod.HardRock not in flags

        # Check if all given flags are set.
        flags.contains_all(OsuMod.Hidden | OsuMod.HardRock)

        # Check if any of given flags are set.
        OsuMod.keyMod in flags

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
    Autopilot = 8192, "AP"  # Called Relax2 on osu api documentation
    Perfect = 16384, "PF"  # Only set along with SuddenDeth. i.e: PF only gives 16416
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
    def _flags_clean_nightcore(self):
        value = self.value
        if OsuMod.Nightcore in self:
            value &= ~OsuMod.DoubleTime.value
        if OsuMod.Perfect in self:
            value &= ~OsuMod.SuddenDeath.value
        yield from OsuMod(value).enabled_flags

    @property
    def shortname(self):
        """The initialism representing this mod. (e.g. HDHR)"""
        return "".join(tpl._shortname for tpl in self._flags_clean_nightcore)

    @property
    def longname(self):
        """The long name representing this mod. (e.g. Hidden DoubleTime)"""
        return " ".join(tpl.name for tpl in self._flags_clean_nightcore)

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
OsuMod.FreeModAllowed = OsuMod.NoFail | OsuMod.Easy | OsuMod.Hidden | OsuMod.HardRock | OsuMod.SuddenDeath | OsuMod.Flashlight | OsuMod.FadeIn | OsuMod.Relax | OsuMod.Autopilot | OsuMod.SpunOut | OsuMod.keyMod


class BeatmapStatus(Enum):
    """Enum representing the ranked status of a beatmap.

    See Also
    ---------
    <https://osu.ppy.sh/wiki/Beatmaps>
    """
    graveyard = -2
    wip = -1
    pending = 0
    ranked = 1
    approved = 2
    qualified = 3
    loved = 4


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
