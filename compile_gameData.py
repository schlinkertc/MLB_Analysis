from API_call import API_call
from gamePks import *
import statsapi as mlb
import pandas as pd
import numpy as np

from tables import *
import relationships

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db.db_engine)
session = Session()

def get_game_features(game_record):
    date = dt.strftime(game_record.dateTime,"%Y-%m-%d")
    pk = game_record.pk
    season = game_record.season
    
    #offense
    stmt=f"""
    SELECT
        p.gamePk,
        p.home_away,
        (
            sum(s.hits) +
            sum(s.baseOnBalls) +
            sum(s.intentionalWalks) +
            sum(s.hitByPitch) 
        ) /
        (   sum(s.atBats) + 
            sum(s.baseOnBalls) +
            sum(s.intentionalWalks) +
            sum(s.hitByPitch)
        ) as offense,

        (sum(s.totalBases) - sum(s.hits)) / sum(s.atBats) as power,
        sum(s.runs) / 
        (
            sum(s.hits) +
            sum(s.baseOnBalls) +
            sum(s.intentionalWalks) +
            sum(s.hitByPitch) 
        ) as clutch
    FROM 
        game_player_links p
    INNER JOIN 
        game_batting_stats s ON p.person_id=s.person_id
    INNER JOIN 
        players on players.id=p.person_id
    WHERE
        p.gamePk = {pk} AND players.primaryPosition_name != 'Pitcher'
    AND 
        s.gamePk
    IN
        (Select pk from games where season = {season} and type = 'R' and dateTime < "{date}")
    group by 
        p.home_away
    having 
        sum(p.gameStatus_isSubstitute)/sum(s.gamesPlayed) < .9
        """
    off = pd.read_sql(stmt,engine)
    off.set_index('home_away',inplace=True)
    
    # for relievers
    stmt=f"""
    SELECT 
        p.home_away,
        sum(s.hits) / sum(s.atBats) as r_oppBa,
        ( sum(s.baseOnBalls) + sum(s.hitBatsmen) )
        /
        ( sum(s.atBats) +  sum(s.baseOnBalls) + sum(s.hitBatsmen) ) as r_oppBb,
        sum(s.earnedRuns) 
        /
        ( sum(s.hits) +  sum(s.baseOnBalls) + sum(s.hitBatsmen) ) as r_oppEr

    FROM 
        game_player_links p
    INNER JOIN 
        game_pitching_stats s ON p.person_id=s.person_id
    INNER JOIN 
        players on players.id=p.person_id
    INNER JOIN 
        games g ON g.pk=s.gamePk
    WHERE
        p.gamePk = {pk} AND players.primaryPosition_name = 'Pitcher'
        AND 
        g.season = {season} and g.type = 'R' and g.dateTime < "{date}"
    group by 
        p.home_away
    having
        sum(s.inningsPitched)/sum(s.gamesPitched) < 3 
        AND
        sum(s.gamesStarted)/sum(s.gamesPitched) < .9
        """
    relief = pd.read_sql(stmt,engine)
    relief.set_index('home_away',inplace=True)
    
    # for starter
    stmt=f"""
    SELECT 
        p.home_away,
        sum(s.hits) / sum(s.atBats) as s_oppBa,
        ( sum(s.baseOnBalls) + sum(s.hitBatsmen) )
        /
        ( sum(s.atBats) +  sum(s.baseOnBalls) + sum(s.hitBatsmen) ) as s_oppBb,
        sum(s.earnedRuns) 
        /
        ( sum(s.hits) +  sum(s.baseOnBalls) + sum(s.hitBatsmen) ) as s_oppEr

    FROM 
        game_player_links p
    INNER JOIN 
        game_pitching_stats s ON p.person_id=s.person_id
    INNER JOIN 
        players on players.id=p.person_id
    INNER JOIN 
        games g ON g.pk=s.gamePk
    WHERE
        p.gamePk = {pk}
        AND 
        g.season = {season} and g.type = 'R' and g.dateTime < "{date}"
        AND
        players.id = g.home_probablePitcher or players.id = away_probablePitcher
    group by 
        p.home_away
        """
    starters = pd.read_sql(stmt,engine)
    starters.set_index('home_away',inplace=True)
    
    df = pd.concat([off,relief,starters],sort=False,axis=1)
    records = df.to_dict(orient='index')
    
    d = {}
    for team in ['home','away']:
        keys = records[team].keys()
        for k in keys:
            if k != 'gamePk':
                d[f"{team}_{k}"] = records[team][k]
            d['gamePk']=records[team]['gamePk']
    return d

games = session.query(Game).filter(Game.type=='R').all()

data = [get_game_features(game) for game in games]

data = pd.DataFrame.from_records(data)

def get_homeTeam_win(gamePk):
    gamePk = str(int(gamePk))
    stmt = f"""
    SELECT 
        sum(BS.runs) as runs,
        L.home_away,
        L.gamePk
    FROM 
        game_batting_stats BS
    INNER JOIN 
        game_player_links L
        ON L.person_id = BS.person_id
    WHERE
        L.gamePk = {gamePk}
        and BS.gamePk = {gamePk}
    GROUP BY 
        L.home_away
    ORDER BY 
        runs desc
    LIMIT
        1
    """
    d = {}
    with db.db_engine.connect() as connection:
        result = connection.execute(stmt).fetchone()
        if result==None:
            d['homeTeam_win']= np.nan
        elif result['home_away']=='home':
            d['homeTeam_win']=1
        else:
            d['homeTeam_win']=0
    return d['homeTeam_win']
    

data['homeTeam_win'] = data.apply(lambda x: get_homeTeam_win(x['gamePk']),axis=1)

data.dropna(inplace=True)

data.to_csv('game_dataset.csv',index=False)