import requests
import json


# hero_request = requests.get("https://api.opendota.com/api/heroStats")
# hero_data = hero_request.json()
# with open('jsf/hero_data_stats.json', 'w+') as hero_file:
#     json.dump(hero_data, hero_file, indent=4)


players_request = requests.get(f"https://api.opendota.com/api/teams/9303383/players")
players_data = players_request.json()

with open('BB.json', 'w+') as players_file:
    json.dump(players_data, players_file, indent=4)