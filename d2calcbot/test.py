import requests
import json

players_request = requests.get(f"https://api.opendota.com/api/teams/{7732977}/players")
players_data = players_request.json()

with open('players.json', 'w+') as players_file:
    json.dump(players_data, players_file, indent=4)



request = requests.get(f"https://api.opendota.com/api/proPlayers")
requestd = request.json()
with open('pl.json', 'w+') as file:
    json.dump(requestd, file, indent=4)