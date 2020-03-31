from gamePks import gamePks
from database import *

for year in gamePks.keys()
    (db.insert_game(game,replace=True) for game in gamePks[year])
    print(f"{year} completed")