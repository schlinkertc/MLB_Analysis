import statsapi as mlb
from datetime import datetime as dt
import os,re,csv
from os import walk

def get_game(api_call):
        gameData = api_call['gameData']
        dateTime = gameData['datetime']
        game = gameData['game']
        weather = gameData['weather']
        timeZone = gameData['venue']['timeZone']
        status = gameData['status']
        probablePitchers = gameData['probablePitchers']

        keys_to_add = ['dateTime','originalDate',
                       'condition','temp','wind',
                       'tz','detailedState'
                      ]
        dicts = [weather,dateTime,timeZone,status]
        for k in keys_to_add:
            for d in dicts:
                try:
                    game[k]=d[k]
                except KeyError:
                    continue
        #'seasonDisplay' key:value seems to be redundant
        del game['seasonDisplay']

        home_team = gameData['teams']['home']
        away_team = gameData['teams']['away']

        game['homeTeam_id'] = home_team['id']
        game['awayTeam_id'] = away_team['id']

        game['venue_id'] = gameData['venue']['id']

        for team in ['home','away']:
            try:
                game[f"{team}_probablePitcher"]=probablePitchers[team]['id']
            except KeyError:
                pass

        #format the dateTime and originalDate
        fmt = "%Y-%m-%dT%H:%M:%SZ" 
        game['dateTime'] = dt.strptime(game['dateTime'],fmt)
        fmt = "%Y-%m-%d"
        game['originalDate'] = dt.strptime(game['originalDate'],fmt).date()

        return game

def flatten_dicts(dictionary):
    """
    recursively flatten a dictionary of dictionaries
    """
    #base case 
    if dict not in [type(x) for x in dictionary.values()]:
        return dictionary
    else:
        for key, value in dictionary.items():
            if type(value)==dict:
                temp_dict = dictionary.pop(key)
                for k,v in temp_dict.items():
                    dictionary[f"{key}_{k}"]=v
                return flatten_dicts(dictionary)

def get_plays(API_result):
    #foreign key references games table
    gamePk={'gamePk':API_result['gamePk']}
    
    allPlays = API_result['liveData']['plays']['allPlays']
    keys = ['result','about','count']
    plays = []
    matchups = []
    hotColdZones = []
    for play in allPlays:
        play_dict = {k:v for k,v in zip(keys,[play[key] for key in keys])}.copy()
        plays.append(flatten_dicts(play_dict))
        matchup = play.pop('matchup')
        #foreign keys to play 'atBatIndex', 'playEndTime'
        fks=['atBatIndex', 'playEndTime']
            
        matchup.update(
            {k:v for k,v in zip(fks,[play[fk] for fk in fks])}
        )
        for x in ['pitcher','batter']:
            hotColdZone =  matchup.pop(f"{x}HotColdZones")
            for zone in hotColdZone:
                try:
                    zone.update(
                        matchup.pop(f'{x}HotColdZoneStats')
                    )
                except KeyError:
                    pass
                zone.update(
                    {k:v for k,v in zip(fks,[play[fk] for fk in fks])}
                )
                zone.update({'type':x})
                hotColdZones.append(flatten_dicts(zone))
        
        matchups.append(flatten_dicts(matchup))
    
    [hc.update(gamePk) for hc in hotColdZones]        
    [m.update(gamePk) for m in matchups]
    [p.update(gamePk) for p in plays]
    
    hotColdStats = []
    for hc in hotColdZones:
        try:
            stats = hc.pop('stats')
        except KeyError:
            continue
        for stat in stats:
            stat.update(gamePk)
            stat.update(
                {k:v for k,v in zip(fks,[play[fk] for fk in fks])}
            )
            hotColdStats.append(flatten_dicts(stat))
        
    return plays,matchups,hotColdZones,hotColdStats
        
def get_pitches(API_result):
    #foreign key references games table
    gamePk={'gamePk':API_result['gamePk']}
    
    allPlays = API_result['liveData']['plays']['allPlays']
    
    pitches = []
    for play in allPlays:
        for i in play['pitchIndex']:
            pitch = play['playEvents'][i]
            #foreign keys to play 'atBatIndex', 'playEndTime'
            fks=['atBatIndex', 'playEndTime']
            
            pitch.update(
                {k:v for k,v in zip(fks,[play[fk] for fk in fks])}
            )
            
            pitches.append(flatten_dicts(pitch))
    
    [p.update(gamePk) for p in pitches]
    return pitches

def get_runners(API_result):
    #foreign key references games table
    gamePk={'gamePk':API_result['gamePk']}
    
    allPlays = API_result['liveData']['plays']['allPlays']
    
    runners = []
    credits = []
    for play in allPlays:
        for i in play['runnerIndex']:
            runner = play['runners'][i]
            
            fks=['atBatIndex', 'playEndTime']
            
            runner.update(
                {k:v for k,v in zip(fks,[play[fk] for fk in fks])}
            )
            try:
                temp_credits = runner.pop('credits')
                
                for credit in temp_credits:
                    credit.update({k:v for k,v in zip(fks,[play[fk] for fk in fks])})
                
                    credits.append(flatten_dicts(credit))
            except KeyError:
                pass 
            runners.append(flatten_dicts(runner))
    
    [r.update(gamePk) for r in runners]
    return runners,credits

def get_actions(API_result):
    #foreign key references games table
    gamePk={'gamePk':API_result['gamePk']}
    
    allPlays = API_result['liveData']['plays']['allPlays']
    
    actions = []
    for play in allPlays:
        for i in play['actionIndex']:
            action = play['playEvents'][i]
            #foreign keys to play 'atBatIndex', 'playEndTime'
            fks=['atBatIndex', 'playEndTime']
            
            action.update(
                {k:v for k,v in zip(fks,[play[fk] for fk in fks])}
            )
            
            actions.append(flatten_dicts(action))
    
    [a.update(gamePk) for a in actions]
    return actions

def get_players(API_result):
    #fk for game_player_link
    gamePk=API_result['gamePk']
    
    players = API_result['gameData']['players']
    players = [flatten_dicts(players[player_id]) for player_id in players.keys()]
    
    game_player_links = []
    for player in players:
        link = {'player':player['id'],'gamePk':gamePk}
        game_player_links.append(link)
    
    return players,game_player_links

def get_teams(API_result):
    #fk for game_team_link
    gamePk=API_result['gamePk']
    teams_dict = API_result['gameData']['teams']
    
    teams = []
    links = []
    team_records = []
    for key in ['home','away']:
        team = teams_dict[key]
        
        team_record = team.pop('record')
        team_record.update({'gamePk':gamePk})
        team_records.append(team_record)
        
        teams.append(flatten_dicts(team))
        
        link = {'gamePk':gamePk,
                'team_id':team['id'],
                'home_away':key}
        links.append(link)
        
    return teams, links, team_records

def get_venue(API_result):
    venue = API_result['gameData']['venue']
    return flatten_dicts(venue)

class API_call():
    
    def __init__(self,gamePk):
        self._result = mlb.get('game',{'gamePk':gamePk})
        self.game = get_game(self._result)
        self.venue = get_venue(self._result)
        self.teams, self.game_team_links, self.team_records = get_teams(self._result)
        self.players, self.game_player_links = get_players(self._result)
        self.plays,self.matchups,self.hotColdZones,self.hotColdStats = get_plays(self._result)
        self.actions = get_actions(self._result)
        self.pitches = get_pitches(self._result)
        self.runners, self.credits = get_runners(self._result)
        
        
    
    
    