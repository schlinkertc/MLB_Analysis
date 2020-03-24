import os
import sqlalchemy
from sqlalchemy import create_engine

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
        else:
            print("DBType is not found in DB_ENGINE")

from sqlalchemy import PrimaryKeyConstraint,ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Table,Column,Integer,String,DateTime,Date,Boolean,Float

class Game(Base):
    __tablename__ = 'games'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id','detailedState',sqlite_on_conflict='IGNORE'
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
    calenderEventId = Column(String(50))
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
    pfxId = Column('pfxId',String)
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
    
    pitchData_startSpeed = Column(Float)
    pitchData_endSpeed = Column(Float)
    pitchData_strikeZoneTop = Column(Float)
    pitchData_zone = Column(Float)
    pitchData_typeConfidence = Column(Float)
    pitchData_plateTime = Column(Float)
    pitchData_extension = Column(Float)
    pitchData_coordinates_aY = Column(Float)
    pitchData_coordinates_aZ = Column(Float)
    pitchData_coordinates_pfxX = Column(Float)
    pitchData_coordinates_pfxZ = Column(Float)
    pitchData_coordinates_pX = Column(Float)
    pitchData_coordinates_pZ = Column(Float)
    pitchData_coordinates_vX0 = Column(Float)
    pitchData_coordinates_vY0 = Column(Float)
    pitchData_coordinates_vZ0 = Column(Float)
    pitchData_coordinates_x = Column(Float)
    pitchData_coordinates_y = Column(Float)
    pitchData_coordinates_x0 = Column(Float)
    pitchData_coordinates_y0 = Column(Float)
    pitchData_coordinates_z0 = Column(Float)
    pitchData_coordinates_aX = Column(Float)
    pitchData_breaks_breakY = Column(Float)
    pitchData_breaks_spinRate = Column(Float)
    pitchData_breaks_spinDirection = Column(Float)
    
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
        'atBatIndex','playEndTime','index'
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
    
    hitData_launchSpeed = Column(Float)
    hitData_launchAngle = Column(Float)
    hitData_totalDistance = Column(Float)
    hitData_trajectory = Column(String)
    hitData_location = Column(String)
    hitData_coordinates_coordX = Column(Float)
    hitData_coordinates_coordY = Column(Float)
    hitData_hardness = Column(String)
        
    def __init__(self,dictionary):
        for k,v in dictionary.items():
            setattr(self,k,v)
            
    def __repr__(self): 
        return "<HitData(gamePk='%s',atBatIndex='%s', endTime = '%s', index = '%s')>" % (
                        self.gamePk, self.atBatIndex, self.playEndTime, self.index)
    
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


