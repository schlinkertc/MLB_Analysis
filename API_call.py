import statsapi as mlb
from datetime import datetime as dt
import os,re,csv
from os import walk
import pandas as pd
import joblib 
import copy 

def get_game(api_call):
        gameData = api_call['gameData']
        dateTime = gameData['datetime']
        game = gameData['game']
        weather = gameData['weather']
        status = gameData['status']
        probablePitchers = gameData['probablePitchers']

        keys_to_add = ['dateTime','originalDate',
                       'condition','temp','wind',
                       'detailedState'
                      ]
        dicts = [weather,dateTime,status]
        for k in keys_to_add:
            for d in dicts:
                try:
                    game[k]=d[k]
                except KeyError:
                    continue

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
        
        #put it in a list for consistency with other records
        list_game = []
        list_game.append(game)
        return list_game

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
        matchup = play.copy().pop('matchup')
        #foreign keys to play 'atBatIndex', 'playEndTime'
        fks=['atBatIndex', 'playEndTime']
            
        matchup.update(
            {k:v for k,v in zip(fks,[play.get(fk,'-') for fk in fks])}
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
                    {k:v for k,v in zip(fks,[play.get(fk,'-') for fk in fks])}
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
                {k:v for k,v in zip(fks,[play.get(fk,'-') for fk in fks])}
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
                {k:v for k,v in zip(fks,[play.get(fk,'-') for fk in fks])}
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
                {k:v for k,v in zip(fks,[play.get(fk,'-') for fk in fks])}
            )
            try:
                temp_credits = runner.pop('credits')
                
                for credit in temp_credits:
                    credit.update(
                        {k:v for k,v in zip(fks,[play.get(fk,'-') for fk in fks])}
                    )
                
                    credits.append(flatten_dicts(credit))
            except KeyError:
                pass 
            runners.append(flatten_dicts(runner))
    
    [r.update(gamePk) for r in runners]
    [c.update(gamePk) for c in credits]
    
    for runner in runners:
        if runner['movement_start']==None:
            runner['movement_start']='-'
        if runner['movement_end']==None:
            runner['movement_end']= '-'
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
                {k:v for k,v in zip(fks,[play.get(fk,'-') for fk in fks])}
            )
            
            actions.append(flatten_dicts(action))
    
    [a.update(gamePk) for a in actions]
    return actions

def get_players(API_result):
    #fk for game_player_link
    gamePk=API_result['gamePk']
    
    players = API_result['gameData']['players']
    players = [flatten_dicts(players[player_id]) for player_id in players.keys()]
    
#     game_player_links = []
#     for player in players:
#         link = {'player':player['id'],'gamePk':gamePk}
#         game_player_links.append(link)
    
    return players

def get_gamePlayerLink(API_result):
    gamePk={'gamePk':API_result['gamePk'],
            'gameDateTime':API_result['gameData']['datetime']['dateTime']}
    boxscore = API_result['liveData']['boxscore']
    player_dicts = []
    for team in ['home','away']:
        players = boxscore['teams'][team]['players']
        for k in players.keys():
            player_dicts.append(flatten_dicts(players[k]))
    
    [p.update(gamePk) for p in player_dicts]
    
    for player_dict in player_dicts:
        try:
            player_dict['allPositions'] = ''.join(
                [ d['code']+', ' for d in player_dict['allPositions'] ]
            )
        except KeyError:
            continue 
    return player_dicts

def get_teams(API_result):
    #fk for game_team_link
    gamePk=API_result['gamePk']
    teams_dict = API_result['gameData']['teams']
    
    teams = []
    links = []
    team_records = []
    for key in ['home','away']:
        team = teams_dict[key].copy()
        
        team_record = team.pop('record')
        team_record.update({'gamePk':gamePk})
        team_record['team_id']=team['id']
        team_records.append(flatten_dicts(team_record))
        
        teams.append(flatten_dicts(team))
        
        link = {'gamePk':gamePk,
                'team_id':team['id'],
                'home_away':key}
        links.append(link)
        
    return teams, links, team_records

def get_venue(API_result):
    venue = API_result['gameData']['venue']
    venue = flatten_dicts(venue)
    
    #put it in a list for consistency
    venue_list = []
    venue_list.append(venue)
    return venue_list

class API_call():
    
    pickled_calls = []
    for (dirpath, dirnames, filenames) in walk('API_results/'):
        pickled_calls.extend(filenames)
        break
    pickled_calls = [x.strip('.pkl') for x in pickled_calls]
    
    def __init__(self,gamePk):
        gamePk = str(gamePk)
        storedResultsDirectory = "API_results/"
        self._pickle_path = str(storedResultsDirectory+gamePk+'.pkl')
        
        if gamePk in API_call.pickled_calls:
            self._result = joblib.load(self._pickle_path)
        else:
            self._result = mlb.get('game',{'gamePk':gamePk})
            self._pickle = joblib.dump(self._result,self._pickle_path)
            API_call.pickled_calls.append(gamePk)
        
        # I don't want to change the underlying api response
        result = copy.deepcopy(self._result)
        
        self.games = get_game(result)
        self.venues = get_venue(result)
        self.teams, self.game_team_links, self.team_records = get_teams(result)
        self.players = get_players(result)
        self.plays,self.matchups,self.hotColdZones,self.hotColdStats = get_plays(result)
        self.actions = get_actions(result)
        self.pitches = get_pitches(result)
        self.runners, self.credits = get_runners(result)
        self.game_player_links = get_gamePlayerLink(result)
        
    def __repr__(self):
        return f"<API Call: gamePk={self._result['gamePk']}>"
        
# class Games_DataFrames():

#     def __init__(self,gamePks):
#         """
#         takes in a list of gamePks, instantiates API_call object for each game, 
#             returns dataframes for db inserts
#         """
#         self._calls = [API_call(gamePk) for gamePk in gamePks]
#         call_dict = {k:v for k,v in self._calls[0].__dict__.items() if k[0]!= '_'}
        
#         for k in call_dict.keys():
#             if type(call_dict[k])==dict:
#                 v = []
#                 v.append(call_dict[k])
#                 call_dict[k]=v
#         for call in self._calls[1:]:
#             for k,v in call.__dict__.items():
#                 try:
#                     call_dict[k].extend(v)
#                 except KeyError:
#                     pass
        
#         for k,v in call_dict.items():
#             setattr(self,k,v)
#         for k,v in self.__dict__.items():
#             if k[0] != '_':
#                 try:
#                     setattr(self,k,pd.DataFrame.from_records(v))
#                 except AttributeError:
#                     pass
                    
        

# for later: update game_player_links with teamIds        
def get_roster_inputs(api_call):
    return {
        'season':api_call.game['season'],
        'rosterType':'active',
        'date':api_call.game['dateTime'].strftime("%m/%d/%Y")
    }

def update_gamePlayerLinks(game):
    roster_inputs = get_roster_inputs(game)
    players =  {}
    for team in game.teams:
        params = get_roster_inputs(call)
        params.update({"teamId":team['id']})
        roster = mlb.get('team_roster',params)
        team_players = [x['person']['id'] for x in roster['roster']]
        players[team['id']] = team_players

    for d in game.game_player_links:
        for k in players.keys():
            if d['player'] in players[k]:
                d.update({'teamId':k})    
        
        
        
        
    
    
    