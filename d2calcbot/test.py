import requests
import json


# test = requests.get('https://api.opendota.com/api/leagues')
# tst = test.json()
#
# with open('main/calc_bot/leagues.json', 'w+') as teams_file:
#     json.dump(tst, teams_file, indent=4)

# with open('main/calc_bot/leagues.json', 'r') as f:
#     tst = json.load(f)
# ESL = requests.get(f'https://api.opendota.com/api/leagues/{16935}/teams')
# esl_req = ESL.json()
#
# with open('main/calc_bot/esl_2024.json', 'w+') as teams_file:
#     json.dump(esl_req, teams_file, indent=4)

league_ids = [16632, 16846, 16935, 17119, 17126, 17272, 17414, 17509]
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
# with open('main/calc_bot/matches.json', 'w+') as esl_file:
#     json.dump(all_matches, esl_file, indent=4)

#########################################################
# with open('main/calc_bot/esl_matches.json', 'r') as f:
#     esl_req_matches = json.load(f)

#
# hero_request = requests.get("https://api.opendota.com/api/heroStats")
# hero_data = hero_request.json()
#
# with open('hero_data_stats.json', 'w+') as hero_file:
#     json.dump(hero_data, hero_file, indent=4)

###############################################################################
match_up = requests.get(f"https://api.opendota.com/api/heroes/{1}/matchups")
match_up_req = match_up.json()


with open('match_up.json', 'w+') as f:
    json.dump(match_up_req , f, indent=4)

