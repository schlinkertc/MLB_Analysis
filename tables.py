from database import *

from sqlalchemy import PrimaryKeyConstraint,ForeignKeyConstraint
from sqlalchemy import Table,Column,Integer,String,DateTime,Date,Boolean,Float

db = MyDatabase('sqlite',dbname='mlb.db')

class Game(db.Base):
    __tablename__ = 'games'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id','pk',sqlite_on_conflict='REPLACE'
        ),
        {'extend_existing': True}
    )

    pk = Column(Integer)
    type = Column(String(1))
    doubleHeader = Column(String(1))
    id = Column(String(150))
    gamedayType = Column(String(1))
    tiebreaker = Column(String(1))
    gameNumber = Column(Integer)
    calendarEventID = Column(String(50))
    season = Column(Integer)

    dateTime = Column(DateTime)
    originalDate = Column(Date)

    detailedState = Column(String(12))

    homeTeam_id = Column(Integer)
    awayTeam_id = Column(Integer)

    condition = Column(String(25))
    temp = Column(Integer)
    wind = Column(String(50))

    venue_id = Column(Integer)

    home_probablePitcher = Column(Integer)
    away_probablePitcher = Column(Integer)

    def __repr__(self): 
        return "<Game(pk='%s',id='%s')>" % (
                        self.pk, self.id)

    def __init__(self,dictionary):
        for k,v in dictionary.items():
            setattr(self,k,v)

class Play(db.Base):
    __tablename__ = 'plays'
    __table_args__ = (
        PrimaryKeyConstraint(
            'about_atBatIndex','about_endTime','gamePk'
        ),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['games.pk']
        ),
        {'extend_existing': True}
        
    )

    result_type = Column(String)
    result_event = Column(String)
    result_eventType = Column(String)
    result_description = Column(String)
    result_rbi = Column(Integer)
    result_awayScore = Column(Integer)
    result_homeScore = Column(Integer)
    about_atBatIndex = Column(Integer)
    about_halfInning = Column(String)
    about_isTopInning = Column(Boolean)
    about_inning = Column(Integer)
    about_startTime = Column(String)
    about_endTime = Column(String)
    about_isComplete = Column(Boolean)
    about_isScoringPlay = Column(Boolean)
    about_hasReview = Column(Boolean)
    about_hasOut = Column(Boolean)
    about_captivatingIndex = Column(Integer)
    count_balls = Column(Integer)
    count_strikes = Column(Integer)
    count_outs = Column(Integer)
    gamePk = Column(Integer)

    def __repr__(self): 
        return "<Play(gamePk='%s',atBatIndex='%s', endTime = '%s')>" % (
                        self.gamePk, self.about_atBatIndex, self.about_endTime)

    def __init__(self,dictionary):
        for k,v in dictionary.items():
            setattr(self,k,v)
            
class Pitch(db.Base):
    __tablename__ = 'pitches'
    __table_args__ = (
        PrimaryKeyConstraint(
        'atBatIndex','playEndTime','index','gamePk'
        ),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['games.pk']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime'],
            refcolumns=['plays.about_atBatIndex','plays.about_endTime']
        ),
        {'extend_existing':True}
    )
    
    gamePk = Column(Integer)
    atBatIndex = Column(Integer)
    playEndTime = Column(String)
    index = Column(Integer)
    
    playId = Column(String)
    pitchNumber = Column(Integer)
    startTime = Column(String)
    endTime = Column(String)
    isPitch = Column(Boolean)
    type = Column(String)
    details_description = Column(String)
    details_code = Column(String)
    details_ballColor = Column(String)
    details_isInPlay = Column(String)
    details_isStrike = Column(Boolean)
    details_isBall = Column(Boolean)
    details_hasReview = Column(Boolean)
    count_balls = Column(Integer)
    count_strikes = Column(Integer)
    details_call_code = Column(String)
    details_call_description = Column(String)
    pfxId = Column(String)
    details_trailColor = Column(String)
    details_type_code = Column(String)
    details_type_description = Column(String)
    details_fromCatcher = Column(String)
    details_runnerGoing = Column(Boolean)
    
    def __init__(self,dictionary):
        for k,v in dictionary.items():
            setattr(self,k,v)
            
    def __repr__(self): 
        return "<Pitch(gamePk='%s',atBatIndex='%s', playEndTime = '%s', index = '%s')>" % (
                        self.gamePk, self.atBatIndex, self.playEndTime, self.index)
    
