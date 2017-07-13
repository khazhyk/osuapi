"""Different classes to parse dicts/lists returned from json into meaningful data objects."""

from .enums import *
from .dictmodel import AttributeModel, Attribute, JsonList, Nullable, PreProcessInt, DateConverter


class Score(AttributeModel):
    """Abstract class representing a score.

    Attributes
    -----------
    score : int
        The score value
    maxcombo : int
        Largest combo achieved
    count50 : int
        Number of "50" hits
    count100 : int
        Number of "100" hits
    count300 : int
        Number of "300" hits
    countmiss : int
        Number of misses
    countkatu : int
        Number of "katu" sections (only 100s and 300s)
    countgeki : int
        Number of "geki" sections (only 300s)
    perfect : bool
        If the play is a full combo (maxcombo is maximal)
    user_id : int
        ID of user who played.
    rank :  str
        Letter rank achieved

    See Also
    ---------
    <https://osu.ppy.sh/wiki/Score>
    """
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
    """Class representing a score in a multiplayer team game.

    See :class:`Score`

    Attributes
    -----------
    slot : int
        Which multiplayer slot the player was in.
    team : int
        Which multiplayer team the player was in.
    passed : bool
        If the score is passing.

    See Also
    ---------
    <https://osu.ppy.sh/wiki/Score>
    """
    slot = Attribute(int)
    team = Attribute(int)
    passed = Attribute(bool, name="pass")

    def __repr__(self):
        return "<{0.__module__}.TeamScore user_id={0.user_id} team={0.team}>".format(self)


class RecentScore(Score):
    """Class representing a recent score.

    See :class:`Score`

    Attributes
    -----------
    beatmap_id : int
        Beatmap the score is for.
    enabled_mods : :class:`osuapi.enums.OsuMod`
        Enabled modifiers
    date : datetime
        When the score was played.

    See Also
    ---------
    <https://osu.ppy.sh/wiki/Score>
    """
    beatmap_id = Attribute(str)
    enabled_mods = Attribute(PreProcessInt(OsuMod))
    date = Attribute(DateConverter)

    def __repr__(self):
        return "<{0.__module__}.SoloScore user_id={0.user_id} beatmap_id={0.beatmap_id} date={0.date}>".format(self)


class SoloScore(Score):
    """Class representing a score in singleplayer.

    See :class:`Score`

    Attributes
    -----------
    beatmap_id : int
        Beatmap the score is for.
    pp : float
        How much PP the score is worth
    enabled_mods : :class:`osuapi.enums.OsuMod`
        Enabled modifiers
    date : datetime
        When the score was played.

    See Also
    ---------
    <https://osu.ppy.sh/wiki/Score>
    """
    beatmap_id = Attribute(str)
    pp = Attribute(float)
    enabled_mods = Attribute(PreProcessInt(OsuMod))
    date = Attribute(DateConverter)

    def __repr__(self):
        return "<{0.__module__}.SoloScore user_id={0.user_id} beatmap_id={0.beatmap_id} date={0.date}>".format(self)


class BeatmapScore(Score):
    """Class representing a score attached to a beatmap.

    See :class:`Score`

    Attributes
    -----------
    username : str
        Name of user.
    pp : float
        How much PP the score is worth
    enabled_mods : :class:`osuapi.enums.OsuMod`
        Enabled modifiers
    date : datetime
        When the score was played.
    score_id : int
        ID of score.

    See Also
    ---------
    <https://osu.ppy.sh/wiki/Score>
    """
    username = Attribute(str)
    pp = Attribute(float)
    enabled_mods = Attribute(PreProcessInt(OsuMod))
    date = Attribute(DateConverter)
    score_id = Attribute(int)

    def __repr__(self):
        return "<{0.__module__}.BeatmapScore user_id={0.user_id} score_id={0.score_id} date={0.date}>".format(self)


