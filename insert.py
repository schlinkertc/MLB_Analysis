from API_call import API_call
from gamePks import *
import statsapi as mlb
import pandas as pd

from tables import *
import relationships

years = ['2017','2018','2019']

games = []
for year in years:
    games.extend(gamePks[year])

exists = [str(x[0]) for x in db.db_engine.execute('select pk from games').fetchall()]

games = [g for g in games if g not in exists]

print(len(games))

for game in games:
    try:
        db.insert_game(game,replace=True)
    except: 
        print(game)