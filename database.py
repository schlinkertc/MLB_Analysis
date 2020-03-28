import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    """
    Custom class for instantiating a SQL Alchemy connection. Configured here for SQLite, but intended to be flexible.
    Credit to Medium user Mahmud Ahsan:
    https://medium.com/@mahmudahsan/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32
    """
    DB_ENGINE = {
       'sqlite': 'sqlite:////{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None
    def __init__(self, dbtype, 
                 username='', password='', 
                 dbname='',path=os.getcwd()+'/'):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=path+dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
            
            self.Base = declarative_base(bind=self.db_engine)
            self.Base.metadata.create_all(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")
    
    def insert_game(self,gamePk,method='IGNORE'):
        gamePk = int(gamePk)
        
        if method == 'IGNORE':
            q = self.db_engine.execute('select pk from games').fetchall()
            existing_pks = [x[0] for x in q]

            if gamePk in existing_pks:
                return {'game':gamePk,
                        'insert_status':'fail',
                        'reason':'already exists'}
            else:
                try:
                    call = API_call(gamePk)
                except:
                    return {'game':gamePk,
                            'insert_status':'fail',
                            'reason':'API call failed'}

                mappers = [
                    Game,Play,
                    Pitch,
                    Action,Runner,Credit,
                    Matchup,Venue,
                    Team,GameTeamLink,TeamRecord,
                    Player,PitchData,HitData
                ]

                for mapper in mappers:
                    insert_values = []

                    table = mapper.__table__
                    cols = [x.name for x in table.c]

                    if mapper == HitData or mapper == PitchData:
                        records = call.__dict__['pitches']
                    else:
                        records = call.__dict__[table.name]
                    for record in records:
                        insert_value = {}
                        for k in cols:
                            try:
                                insert_value[k]=record[k]
                            except KeyError:
                                insert_value[k]=None
                        insert_values.append(insert_value)

                    conn = self.db_engine.connect()    
                    try:
                        conn.execute(table.insert(),insert_values)
                        return {'game':gamePk,
                                'insert_status':'success',
                                'reason':'None'}
                    except IntegrityError:
                        return {'game':gamePk,
                                'insert_status':'fail',
                                'reason':'Integrity Error'}
        if method == 'REPLACE':
            return 'replace method needs to be done!'
            

from sqlalchemy import PrimaryKeyConstraint,ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Table,Column,Integer,String,DateTime,Date,Boolean,Float

class Game(Base):
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

class Play(Base):
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
            
class Pitch(Base):
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
    
class PitchData(Base):
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
    
class HitData(Base):
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
    
class Action(Base):
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
    
class Runner(Base):
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
        
class Credit(Base):
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
    
class Matchup(Base):
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
    
class Venue(Base):
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
    
class Team(Base):
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
    
class GameTeamLink(Base):
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
    
class TeamRecord(Base):
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
    
class Player(Base):
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
    
class GamePlayerLink(Base):
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
    
    
    
###################

## RELATIONSHIPS ##

###################

from sqlalchemy.orm import relationship

# one-to-many between game and plays
Game.plays = relationship(
    "Play",order_by=Play.about_endTime,back_populates='game')
Play.game = relationship("Game",back_populates="plays")

# one-to-many relationship between play and pitches
Play.pitches = relationship('Pitch',order_by=Pitch.index,back_populates='play')
Pitch.play = relationship('Play',back_populates='pitches')

Play.hitData = relationship(
    'HitData',order_by=HitData.index,back_populates='play'
)
HitData.play = relationship('Play',back_populates='hitData')

Play.pitchData = relationship(
    'PitchData', order_by=PitchData.index, back_populates='play')
PitchData.play = relationship('Play',back_populates='pitchData')

Pitch.hitData = relationship(
    'HitData',back_populates='pitch',uselist=False)
HitData.pitch = relationship(
    'Pitch',back_populates='hitData',viewonly=True)

Pitch.pitchData = relationship(
    'PitchData',back_populates='pitch',uselist=False)
PitchData.pitch = relationship(
    'Pitch',back_populates='pitchData',viewonly=True)