class PitchData(db.Base):
    __tablename__ = 'pitch_data'
    __table_args__ = (
        PrimaryKeyConstraint(
        'atBatIndex','playEndTime','index','gamePk'
        ),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['games.pk']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime'],
            refcolumns=['plays.about_atBatIndex','plays.about_endTime']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime','index'],
            refcolumns=['pitches.atBatIndex','pitches.playEndTime','pitches.index']
        ),
        {'extend_existing':True}
    )
    
    gamePk = Column(Integer)
    atBatIndex = Column(Integer)
    playEndTime = Column(String)
    index = Column(Integer)
    
    startSpeed = Column('pitchData_startSpeed',Float)
    endSpeed = Column('pitchData_endSpeed',Float)
    strikeZoneTop = Column('pitchData_strikeZoneTop',Float)
    zone = Column('pitchData_zone',Float)
    typeConfidence = Column('pitchData_typeConfidence',Float)
    plateTime = Column('pitchData_plateTime',Float)
    extension = Column('pitchData_extension',Float)
    coordinates_aY = Column('pitchData_coordinates_aY',Float)
    coordinates_aZ = Column('pitchData_coordinates_aZ',Float)
    coordinates_pfxX = Column('pitchData_coordinates_pfxX',Float)
    coordinates_pfxZ = Column('pitchData_coordinates_pfxZ',Float)
    coordinates_pX = Column('pitchData_coordinates_pX',Float)
    coordinates_pZ = Column('pitchData_coordinates_pZ',Float)
    coordinates_vX0 = Column('pitchData_coordinates_vX0',Float)
    coordinates_vY0 = Column('pitchData_coordinates_vY0',Float)
    coordinates_vZ0 = Column('pitchData_coordinates_vZ0',Float)
    coordinates_x = Column('pitchData_coordinates_x',Float)
    coordinates_y = Column('pitchData_coordinates_y',Float)
    coordinates_x0 = Column('pitchData_coordinates_x0',Float)
    coordinates_y0 = Column('pitchData_coordinates_y0',Float)
    coordinates_z0 = Column('pitchData_coordinates_z0',Float)
    coordinates_aX = Column('pitchData_coordinates_aX',Float)
    breaks_breakY = Column('pitchData_breaks_breakY',Float)
    breaks_spinRate = Column('pitchData_breaks_spinRate',Float)
    breaks_spinDirection = Column('pitchData_breaks_spinDirection',Float)
    
    def __init__(self,dictionary):
        for k,v in dictionary.items():
            setattr(self,k,v)
            
    def __repr__(self): 
        return "<PitchData(gamePk='%s',atBatIndex='%s', endTime = '%s', index = '%s')>" % (
                        self.gamePk, self.atBatIndex, self.playEndTime, self.index)
    
class HitData(db.Base):
    __tablename__ = 'hit_data'
    __table_args__ = (
        PrimaryKeyConstraint(
        'atBatIndex','playEndTime','index','gamePk'
        ),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['games.pk']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime'],
            refcolumns=['plays.about_atBatIndex','plays.about_endTime']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime','index'],
            refcolumns=['pitches.atBatIndex','pitches.playEndTime','pitches.index']
        ),
        {'extend_existing':True}
    )
    
    gamePk = Column(Integer)
    atBatIndex = Column(Integer)
    playEndTime = Column(String)
    index = Column(Integer)
    
    launchSpeed = Column('hitData_launchSpeed',Float)
    launchAngle = Column('hitData_launchAngle',Float)
    totalDistance = Column('hitData_totalDistance',Float)
    trajectory = Column('hitData_trajectory',String)
    location = Column('hitData_location',String)
    coordinates_coordX = Column('hitData_coordinates_coordX',Float)
    coordinates_coordY = Column('hitData_coordinates_coordY',Float)
    hardness = Column('hitData_hardness',String)
        
    def __init__(self,dictionary):
        for k,v in dictionary.items():
            setattr(self,k,v)
            
    def __repr__(self): 
        return "<HitData(gamePk='%s',atBatIndex='%s', endTime = '%s', index = '%s')>" % (
                        self.gamePk, self.atBatIndex, self.playEndTime, self.index)
    
