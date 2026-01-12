import os
import sys
from logging import DEBUG
from pathlib import Path
import json
from datetime import datetime

project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

from yfpy import Data
from yfpy.logger import get_logger
from yfpy.query import YahooFantasySportsQuery

"""
Team Friends Fantasy league URL: https://football.fantasysports.yahoo.com/league/bop_bop
"""

##############################################################
### ENVIRONMENT SETUP ########################################
##############################################################

#set directory location of private.json for authentication
auth_dir = project_dir

#set target directory for data output
data_dir = Path(__file__).parent.parent / "dataStore"

#create YFPY Data instance for saving/loading data
data = Data(data_dir)

##############################################################
################ VARIABLE SETUP###############################
##############################################################
def parse_auth():
    f = open('private.json')    #private.json needs to exist in same directory structure as this script
    auth = json.load(f)
    auth_key = auth['consumer_key']
    auth_secret = auth['consumer_secret']
    
    f.close()
    return auth_key, auth_secret

auth_key, auth_secret = parse_auth()

def get_season():
    #season = 2023
    season = 2025
    return season

season = get_season()

def get_chosen_week():
    finalWeek = 17
    today = datetime.now().strftime("%Y-%m-%d")
    lstWeeks = yahoo_query.get_game_weeks_by_game_id(game_id)
    for wk in lstWeeks:
        if wk.week == finalWeek:
            return wk.week
        else:
            if wk.start <= today <= wk.end:
                return wk.week

#chosen_week = get_chosen_week()

def get_chosen_date():
    chosen_date = "2025-09-05"  #NFL season opener
    return chosen_date
    
chosen_date = get_chosen_date()

def get_game_code():
    game_code = "nfl"   #Fantasy Football
    #game_code = "mlb"  #Fantasy Baseball
    return game_code
    
game_code = get_game_code()

def get_game_id():
    #https://developer.yahoo.com/fantasysports/guide/#game-resource
    #game_id = 423   #NFL - 2023
    game_id = 461   #NFL - 2024
    return game_id
    
game_id = get_game_id()

def get_league_id():
    #Fantasy Football
    #league_id = "17343"	#2023 season
    league_id = "31501" #2024 season
    return league_id
    
league_id = get_league_id()

def get_team_id():
    #Fantasy Football
    team_id = 1 #me
    return team_id
    
team_id = get_team_id()

def get_team_name():
    team_name = "Cåptain Crünch"    #me - 2024
    return team_name
    
team_name = get_team_name()

def get_player_id():
    #Fantasy Football
    player_id = 30977   #Josh Allen
    return player_id
    
player_id = get_player_id()

def get_league_player_limit():
    league_player_limit = 101
    return league_player_limit
    
league_player_limit = get_league_player_limit()

print(f'FF season: {season}')
print(f'game_id: {game_id}')
print(f'league_id: {league_id}')
print('-----------------------')
##############################################################
################ QUERY SETUP #################################
##############################################################
#configure Yahoo Fantasy Sports query (change all_output_as_json_str=True if you want to output JSON strings)
yahoo_query = YahooFantasySportsQuery(
    league_id,
    game_code,
    game_id=game_id,
    offline=False,
    all_output_as_json_str=False,
    yahoo_consumer_key=auth_key,
    yahoo_consumer_secret=auth_secret)
    
#manually override league key for example code to work
yahoo_query.league_key = f"{game_id}.l.{league_id}"

#manually override player key for example code to work
#player_key = f"{game_id}.p.{player_id}"

#-----------League Setup--------------------------------------
chosen_week = get_chosen_week()
print(f"Current Week: {chosen_week}")

#------------Team Info store----------------------------------
teamsDict = yahoo_query.get_league_teams()

op = open(os.path.join(data_dir,'allTeams.json'), 'r+')
currentList = json.load(op)
#writeList = list()
for team in teamsDict:
    ownerMatch = next((item for item in currentList if item["name"] == team.managers[0].nickname), None)
    if (ownerMatch["teamname"] != team.name.decode('UTF-8')):
        ownerMatch["teamname"] = team.name.decode('UTF-8')
        owner = ownerMatch["name"].replace(" ","")
        print(f'****{owner} changed their team name to {team.name}****')
        with open(os.path.join(data_dir,f'{owner}.name'),'w') as np:
            np.write(ownerMatch["teamname"])
