############################################################################################
# This file defines python classes using the SQL Alchemy declaritive base 
# These classes will be used to add records to the database 
# The SQL Alchemy ORM allows us to access relationships between records via class methods 
############################################################################################

import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey,DateTime,Boolean,Date,Time,Float,DATE,DATETIME,TIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import statsapi as mlb
from datetime import datetime
import time

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
    def __init__(self, dbtype, username='', password='', dbname='',path=os.getcwd()+'/'):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=path+dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

db = MyDatabase('sqlite',dbname='mlb.db')

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db.db_engine)
session = Session()
Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    __table_args__ = {'extend_existing': True}
    
    def __init__(self,personId,session,commit=False):
        try:
            current_players=[item for sublist in 
                             session.execute("""select id from people""").fetchall() for item in sublist]
        except:
            current_players=[]
          
            session.rollback()
        if personId not in current_players:
            api_call = mlb.get('person',{'personId':personId})

            person = api_call['people'][0]
            person['birthDate'] = person.get('birthDate','1900-01-01')


            self.id=person.get('id','null')
            self.fullName=person.get('fullName','null')
            self.firstName=person.get('firstName','null')
            self.lastName=person.get('lastName','null')
            self.primaryNumber=person.get('primaryNumber','null')
            
            self.birthDate=datetime.date(datetime.strptime(person.get('birthDate','1900-01-01'),'%Y-%m-%d'))
            
            self.currentAge=person.get('currentAge','null')
            self.birthCity=person.get('birthCity','null')
            self.birthCountry=person.get('birthCountry','null')
            self.height=person.get('height','null')
            self.weight=person.get('weight','null')
            self.active=person.get('active','null')
            self.primaryPosition_code=person.get('primaryPosition',{'code':'null'})['code']
            self.primaryPosition_name=person.get('primaryPosition',{'name':'null'})['name']
            self.primaryPosition_type=person.get('primaryPosition',{'type':'null'})['type']
            self.primaryPosition_abbreviation=person.get('primaryPosition',{'abbreviation':'null'})['abbreviation']
            self.gender=person.get('gender','null')
            self.isPlayer=person.get('isPlayer','null')
            self.isVerified=person.get('isVerified','null')
            self.draftYear=person.get('draftYear','null')
            
            self.mlbDebutDate=datetime.date(datetime.strptime(person.get('mlbDebutDate','1900-01-01'),'%Y-%m-%d'))
            
            self.batSide=person.get('batSide',{'description':'null'})['description']
            self.pitchHand=person.get('pitchHand',{'description':'null'})['description']
            self.nameSlug=person.get('nameSlug','null')
            self.fullFMLName=person.get('fullFMLName','null')
            self.strikeZoneTop=person.get('strikeZoneTop','null')
            self.strikeZoneBottom=person.get('strikeZoneBottom','null')
            
            if commit==True:
                session.add(self)
                session.commit()
        else:
            pass
    
    id = Column(Integer, primary_key=True)
    fullName = Column(String(25))
    firstName = Column(String(25))
    lastName = Column(String(25))
    primaryNumber = Column(Integer)
    birthDate = Column(Date)
    currentAge = Column(Integer)
    birthCity = Column(String(25))
    birthCountry = Column(String(25))
    height = Column(String(25))
    weight = Column(Integer)
    active = Column(Boolean)
    primaryPosition_code = Column(String(10))
    primaryPosition_name = Column(String(25))
    primaryPosition_type = Column(String(25))
    primaryPosition_abbreviation = Column(String(25))
    gender = Column(String(5))
    isPlayer = Column(Boolean)
    isVerified = Column(Boolean)
    draftYear = Column(Integer)
    mlbDebutDate = Column(Date)
    batSide = Column(String(10))
    pitchHand = Column(String(10))
    nameSlug = Column(String(30))
    fullFMLName = Column(String(50))
    strikeZoneTop = Column(Float)
    strikeZoneBottom = Column(Float)
    
    def __repr__(self):
        return "<Person(nameSlug='%s')>" % self.nameSlug
    