class Action(db.Base):
    __tablename__ = 'actions'
    __table_args__ = (
        PrimaryKeyConstraint(
        'atBatIndex','playEndTime','index','gamePk'
        ),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['games.pk']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime'],
            refcolumns=['plays.about_atBatIndex','plays.about_endTime']
        ),
        ForeignKeyConstraint(
            columns=['player_id'],
            refcolumns=['players.id']
        ),
        ForeignKeyConstraint(
            columns=['reviewDetails_challengeTeamId'],
            refcolumns=['teams.id']
        ),
        {'extend_existing':True}
    )
    gamePk = Column(Integer)
    atBatIndex = Column(Integer)
    playEndTime = Column(String)
    index = Column(Integer)
    
    startTime = Column(String)
    endTime = Column(String)
    isPitch = Column(Boolean)
    type = Column(String)
    details_description = Column(String)
    details_event = Column(String)
    details_eventType = Column(String)
    details_awayScore = Column(Integer)
    details_homeScore = Column(Integer)
    details_isScoringPlay = Column(Boolean)
    details_hasReview = Column(Boolean)
    count_balls = Column(Integer)
    count_strikes = Column(Integer)
    count_outs = Column(Integer)
    player_id = Column(Integer)
    battingOrder = Column(Integer)
    position_code = Column(Integer)
    base = Column(Integer)
    injuryType = Column(String)
    actionPlayId = Column(String)
    reviewDetails_isOverturned = Column(Boolean)
    reviewDetails_reviewType = Column(String)
    reviewDetails_challengeTeamId = Column(Integer)
    
class Runner(db.Base):
    __tablename__ = 'runners'
    __table_args__ = (
        PrimaryKeyConstraint(
            'atBatIndex','playEndTime',
            'gamePk','details_playIndex','details_runner_id',
            'movement_start','movement_end','details_event'
        ),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['games.pk']
        ),
        ForeignKeyConstraint(
            columns=['details_responsiblePitcher_id'],
            refcolumns=['players.id']
        ),
        ForeignKeyConstraint(
            columns=['details_runner_id'],
            refcolumns=['players.id']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime','gamePk','details_playIndex'],
            refcolumns=['pitches.atBatIndex','pitches.playEndTime','pitches.gamePk','pitches.index']
        ),
        {'extend_existing':True}
    )
    atBatIndex = Column(Integer)
    playEndTime = Column(String)
        
    movement_start = Column(String)
    movement_end = Column(String)
    movement_outBase = Column(String)
    movement_isOut = Column(Boolean)
    movement_outNumber = Column(Integer)
    details_event = Column(String)
    details_eventType = Column(String)
    details_movementReason = Column(String)
    details_responsiblePitcher_id = Column(Integer)
    details_isScoringEvent = Column(Boolean)
    details_rbi = Column(Boolean)
    details_earned = Column(Boolean)
    details_teamUnearned = Column(Boolean)
    details_playIndex = Column(Integer)
    details_runner_id = Column(Integer)
    gamePk = Column(Integer)
        
