from datetime import datetime as dt
import os,re,csv
from os import walk
import statsapi as mlb

#dates from the 'season' endpoint are returned in a different format than what we need to query the API
#we'll use this function to take care of that in a moment
def convert_date(date):
    date = dt.strptime(date,"%Y-%m-%d")
    convertedDate = dt.strftime(date,"%m/%d/%Y")
    return convertedDate

def get_gamePks(seasons,target_directory=None):
    """
    Takes in a list of seasons as strings representing their year e.g. ['2018','2019']
    Queries the MLB API to find gamePks for each season and writes them to CSV files
    if a target directory for the gamePks is not specified, a directory called 'gamePks'
    will be added to the current directory. 
    """
    if target_directory:
        gamePks_path = target_directory
    else:
        #create a directory to store CSVs
        try:
            os.mkdir(os.getcwd()+'/gamePks')
        except FileExistsError:
            pass
        gamePks_path=os.getcwd()+'/gamePks'
    
    #walk the gamePks directory to see if we've already added any seasons
    f = []
    for (dirpath, dirnames, filenames) in walk(gamePks_path):
        f.extend(filenames)
        break
    years = [re.findall('[^.csv]+',x) for x in f]
    already_added = [item for sublist in years for item in sublist if item[0] in ['1','2']]
    seasons = list(set(seasons)-set(already_added))
    
    #query the API to get start dates and end dates for all seasons
    all_seasons = mlb.get('seasons',{'sportId':1,'all':True})['seasons']
    
    #filter out the ones we don't care about right now
    seasons = list(filter(lambda x: x['seasonId'] in seasons,all_seasons))
    
    gamePks = {}
    for season in seasons:  
        year = season['seasonId']
        startDate = convert_date(season['seasonStartDate'])
        endDate = convert_date(season['seasonEndDate'])
        
        #returns a list of dicts for each date in the range
        #each dict has a 'games' key with a list of dicts for each game in that day as values
        dates = mlb.get('schedule',{'sportId':1,'startDate':startDate,'endDate':endDate})['dates']
        
        #for each date, and for each game in that date, get the gamePk 
        gamePks[year]= [ game['gamePk'] 
                                          for date in dates 
                                          for game in date['games'] ]
        #store the gamePks as CSVs
        with open(gamePks_path + f"/{year}.csv", 'w',newline='') as myfile:
            wr = csv.writer(myfile,quoting=csv.QUOTE_ALL)
            wr.writerow(gamePks[year])

def read_gamePks():
    gamePks_path = os.curdir+'/gamePks'
    f = []
    for (dirpath, dirnames, filenames) in walk(gamePks_path):
        f.extend(filenames)
        break
    pk_paths = [gamePks_path + '/' + x for x in f if x[0]!= '.']
    
    gamePks = {}
    for path in pk_paths:
        season = re.findall('/gamePks/([^.csv]+)',path)
        with open(path, 'r') as f:
            reader = csv.reader(f)
            seasonPks = list(reader)
        gamePks[season[0]] = [item for sublist in seasonPks for item in sublist]
    return gamePks