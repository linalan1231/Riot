# !pip3 install riotwatcher
from riotwatcher import LolWatcher, ApiError
import requests

api_key  = "RGAPI-c3a7bab0-2e16-4ff7-92d1-58d667da76fb" #key expires every 24 hours, please renew at https://developer.riotgames.com
tag = "NA2"
league_name ="Better team wins"
url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{league_name}/{tag}"

#checking the response
api_url = url + '?api_key=' + api_key
response = requests.get(api_url)  
print(response)

#printing player information
player_info = response.json()
print(player_info)

#getting the puuid
puuid = player_info["puuid"]

headers = {"X-Riot-Token":api_key}

total_match_ids = []
def get_match_id(numb_of_matches):
    # set numb_of_matches = match number
    numb_of_matches = numb_of_matches
    match_id_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={numb_of_matches}'
    match_ids = requests.get(match_id_url, headers=headers)
    match_id = match_ids.json() 
    total_match_ids.append(match_id)
    return total_match_ids
get_match_id(20)

def get_match_info(total_match_ids):
    match_ids  = match_id[0]
    match_ids
    match_info_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_ids}"
    match_info = requests.get(match_info_url, headers=headers)
    game_info = match_info.json()


#creating a function that will collect the kills, deaths, assists, and kda of a player
def get_player_info(player_name):
    player_true = []
    for i in range(10):
        player_info = game_info["info"]["participants"][i]["riotIdGameName"] == player_name
        if player_info:
            player_true.append(game_info["info"]["participants"][i]["riotIdGameName"])
            player_true.append(game_info["info"]["participants"][i]["kills"])
            player_true.append(game_info["info"]["participants"][i]["deaths"])
            player_true.append(game_info["info"]["participants"][i]["assists"])
            player_true.append(game_info["info"]["participants"][6]["challenges"]["kda"])
    return player_true



#getting the 1st match ID
#match_ids  = match_id[0]
#match_info_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_ids}"
#match_info = requests.get(match_info_url, headers=headers)
#game_info = match_info.json()
#return game_info