class Credit(db.Base):
    __tablename__ = 'credits'
    __table_args__ = (
        PrimaryKeyConstraint(
            'atBatIndex','playEndTime',
            'gamePk','player_id',sqlite_on_conflict='IGNORE'
        ),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['games.pk']
        ),
        ForeignKeyConstraint(
            columns=['player_id'],
            refcolumns=['players.id']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime','gamePk'],
            refcolumns=['plays.about_atBatIndex','plays.about_endTime','plays.gamePk']
        ),
        {'extend_existing':True}
    )
    
    credit = Column(String)
    atBatIndex = Column(Integer)
    playEndTime = Column(String)
    player_id = Column(Integer)
    position_code = Column(String)
    gamePk = Column(Integer)
    
class Matchup(db.Base):
    __tablename__ = 'matchups'
    __table_args__ = (
        PrimaryKeyConstraint(
            'atBatIndex','playEndTime','gamePk'
        ),
        ForeignKeyConstraint(
            columns=['gamePk'],
            refcolumns=['games.pk']
        ),
        ForeignKeyConstraint(
            columns=['atBatIndex','playEndTime','gamePk'],
            refcolumns=['plays.about_atBatIndex','plays.about_endTime','plays.gamePk']
        ),
        ForeignKeyConstraint(columns=['batter_id'],refcolumns=['players.id']),
        ForeignKeyConstraint(columns=['pitcher_id'],refcolumns=['players.id']),
        ForeignKeyConstraint(columns=['postOnFirst_id'],refcolumns=['players.id']),
        ForeignKeyConstraint(columns=['postOnSecond_id'],refcolumns=['players.id']),
        ForeignKeyConstraint(columns=['postOnThird_id'],refcolumns=['players.id']),
        {'extend_existing':True}
    )
    atBatIndex = Column(Integer)
    playEndTime = Column(String)
    batter_id = Column(Integer)
    pitcher_id = Column(Integer)
    splits_batter = Column(String)
    splits_pitcher = Column(String)
    splits_menOnBase = Column(String)
    gamePk = Column(Integer)
    postOnFirst_id = Column(Integer)
    postOnSecond_id = Column(Integer)
    postOnThird_id = Column(Integer)
    
class Venue(db.Base):
    __tablename__ = 'venues'
    __table_args__ = (
        PrimaryKeyConstraint('id',sqlite_on_conflict='IGNORE'),
        {'extend_existing':True}
    )
    id = Column(Integer)
    name = Column(String)
    location_city = Column(String)
    location_state = Column(String)
    location_country = Column(String)
    location_defaultCoordinates_latitude = Column(Float)
    location_defaultCoordinates_longitude = Column(Float)
    timeZone_id = Column(String)
    timeZone_offset = Column(Integer)
    fieldInfo_capacity = Column(Integer)
    fieldInfo_turfType = Column(String)
    fieldInfo_roofType = Column(String)
    fieldInfo_leftLine = Column(Integer)
    fieldInfo_leftCenter = Column(Float)
    fieldInfo_center = Column(Integer)
    fieldInfo_rightCenter = Column(Float)
    fieldInfo_rightLine = Column(Integer)
    fieldInfo_left = Column(Float)
    fieldInfo_right = Column(Float)
    
class Team(db.Base):
    __tablename__ = 'teams'
    __table_args__ = (
        PrimaryKeyConstraint('id',sqlite_on_conflict='IGNORE'),
        ForeignKeyConstraint(columns=['venue_id'],refcolumns=['venues.id']),
        {'extend_existing':True}
    )
    
    id = Column(Integer)
    name = Column(String)
    abbreviation = Column(String)
    teamName = Column(String)
    locationName = Column(String)
    firstYearOfPlay = Column(String)
    shortName = Column(String)
    active = Column(Boolean)
    venue_id = Column(Integer)
    league_name = Column(String)
    division_name = Column(String)
    springLeague_name = Column(String)
    
class GameTeamLink(db.Base):
    __tablename__ = 'game_team_links'
    __table_args__ = (
        PrimaryKeyConstraint('gamePk','team_id'),
        ForeignKeyConstraint(columns=['gamePk'],refcolumns=['games.pk']),
        ForeignKeyConstraint(columns=['team_id'],refcolumns=['teams.id']),
        {'extend_existing':True}
    )
    gamePk = Column(Integer)
    team_id = Column(Integer)
    home_away = Column(String)
    
