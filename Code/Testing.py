# !pip3 install riotwatcher
from riotwatcher import LolWatcher, ApiError
import requests

api_key  = "RGAPI-a738f7ff-0c04-479b-aec9-cb2fba09f77c" #key expires every 24 hours, please renew at https://developer.riotgames.com

headers = {"X-Riot-Token":api_key}

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

#getting match history base on puuid 
numb_of_matches = 20
match_id_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={numb_of_matches}'
match_ids = requests.get(match_id_url, headers=headers)
match_id = match_ids.json()
match_id

#getting the 20 match ID
match_ids1  = match_id[0]
match_info_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_ids1}"
match_info = requests.get(match_info_url, headers=headers)
match_info.json()


match_ids1