#    writeDict = {"team_id": team.team_id, "name": team.managers[0].nickname, "teamname": team.name.decode('UTF-8')}
#    writeList.append(writeDict)
    print(f'{team.team_id} - {team.managers[0].nickname} - {team.name.decode("UTF-8")}')
op.seek(0)
json.dump(currentList, op)
op.truncate()
op.close()
#with open(os.path.join(data_dir,'allTeams.json'), 'w+') as fp:
#    json.dump(writeList, fp)
print('-----------------------')

#------------Weekly Hi Score store----------------------------
scores = {}
lstHighs = []
fileScore = os.path.join(data_dir, f"{season}scores.json")
for j in range(1,18):   # 14 reg season, plus 3 playoff weeks
    print(f"Finding hiScore for week {j}...")
    for i in range(1,13):
        wkScores = yahoo_query.get_team_stats_by_week(i, j)
        scores[teamsDict[i-1].name.decode('UTF-8')] = wkScores['team_points'].total
    max_key, max_value = max(scores.items(), key=lambda k: k[1])
    hiScore = {}
    hiScore['week'] = j
    hiScore['team'] = max_key
    hiScore['score'] = max_value
    lstHighs.append(hiScore)

with open(fileScore, 'w+') as fp:
    fp.write(json.dumps(lstHighs, indent=4))
    
##############################################################
################ QUERY EXAMPLES ##############################
##############################################################

#print(repr(yahoo_query.get_all_yahoo_fantasy_game_keys()))
#print(repr(yahoo_query.get_game_key_by_season(season)))
#print(repr(yahoo_query.get_current_game_info()))
#print(repr(yahoo_query.get_current_game_metadata()))
#print(repr(yahoo_query.get_game_info_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_metadata_by_game_id(game_id)))
#print(repr(yahoo_query.get_game_weeks_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_stat_categories_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_position_types_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_roster_positions_by_game_id(game_id)))
# print(repr(yahoo_query.get_league_key(season)))
# print(repr(yahoo_query.get_current_user()))
# print(repr(yahoo_query.get_user_games()))
# print(repr(yahoo_query.get_user_leagues_by_game_key(game_key)))
# print(repr(yahoo_query.get_user_teams()))
#print(repr(yahoo_query.get_league_info()))
# print(repr(yahoo_query.get_league_metadata()))
# print(repr(yahoo_query.get_league_settings()))
# print(repr(yahoo_query.get_league_standings()))
#print(repr(yahoo_query.get_league_teams()))
# print(repr(yahoo_query.get_league_players(player_count_limit=10, player_count_start=0)))
# print(repr(yahoo_query.get_league_draft_results()))
# print(repr(yahoo_query.get_league_transactions()))
# print(repr(yahoo_query.get_league_scoreboard_by_week(chosen_week)))
# print(repr(yahoo_query.get_league_matchups_by_week(chosen_week)))
#print(repr(yahoo_query.get_team_info(team_id)))
#print(repr(yahoo_query.get_team_metadata(team_id)))
# print(repr(yahoo_query.get_team_stats(team_id)))
# print(repr(yahoo_query.get_team_stats_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_standings(team_id)))
#print(repr(yahoo_query.get_team_roster_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_roster_player_info_by_week(team_id, chosen_week)))
# # print(repr(yahoo_query.get_team_roster_player_info_by_date(team_id, chosen_date)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_team_roster_player_stats(team_id)))
# print(repr(yahoo_query.get_team_roster_player_stats_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_draft_results(team_id)))
# print(repr(yahoo_query.get_team_matchups(team_id)))
# print(repr(yahoo_query.get_player_stats_for_season(player_key)))
# print(repr(yahoo_query.get_player_stats_for_season(player_key, limit_to_league_stats=False)))
# print(repr(yahoo_query.get_player_stats_by_week(player_key, chosen_week)))
# print(repr(yahoo_query.get_player_stats_by_week(player_key, chosen_week, limit_to_league_stats=False)))
# print(repr(yahoo_query.get_player_stats_by_date(player_key, chosen_date)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_player_stats_by_date(player_key, chosen_date, limit_to_league_stats=False)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_player_ownership(player_key)))
# print(repr(yahoo_query.get_player_percent_owned_by_week(player_key, chosen_week)))
# print(repr(yahoo_query.get_player_draft_analysis(player_key)))

logger = get_logger("yfpy.models", DEBUG)