class Pitch(Base):
    __tablename__= 'pitches'
    __table_args__ = {'extend_existing': True}
    
    def __init__(self,pitch_dict,play_id,session):
        
        
        details = pitch_dict['details']
        count = pitch_dict['count']
        pitchData = pitch_dict.get('pitchData',{'null':'null'})
        coordinates = pitchData['coordinates']
        breaks=pitchData['breaks']

        self.id=play_id+'--pitchNumber: '+str(pitch_dict['pitchNumber'])
        self.call_code=details['code']
        self.call_description=details['description']
        self.ballColor=details.get('ballColor','null')
        self.trailColor=details.get('trailColor','null')
        self.isInPlay=details['isInPlay']
        self.isStrike=details['isStrike']
        self.isBall=details['isBall']
        self.type_code=details.get('type',{'code':'null'})['code']
        self.type_description=details.get('type',{'description':'null'})['description']

        self.count_balls=count['balls']
        self.count_strikes=count['strikes']

        self.startSpeed=pitchData.get('startSpeed',0.0)
        self.endSpeed=pitchData.get('endSpeed',0.0)
        self.strikeZoneTop=pitchData.get('strikeZoneTop',0.0)
        self.strikeZoneBottom=pitchData.get('strikeZoneBottom',0.0)

        self.aY = coordinates.get('aY',99.9)
        self.aZ = coordinates.get('aZ',99.9)
        self.pfxX = coordinates.get('pfxX',99.9)
        self.pfxZ = coordinates.get('pfxZ',99.9)
        self.pX = coordinates.get('pX',99.9)
        self.pZ = coordinates.get('pZ',99.9)
        self.vX0 = coordinates.get('vX0',99.9)
        self.vY0 = coordinates.get('vY0',99.9)
        self.vZ0 = coordinates.get('vZ0',99.9)
        self.x = coordinates.get('x',99.9)
        self.y = coordinates.get('y',99.9)
        self.x0 = coordinates.get('x0',99.9)
        self.y0 = coordinates.get('y0',99.9)
        self.z0 = coordinates.get('zy',99.9)
        self.aX = coordinates.get('aX',99.9)

        self.breakAngle = breaks.get('breakAngle',99.9)
        self.breakLength = breaks.get('breakLength',99.9)
        self.breakY = breaks.get('breakY',99.9)
        self.spinRate = breaks.get('spinRate',99.9)
        self.spinDirection = breaks.get('spinDirection',99.9)

        self.zone = pitchData.get('zone',0)
        self.typeConfidence = pitchData.get('typeConfidence',99.9)
        self.plateTime = pitchData.get('plateTime',99.9)
        self.extension = pitchData.get('extension',99.9)
        self.index=pitch_dict['index']

        self.pfxId = pitch_dict.get('pfxId','null')
        self.pitchId = pitch_dict.get('playId','null')
        self.pitchNumber = pitch_dict['pitchNumber']
        self.startTime = datetime.strptime(pitch_dict['startTime'],'%Y-%m-%dT%H:%M:%S.%fZ')
        self.endTime = datetime.strptime(pitch_dict['endTime'],'%Y-%m-%dT%H:%M:%S.%fZ')
        self.play_id = play_id
        
    id = Column(String(200),primary_key=True)
    call_code = Column(String(3))
    call_description = Column(String(25))
    ballColor = Column(String(50))
    trailColor = Column(String(50))
    isInPlay = Column(Boolean)
    isStrike = Column(Boolean)
    isBall = Column(Boolean)
    type_code = Column(String(10))
    type_description = Column(String(30))
    hasReview = Column(Boolean)
    count_balls = Column(Integer)
    count_strikes = Column(Integer)
    startSpeed = Column(Float)
    endSpeed = Column(Float)
    strikeZoneTop=Column(Float)
    strikeZoneBottom=Column(Float)
    aY = Column(Float)
    aZ = Column(Float)
    pfxX = Column(Float)
    pfxZ = Column(Float)
    pX = Column(Float)
    pZ = Column(Float)
    vX0 = Column(Float)
    vY0 = Column(Float)
    vZ0 = Column(Float)
    x = Column(Float)
    y = Column(Float)
    x0 = Column(Float)
    y0 = Column(Float)
    z0 = Column(Float)
    aX = Column(Float)
    breakAngle = Column(Float)
    breakLength = Column(Float)
    breakY = Column(Float)
    spinRate = Column(Float)
    spinDirection = Column(Float)
    zone = Column(Integer)
    typeConfidence = Column(Float)
    plateTime = Column(Float)
    extension = Column(Float)
    index = Column(Integer)
    pfxId = Column(String(200))
    pitchId = Column(String(200))
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    
    play_id = Column(String(200),ForeignKey("plays.id"))
    play = relationship('Play',back_populates='pitches')
    
    def __repr__(self):
        return "<Pitch(id=%s)>" % self.id