class User(AttributeModel):
    """Class representing a user.

    Attributes
    -----------
    user_id : int
        User's unique identifier.
    username : str
        User's name.
    count300 : int
        Career total of "300" hits.
    count100 : int
        Career total of "100" hits.
    count50 : int
        Career total of "50" hits.
    playcount : int
        Career total play count.
    ranked_score : int
        Total sum of the best scores from all the ranked beatmaps played online.
    total_score : int
        Total sum of all scores on ranked beatmaps, including failed trails.
    pp_rank : int
        Global ranking place.
    level: float
        User's level
    pp_raw: float
        User's performance points
    accuracy : float
        Weighted average of accuracy on top plays.
    count_rank_ss : int
        Career total of SS ranks.
    count_rank_s : int
        Career total of S ranks.
    count_rank_a : int
        Career total of A ranks.
    country : str
        Country the user is registered to.
    pp_country_rank : int
        Country ranking place.
    events : list[str]
        HTML snippets of recent "interesting" events.

    See Also
    ---------
    <https://osu.ppy.sh/wiki/Score>

    """
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
        return self.username


class Beatmap(AttributeModel):
    """Class representing a beatmap

    Attributes
    -----------
    approved : bool
        Whether or not the map has been ranked.
    approved_date : Optional[datetime]
        When the beatmap was ranked, or None.
    last_update : datetime
        Last time the map was updated.
    artist : str
        Music metadata.
    beatmap_id : int
        Unique identifier for beatmap.
    beatmapset_id : int
        Unique identifier for set this beatmap belongs to.
    bpm : float
        Speed of map in beats per minute.
    creator : str
        Username of map creator.
    difficultyrating : float
        Star rating of a map.
    diff_size : float
        Circle Size. (CS)
    diff_overall : float
        Overall Difficulty. (OD)
    diff_approach : float
        Approach rate. (AR)
    diff_drain : float
        Health Drain (HP)
    hit_length : int
        Playable time in seconds. (Drain time)
    source : str
        Source of the music
    genre_id : :class:`osuapi.enums.BeatmapGenre`
        Genre of the music.
    language_id : :class:`osuapi.enums.BeatmapLanguage`
        Language of the music.
    title : str
        Title of the song.
    total_length : int
        Total song length in seconds.
    version : str
        Difficulty name.
    file_md5 : str
        md5 hash of map.
    mode : :class:`osuapi.enums.OsuMode`
        Game mode for the map.
    tags : str
        Space delimited tags for the map.
    favourite_count : int
        Number of users that have favorited this map.
    playcount : int
        Number of times this map has been played (including fails)/
    passcount : int
        Number of times this map has been passed.
    max_combo : Optional[int]
        Maximum possible combo.

    See Also
    ---------
    <https://osu.ppy.sh/wiki/Beatmaps>
    """
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
    """Class representing info about a match.

    Attributes
    -----------
    match_id : int
        Unique identifier for this match.
    name : str
        Name of the match when it was first created.
    start_time : datetime
        When the match was created.
    end_time : Optional[datetime]
        When the match was ended, or None.
    """
    match_id = Attribute(int)
    name = Attribute(str)
    start_time = Attribute(DateConverter)
    end_time = Attribute(Nullable(DateConverter))

    def __repr__(self):
        return "<{0.__module__}.MatchMetadata id={0.match_id} name={0.name} start_time={0.start_time}>".format(self)


class Game(AttributeModel):
    """Class representing an individual multiplayer game.

    Attributes
    -----------
    game_id : int
        Unique identifier for this game.
    start_time : datetime
        When the game started.
    end_time : datetime
        When the game ended.
    beatmap_id : int
        Beatmap played.
    play_mode : :class:`osuapi.enums.OsuMode`
        Game mode.
    match_type
        Not really sure...
    scoring_type : :class:`osuapi.enums.ScoringType`
        Scoring type of game.
    team_type : :class:`osuapi.enums.TeamType`
        Team type of the game.
    mods : :class:`osuapi.enums.OsuMod`
        Modifiers enabled for all players.
    scores : list[:class:`TeamScore`]
        List of scores for all players.
    """
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
