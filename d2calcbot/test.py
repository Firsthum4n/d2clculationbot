import requests
import json

import requests
import json


# test = requests.get('https://api.opendota.com/api/leagues')
# tst = test.json()
#
# with open('main/calc_bot/leagues.json', 'w+') as teams_file:
#     json.dump(tst, teams_file, indent=4)

# with open('main/calc_bot/leagues.json', 'r') as f:
#     tst = json.load(f)

import requests
import json

league_ids = [17509, 17414]
all_matches = []

all_teams = []

# for league_id in league_ids:
#     ESL = requests.get(f'https://api.opendota.com/api/leagues/{league_id}/teams')
#     if ESL.status_code == 200:
#         esl_req = ESL.json()
#         all_teams.extend(esl_req)
#     else:
#         print(f"Ошибка при запросе к лиге {league_id}: {ESL.status_code}")
#
#
# with open('main/calc_bot/esl_2024.json', 'w+') as teams_file:
#     json.dump(all_teams, teams_file, indent=4)
#
# print("Данные успешно записаны в esl_2024.json")

##########################################################
# with open('main/calc_bot/esl_2024.json', 'r') as f:
#     esl_req = json.load(f)
#########################################################
# for league_id in league_ids:
#     esl_matches = requests.get(f'https://api.opendota.com/api/leagues/{league_id}/matches')
#     if esl_matches.status_code == 200:
#         esl_req_matches = esl_matches.json()
#         all_matches.extend(esl_req_matches)
#     else:
#         print(f"Ошибка при запросе к лиге {league_id}: {esl_matches.status_code}")
#
# with open('main/calc_bot/esl_matches.json', 'w+') as esl_file:
#     json.dump(all_matches, esl_file, indent=4)

#########################################################
# with open('main/calc_bot/esl_matches.json', 'r') as f:
#     esl_req_matches = json.load(f)
