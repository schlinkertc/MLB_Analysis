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
from sqlalchemy import Table,Column,Integer,String,DateTime,Date,Boolean

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
        
            