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

from sqlalchemy import PrimaryKeyConstraint
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
            'about_atBatIndex','about_endTime',sqlite_on_conflict='IGNORE'
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
        PrimaryKeyConstraint('atBatIndex','playEndTime','index','gamePk'),
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
    pfxID = Column(String)
    details_trailColor = Column(String)
    details_type_code = Column(String)
    details_type_description = Column(String)
    details_fromCatcher = Column(String)
    details_runnerGoing = Column(Boolean)
    
    def __init__(self,dictionary):
        for k,v in dictionary.items():
            setattr(self,k,v)
            
    def __repr__(self): 
        return "<Pitch(gamePk='%s',atBatIndex='%s', endTime = '%s', index = '%s')>" % (
                        self.gamePk, self.about_atBatIndex, self.about_endTime, self.index)
    
class PitchData(Base):
    __tablename__ = 'pitch_data'
    __table_args__ = (
        PrimaryKeyConstraint('atBatIndex','playEndTime','index','gamePk'),
        {'extend_existing':True}
    )
    
    gamePk = Column(Integer)
    atBatIndex = Column(Integer)
    playEndTime = Column(String)
    index = Column(Integer)
    
    startSpeed = Column(Float)
    endSpeed = Column(Float)
    strikeZoneTop = Column(Float)
    zone = Column(Float)
    typeConfidence = Column(Float)
    plateTime = Column(Float)
    extension = Column(Float)
    coordinates_aY = Column(Float)
    coordinates_aZ = Column(Float)
    coordinates_pfxX = Column(Float)
    coordinates_pfxZ = Column(Float)
    coordinates_pX = Column(Float)
    coordinates_pZ = Column(Float)
    coordinates_vX0 = Column(Float)
    coordinates_vY0 = Column(Float)
    coordinates_vZ0 = Column(Float)
    coordinates_x = Column(Float)
    coordinates_y = Column(Float)
    coordinates_x0 = Column(Float)
    coordinates_y0 = Column(Float)
    coordinates_z0 = Column(Float)
    coordinates_aX = Column(Float)
    breaks_breakY = Column(Float)
    breaks_spinRate = Column(Float)
    breaks_spinDirection = Column(Float)
    
    def __init__(self,dictionary):
        for k,v in dictionary.items():
            setattr(self,k,v)
            
    def __repr__(self): 
        return "<PitchData(gamePk='%s',atBatIndex='%s', endTime = '%s', index = '%s')>" % (
                        self.gamePk, self.about_atBatIndex, self.about_endTime, self.index)
    
class HitData(Base):
    __tablename__ = 'hit_data'
    __table_args__ = (
        PrimaryKeyConstraint('atBatIndex','playEndTime','index','gamePk'),
        {'extend_existing':True}
    )
    
    gamePk = Column(Integer)
    atBatIndex = Column(Integer)
    playEndTime = Column(String)
    index = Column(Integer)
    
    launchSpeed = Column(Float)
    launchAngle = Column(Float)
    totalDistance = Column(Float)
    trajectory = Column(String)
    location = Column(String)
    coordinates_coordX = Column(Float)
    coordinates_coordY = Column(Float)
    hardness = Column(String)
        
    def __init__(self,dictionary):
        for k,v in dictionary.items():
            setattr(self,k,v)
            
    def __repr__(self): 
        return "<HitData(gamePk='%s',atBatIndex='%s', endTime = '%s', index = '%s')>" % (
                        self.gamePk, self.about_atBatIndex, self.about_endTime, self.index)