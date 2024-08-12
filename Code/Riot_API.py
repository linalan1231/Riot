# !pip3 install riotwatcher
import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Setting up Api key and URL to establish connection
api_file = open("/Users/alanlin/Desktop/API_Key/API_KEY.txt","r") #opening API key on local 
api_key = api_file.read()
tag = "Na2"
league_name ="Better Team wins"
url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{league_name}/{tag}"

# Checking the response -> 400 bad, 401 authorized, 403 forbidden, 404 data not found, 405 method not found.
api_url = url + '?api_key=' + api_key
response = requests.get(api_url)
print(response)

# Printing player information and puuid
player_info = response.json()
print(player_info)
puuid = player_info["puuid"]
puuid #unique identifier of a specific player

def get_match_history(numb_of_matches):
    headers = {"X-Riot-Token":api_key}  

    match_id_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={numb_of_matches}' #getting the matchID
    response = requests.get(match_id_url, headers=headers)
    match_ids = response.json() 

    latest_match_history = []
    for i in match_ids:
        match_info_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{i}" #getting match information 
        match_info = requests.get(match_info_url, headers=headers)
        game_info = match_info.json()
        latest_match_history.append(game_info)

    return latest_match_history

# Creating a function that will collect the kills, deaths, assists, kda, and other player stats
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
                    player_true.append(participants[i].get("goldEarned"))
                    player_true.append(participants[i].get("goldSpent"))
                    player_true.append(participants[i].get("totalDamageDealtToChampions"))
                    player_true.append(participants[i].get("totalDamageTaken"))
                    player_true.append(participants[i].get("win"))
                    player_true.append(game.get("info", {}).get("gameCreation"))
    return player_true

# Get match history and player info
game_history = get_match_history(100) #100 maximum amount
print(len(game_history)) #checking the number of games

player_info = get_player_info(game_history, "Better Team wins")
print(player_info)

player_info = np.array(player_info).reshape(-1,11) #reshaping the list -> 10 columns, and x amount of rows 
player_stats = pd.DataFrame(player_info, columns =["player_name","kills","deaths","assists","KDA","gold_Earned","gold_Spend","Total_Damage_dealt","Damage_Taken","status","Date"])
player_stats["status"] = player_stats["status"].replace({"True":"Win", "False":"Lose"}) #Changing True to win and False to Lose
player_stats["Date"] = player_stats["Date"].apply(lambda x: datetime.fromtimestamp(float(x) / 1000).strftime('%m%d%Y')) # converting gamecreation value to MM/DD/YYYY
player_stats.to_csv("player_stats.csv", index = False)

#Basic Visualization to test -> then import into tableau for analysis 
# Bar - Wins vs Lost
status_counts = dict(player_stats["status"].value_counts()) 
status_df = pd.DataFrame(list(status_counts.items()), columns=['status', 'counts'])
sns.barplot(x='status', y='counts', data = status_df)
plt.title("Wins Vs Losses")
plt.xlabel("Status")
plt.ylabel("Counts")
plt.show() # -> more loses than wins 