class TeamRecord(db.Base):
    __tablename__ = 'team_records'
    __table_args__ = (
        PrimaryKeyConstraint('gamePk','team_id'),
        ForeignKeyConstraint(columns=['gamePk'],refcolumns=['games.pk']),
        ForeignKeyConstraint(columns=['team_id'],refcolumns=['teams.id']),
        {'extend_existing':True}
    )
        
    gamesPlayed = Column(Integer)
    wildCardGamesBack = Column(String)
    leagueGamesBack = Column(String)
    divisionGamesBack = Column(String)
    divisionLeader = Column(Boolean)
    wins = Column(Integer)
    losses = Column(Integer)
    winningPercentage = Column(String)
    gamePk = Column(Integer)
    team_id = Column(Integer)
    leagueRecord_wins = Column(Integer)
    leagueRecord_losses = Column(Integer)
    leagueRecord_pct = Column(String)
    
class Player(db.Base):
    __tablename__ = 'players'
    __table_args__ = (
        PrimaryKeyConstraint('id',sqlite_on_conflict='IGNORE'),
        {'extend_existing':True}
    )
    
    id = Column(Integer)
    firstName = Column(String)
    lastName = Column(String)
    fullName = Column(String)
    primaryNumber = Column(String)
    birthDate = Column(String)
    currentAge = Column(String)
    birthCity = Column(String)
    birthStateProvince = Column(String)
    birthCountry = Column(String)
    height = Column(String)
    weight = Column(String)
    active = Column(Boolean)
    useName = Column(String)
    middleName = Column(String)
    boxscoreName = Column(String)
    nickName = Column(String)
    gender = Column(String)
    isPlayer = Column(Boolean)
    isVerified = Column(Boolean)
    draftYear = Column(Integer)
    mlbDebutDate = Column(String)
    nameSlug = Column(String)
    strikeZoneTop = Column(Float)
    strikeZoneBottom = Column(Float)
    primaryPosition_name = Column(String)
    primaryPosition_type = Column(String)
    batSide_description = Column(String)
    pitchHand_description = Column(String)
    pronunciation = Column(String)
    lastPlayedDate = Column(String)
    nameTitle = Column(String)
    deathDate = Column(String)
    deathCity = Column(String)
    deathStateProvince = Column(String)
    deathCountry = Column(String)
    
class GamePlayerLink(db.Base):
    __tablename__ = 'game_player_links'
    __table_args__ = (
        PrimaryKeyConstraint('person_id','gamePk','gameDateTime'),
        {'extend_existing':True}
    )
    person_id = Column(Integer)
    team_id = Column(Integer)
    gamePk = Column(Integer)
    gameDateTime = Column(String)
    position_code = Column(String)
    status_description = Column(String)
    gameStatus_isCurrentBatter = Column(Boolean)
    gameStatus_isCurrentPitcher = Column(Boolean)
    gameStatus_isOnBench = Column(Boolean)
    gameStatus_isSubstitute = Column(Boolean)
    battingOrder = Column(String)
    allPositions = Column(String)
    
class BattingStats(db.Base):
    __tablename__ = "batting_stats"
    __table_args__ = (
        PrimaryKeyConstraint('gamePk','person_id','gameDateTime'),
        {'extend_existing':True}
    )
    
    gamePk
    person_id
    gameDateTime
    
    gamesPlayed
    plateAppearances
    atBats
    hits
    baseOnBalls
    intentionalWalks
    strikeOuts
    hitByPitch
    sacFlies
    sacBunts
    doubles
    triples
    homeRuns
    totalBases
    runs
    groundOuts
    flyOuts
    stolenBases
    caughtStealing
    catchersInterference
    groundIntoDoublePlay
    groundIntoTriplePlay
    leftOnBase
    pickoffs
    
    
    
    
    
    
    

if __name__ != '__main__':
    db.Base.metadata.create_all()