# Declare the mapping for the Plays table 
class Play(Base):
    __tablename__= 'plays'
    __table_args__ = {'extend_existing': True} 
    
    def __init__(self,play,game_id,session,commit=False):
            result = play['result']
            about = play['about']
            batter = play.get('matchup',{'batter':'null'})['batter']
            pitcher = play.get('matchup',{'pitcher':'null'})['pitcher']
            count = play['count']
            Person(batter['id'],session,commit=commit)
            Person(pitcher['id'],session,commit=commit)
            
            play_id = game_id+'AB_'+str(about['atBatIndex'])

            self.id=play_id
            self.type=result['type']
            self.event=result.get('event','null')
            self.eventType=result.get('eventType','null')
            self.description=result.get('description','null')
            self.rbi=result.get('rbi','null')
            self.awayScore=result.get('awayScore','null')
            self.homeScore=result.get('homeScore','null')

            self.atBatIndex=about.get('atBatIndex','null')
            self.halfInning=about['halfInning']
            self.inning=about['inning']
            
            self.startTime=datetime.strptime(about.get('startTime','1900-01-01T01:01:1.0Z'),'%Y-%m-%dT%H:%M:%S.%fZ')
            
            self.endTime=datetime.strptime(about.get('endTime','1900-01-01T01:01:01.0Z'),'%Y-%m-%dT%H:%M:%S.%fZ')
            
            self.isComplete=about.get('isComplete','null')
            self.isScoringPlay=about.get('isScoringPlay','null')
            self.hasReview=about.get('hasReview','null')
            self.hasOut=about.get('hasOut','null')
            self.captivatingIndex=about.get('captivatingIndex','null')

            self.batter_id=batter.get('id','null')
            self.pitcher_id=pitcher.get('id','null')

            self.count_balls=count.get('balls','null')
            self.count_strikes=count.get('striks','null')
            self.count_outs=count.get('outs','null')

            self.num_pitches=len(play['pitchIndex'])
            self.num_actions=len(play['actionIndex'])
            self.num_runners=len(play['runners'])

            self.game_id=game_id
            
            # for every play, there are pitches, runners, and actions
            pitch_dicts = [play['playEvents'][x] 
                           for x in play['pitchIndex'] 
                           if play['playEvents'][x]['isPitch']==True]
            pitch_records = []
            for pitch_dict in pitch_dicts:
                pitch_records.append(Pitch(pitch_dict,play_id,session))
                session.add_all(pitch_records)
                session.commit()


    id = Column(String(200),primary_key=True,unique=True)
    type = Column(String(10))
    event = Column(String(25))
    eventType = Column(String(25))
    description = Column(String(250))
    rbi = Column(Integer)
    awayScore = Column(Integer)
    homeScore = Column(Integer)
    
    atBatIndex = Column(Integer)
    halfInning = Column(String(10))
    inning = Column(Integer)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    isComplete = Column(Boolean)
    isScoringPlay = Column(Boolean)
    hasReview = Column(Boolean)
    hasOut = Column(Boolean)
    captivatingIndex = Column(Integer)
    
    batter_id = Column(Integer,ForeignKey("people.id"))
    pitcher_id = Column(Integer,ForeignKey("people.id"))
    
    count_balls = Column(Integer)
    count_strikes = Column(Integer)
    count_outs = Column(Integer)
    
    num_pitches = Column(Integer)
    num_actions = Column(Integer)
    num_runners = Column(Integer)
    
    def __repr__(self):
        return "<Play(game_id='%s',atBatIndex='%s')>" % (
                     self.game_id,self.atBatIndex)
    
