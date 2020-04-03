from API_call import API_call
from gamePks import *
import statsapi as mlb
import pandas as pd

from tables import *
import relationships

games = gamePks['2019']

for game in games:
    db.insert_game(game,replace=True)