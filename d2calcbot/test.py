import requests
import json

players_request = requests.get(f"https://api.opendota.com/api/teams/{9498970}/players")
players_data = players_request.json()

with open('players.json', 'w+') as players_file:
    json.dump(players_data, players_file, indent=4)