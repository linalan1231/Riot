# !pip3 install riotwatcher
import requests
import pandas as pd
import numpy as np

# Setting up Api key and URL to establish connection
api_key  = "RGAPI-c3a7bab0-2e16-4ff7-92d1-58d667da76fb" # Key expires every 24 hours, please renew at https://developer.riotgames.com
tag = "NA1"
league_name ="SuSuN PaNdiE"
url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{league_name}/{tag}"

# Checking the response -> 400 bad, 401 authorized, 403 forbidden, 404 data not found, 405 method not found.
api_url = url + '?api_key=' + api_key
response = requests.get(api_url)
print(response)

# Printing player information and puuid
player_info = response.json()
print(player_info)
puuid = player_info["puuid"]

def get_match_history(numb_of_matches):
    headers = {"X-Riot-Token":api_key}  

    match_id_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={numb_of_matches}'
    response = requests.get(match_id_url, headers=headers)
    match_ids = response.json() 

    latest_match_history = []
    for i in match_ids:
        match_info_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{i}"
        match_info = requests.get(match_info_url, headers=headers)
        game_info = match_info.json()
        latest_match_history.append(game_info)

    return latest_match_history

# Creating a function that will collect the kills, deaths, assists, and kda of a player
def get_player_info(game_info, player_name):
    player_true = []
    for game in game_info:
            participants = game.get("info", {}).get("participants", [])
            for i in range(len(participants)): 
                if participants[i].get("riotIdGameName") == player_name:
                    player_true.append(participants[i].get("riotIdGameName"))
                    player_true.append(participants[i].get("kills"))
                    player_true.append(participants[i].get("deaths"))
                    player_true.append(participants[i].get("assists"))
                    player_true.append(participants[i].get("challenges", {}).get("kda"))
                
    return player_true

# Get match history and player info
game_history = get_match_history(20)
print(len(game_history))

player_info = get_player_info(game_history, "SuSuN PaNdiE")
print(player_info)

player_info = np.array(player_info).reshape(-1,5)
player_info
df = pd.DataFrame(player_info, columns =["player_name","kills","deaths","assists","KDA"])
df