# Declare mapping for the game table 
class Game(Base):
    __tablename__ = 'games'
    __table_args__ = {'extend_existing': True}
    
    def __init__(self,pk,session,commit=False,verbose=False):
        """
        Takes in a gamepk and a sql alchemy session, calls the 'game' api endpoint, and turns the information into a
        mapped class instance for that game as well as all the plays in that game. When commit=True, the 
        function will also add these instances to a sqlalchemy session and commit them to the database. 
        """
        try:
            already_added_pk = [item for sublist in session.execute('select pk from games').fetchall() for item in sublist]
        except:
            print("query for existing records didn't work")
            session.rollback()
            already_added_pk=[]
        if int(pk) not in already_added_pk:
            api_call = mlb.get('game',{'gamePk':pk})

            gameData = api_call['gameData']
            game = gameData['game']
            _datetime = gameData['datetime']
            status = gameData['status']
            weather = gameData['weather']
            probablePitchers = gameData['probablePitchers']

            liveData = api_call['liveData']
            all_plays = liveData['plays']['allPlays']
            

            self.pk=game['pk']
            self.type=game['type']
            self.doubleHeader=game['doubleHeader']
            self.id=game['id']
            self.gamedayType=game['gamedayType']
            self.tiebreaker=game['tiebreaker']
            self.gameNumber=game['gameNumber']
            self.calenderEventId=game['calendarEventID']
            self.season=game['season']

            self.dateTime=datetime.strptime(_datetime['dateTime'],'%Y-%m-%dT%H:%M:%SZ')
            self.originalDate=datetime.date(datetime.strptime(_datetime['originalDate'],"%Y-%m-%d"))
            self.dayNight=_datetime['dayNight']
            self.time=datetime.time(datetime.strptime(_datetime['time']+_datetime['ampm'],"%H:%M%p"))

            self.abstractGameState=status['abstractGameState']
            self.codedGameState=status['codedGameState']
            self.detailedState=status['detailedState']
            self.statusCode=status['statusCode']
            self.abstractGameCode=status['abstractGameCode']

            self.homeTeam_id=gameData['teams']['home']['id']
            self.awayTeam_id=gameData['teams']['away']['id']

            self.condition=weather.get('condition','null')
            self.temp=weather.get('temp','null')
            self.wind=weather.get('wind','null')

            self.venue_id=gameData['venue']['id']

            self.home_probablePitcher=probablePitchers.get('home',{'null':'null'}).get('id','null')
            self.away_probablePitcher=probablePitchers.get('away',{'null':'null'}).get('id','null') 
            
            play_records = []
            for play in all_plays:
                play_records.append(Play(play,game['id'],session,commit=commit))
            
            if commit:
                if verbose:
                    print('adding game record')
                session.add(self)
                if verbose:
                    print('adding play records')
                session.add_all(play_records)
                if verbose:
                    print('commit...')
                session.commit()
        
    
    pk = Column(Integer)
    type = Column(String(1))
    doubleHeader = Column(String(1))
    id = Column(String(150), primary_key=True,unique=True)
    gamedayType = Column(String(1))
    tiebreaker = Column(String(1))
    gameNumber = Column(Integer)
    calenderEventId = Column(String(50))
    season = Column(Integer)
    
    dateTime = Column(String(200))
    originalDate = Column(Date)
    dayNight = Column(String(12))
    time = Column(Time)
    
    abstractGameState = Column(String(12))
    codedGameState = Column(String(3))
    detailedState = Column(String(12))
    statusCode = Column(String(3))
    abstractGameCode = Column(String(3))
    
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

Play.game_id = Column(String(150),ForeignKey('games.id'))
Play.pitches = relationship('Pitch',order_by=Pitch.startTime,back_populates='play')    
Play.game = relationship("Game",back_populates="plays")

Game.plays = relationship(
    "Play",order_by=Play.id,back_populates='game')

Play.batter = relationship('Person',back_populates='hitter_at_bats',foreign_keys=Play.batter_id)
Play.pitcher = relationship('Person',back_populates='pitcher_at_bats',foreign_keys=Play.pitcher_id)

Person.hitter_at_bats = relationship('Play',order_by=Play.startTime,
                                     back_populates='batter',foreign_keys=Play.batter_id)

Person.pitcher_at_bats = relationship('Play',order_by=Play.startTime,
                                     back_populates='pitcher',foreign_keys=Play.pitcher_id)


class Team(Base):
    __tablename__ = 'teams'
    __table_args__ = {'extend_existing': True}
    
    def __init__(self,team_id):
        team = mlb.get('team',{'teamId':team_id})['teams'][0]
        
        self.id=team['id']
        self.name=team['name']
        self.venue_id=team['venue']['id']
        self.teamCode=team['teamCode']
        self.abbreviation=team['abbreviation']
        self.teamName=team['teamName']
        self.locationName=team.get('locationName','null')
        self.league_id=team.get('league',{'id':'null'})['id']
        self.division_id=team.get('division',{'id':'null'})['id']
    
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    venue_id = Column(Integer)
    teamCode = Column(String(10))
    abbreviation = Column(String(10))
    teamName = Column(String(25))
    locationName = Column(String(25))
    league_id = Column(Integer)
    division_id = Column(Integer)
    
    def __repr__(self):
        return "<Team(name='%s')>" % self.name
    
class GameTeamLink(Base):
    __tablename__ = 'game_team_link'
    __table_args__ = {'extend_existing': True}
    
    def __init__(self,game_id,home_away='home'):
        def get_roster_inputs(query):   
            roster_inputs = []
            for instance in query.all():
                roster_input_dict = {'date':instance.dateTime.split(' ')[0],
                                     'season':instance.season,
                                     'homeTeam':instance.homeTeam_id,
                                     'awayTeam':instance.awayTeam_id,
                                     }
                roster_inputs.append(roster_input_dict)

            return roster_inputs
    
        def get_roster(roster_input_dict):
            if home_away=='home':
                home = mlb.get('team_roster',
                               {'teamId':roster_input_dict['homeTeam'],
                                'rosterType':'active',
                                'season':roster_input_dict['season'],
                                'date':roster_input_dict['date']
                               })['roster']
                home_roster_ids = [x['person']['id'] for x in home]
                player_list = ['player_'+str(x) for x in range(1,len(home_roster_ids)+1)]
                home_roster_dict = {x:y for x,y in zip(player_list,home_roster_ids)}
                home_roster_dict['teamId'] = roster_input_dict['homeTeam']
                
                roster_dict = home_roster_dict
            
            elif home_away=='away':
                away = mlb.get('team_roster',
                               {'teamId':roster_input_dict['awayTeam'],
                                'rosterType':'active',
                                'season':roster_input_dict['season'],
                                'date':roster_input_dict['date']
                               })['roster']
                away_roster_ids = [x['person']['id'] for x in away]
                player_list = ['player_'+str(x) for x in range(1,len(away_roster_ids)+1)]
                away_roster_dict = {x:y for x,y in zip(player_list,away_roster_ids)}
                away_roster_dict['teamId']=roster_input_dict['awayTeam']
                
                roster_dict = away_roster_dict
            return roster_dict
    
        game_query = session.query(Game).filter_by(id=game_id)
        roster_input_dicts = get_roster_inputs(game_query)
        roster = get_roster(roster_input_dicts[0])

        

        self.game_id=game_id
        self.team_id=roster['teamId']

        self.player_1_id = roster.get('player_1','null')
        self.player_2_id = roster.get('player_2','null')
        self.player_3_id = roster.get('player_3','null')
        self.player_4_id = roster.get('player_4','null')
        self.player_5_id = roster.get('player_5','null')
        self.player_6_id = roster.get('player_6','null')
        self.player_7_id = roster.get('player_7','null')
        self.player_8_id = roster.get('player_8','null')
        self.player_9_id = roster.get('player_9','null')
        self.player_10_id = roster.get('player_10','null')
        self.player_11_id = roster.get('player_11','null')
        self.player_12_id = roster.get('player_12','null')
        self.player_13_id = roster.get('player_13','null')
        self.player_14_id = roster.get('player_14','null')
        self.player_15_id = roster.get('player_15','null')
        self.player_16_id = roster.get('player_16','null')
        self.player_17_id = roster.get('player_17','null')
        self.player_18_id = roster.get('player_18','null')
        self.player_19_id = roster.get('player_19','null')
        self.player_20_id = roster.get('player_20','null')
        self.player_21_id = roster.get('player_21','null')
        self.player_22_id = roster.get('player_22','null')
        self.player_23_id = roster.get('player_23','null')
        self.player_24_id = roster.get('player_24','null')
        self.player_25_id = roster.get('player_25','null')
        self.player_26_id = roster.get('player_26','null')
        self.player_27_id = roster.get('player_27','null')
        self.player_28_id = roster.get('player_28','null')
        self.player_29_id = roster.get('player_29','null')
        self.player_30_id = roster.get('player_30','null')
        self.player_31_id = roster.get('player_31','null')
        self.player_32_id = roster.get('player_32','null')
        self.player_33_id = roster.get('player_33','null')
        self.player_34_id = roster.get('player_34','null')
        self.player_35_id = roster.get('player_35','null')
        self.player_36_id = roster.get('player_36','null')
        self.player_37_id = roster.get('player_37','null')
        self.player_38_id = roster.get('player_38','null')
        self.player_39_id = roster.get('player_39','null')
        self.player_40_id = roster.get('player_40','null')

    game_id = Column(String(150),ForeignKey('games.id'),primary_key=True)
    team_id = Column(Integer,ForeignKey('teams.id'),primary_key=True)
    
    # add roster at the time of game 
    player_1_id = Column(Integer,ForeignKey('people.id'))
    player_2_id = Column(Integer,ForeignKey('people.id'))
    player_3_id = Column(Integer,ForeignKey('people.id'))
    player_4_id = Column(Integer,ForeignKey('people.id'))
    player_5_id = Column(Integer,ForeignKey('people.id'))
    player_6_id = Column(Integer,ForeignKey('people.id'))
    player_7_id = Column(Integer,ForeignKey('people.id'))
    player_8_id = Column(Integer,ForeignKey('people.id'))
    player_9_id = Column(Integer,ForeignKey('people.id'))
    player_10_id = Column(Integer,ForeignKey('people.id'))
    player_11_id = Column(Integer,ForeignKey('people.id'))
    player_12_id = Column(Integer,ForeignKey('people.id'))
    player_13_id = Column(Integer,ForeignKey('people.id'))
    player_14_id = Column(Integer,ForeignKey('people.id'))
    player_15_id = Column(Integer,ForeignKey('people.id'))
    player_16_id = Column(Integer,ForeignKey('people.id'))
    player_17_id = Column(Integer,ForeignKey('people.id'))
    player_18_id = Column(Integer,ForeignKey('people.id'))
    player_19_id = Column(Integer,ForeignKey('people.id'))
    player_20_id = Column(Integer,ForeignKey('people.id'))
    player_21_id = Column(Integer,ForeignKey('people.id'))
    player_22_id = Column(Integer,ForeignKey('people.id'))
    player_23_id = Column(Integer,ForeignKey('people.id'))
    player_24_id = Column(Integer,ForeignKey('people.id'))
    player_25_id = Column(Integer,ForeignKey('people.id'))
    player_26_id = Column(Integer,ForeignKey('people.id'))
    player_27_id = Column(Integer,ForeignKey('people.id'))
    player_28_id = Column(Integer,ForeignKey('people.id'))
    player_29_id = Column(Integer,ForeignKey('people.id'))
    player_30_id = Column(Integer,ForeignKey('people.id'))
    player_31_id = Column(Integer,ForeignKey('people.id'))
    player_32_id = Column(Integer,ForeignKey('people.id'))
    player_33_id = Column(Integer,ForeignKey('people.id'))
    player_34_id = Column(Integer,ForeignKey('people.id'))
    player_35_id = Column(Integer,ForeignKey('people.id'))
    player_36_id = Column(Integer,ForeignKey('people.id'))
    player_37_id = Column(Integer,ForeignKey('people.id'))
    player_38_id = Column(Integer,ForeignKey('people.id'))
    player_39_id = Column(Integer,ForeignKey('people.id'))
    player_40_id = Column(Integer,ForeignKey('people.id'))
    
    #relationships
    game = relationship('Game',back_populates='teams')
    team = relationship('Team',back_populates='games')
    
    def __repr__(self):
        return "<GameTeamLink(game_id='%s',team_id='%s')>" % (self.game_id,self.team_id)

# update game and team tables 
Game.teams = relationship("GameTeamLink",back_populates='game')
Team.games = relationship("GameTeamLink",back_populates='team')

Base.metadata.create_all(db.db_engine)

# Create visualization
import sqlalchemy_schemadisplay
from sqlalchemy import MetaData

schema_viz = sqlalchemy_schemadisplay.create_schema_graph(metadata=MetaData(db.db_engine))
schema_viz.write_png('dbschema.png')