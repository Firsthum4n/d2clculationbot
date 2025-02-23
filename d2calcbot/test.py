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

league_ids = [16632, 16846, 16935, 17119, 17126, 17272, 17414, 17509, ]
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
# match_up = requests.get(f"https://api.opendota.com/api/heroes/{106}/matchups")
# match_up_req = match_up.json()
#
#
# with open('match_up.json', 'w+') as f:
#     json.dump(match_up_req , f, indent=4)
#
# print(len(match_up_req))
#############################################################################################





# with open('main/jsf/hero_data_stats.json', 'r') as f:
#     hero = json.load(f)
#
# for i in hero:
#     match_up = requests.get(f"https://api.opendota.com/api/heroes/{i["id"]}/matchups")
#     match_up_req = match_up.json()
#     with open(f'main/calc_bot/matchupjson/{i["id"]}.json', 'w+') as f:
#         json.dump(match_up_req , f, indent=4)
#
#
#


#############################################################################################





# with open('main/jsf/hero_data_stats.json', 'r') as f:
#     hero = json.load(f)
#
# for i in hero:
#     match_up = requests.get(f"https://api.opendota.com/api/heroes/{i["id"]}/matchups")
#     match_up_req = match_up.json()
#     with open(f'main/calc_bot/matchupjson/{i["id"]}.json', 'w+') as f:
#         json.dump(match_up_req , f, indent=4)
#
# teams_up = requests.get(f"https://api.opendota.com/api/teams/{17414}/heroes")


####################################################################################













# ids = [109, 110, 111, 112, 113, 114, 119, 120, 121, 122, 123, 126, 128, 129]
# for i in ids:
#     match_up = requests.get(f"https://api.opendota.com/api/heroes/{i}/matchups")
#     match_up_req = match_up.json()
#     with open(f'main/calc_bot/matchupjson/{i}.json', 'w+') as f:
#         json.dump(match_up_req , f, indent=4)
#####################################################
############################################
# import time
# league_id = [17628, 17674, 17669, 17670,  17671, 17672, 17673, 17629, 17588, 17767, 17768, 17769, 17770, 17771, 17772, 17775, 17776, 17778, 17765]
#
#
# for league_id in league_id:
#     esl_matches = requests.get(f'https://api.opendota.com/api/leagues/{league_id}/matches')
#     if esl_matches.status_code == 200:
#         esl_req_matches = esl_matches.json()
#         all_matches.extend(esl_req_matches)
#     else:
#         time.sleep(60)
#         print(f"Ошибка при запросе к лиге {league_id}: {esl_matches.status_code}")
#
# with open('main/calc_bot/matches3.json', 'w+') as esl_file:
#     json.dump(all_matches, esl_file, indent=4)
####################################################################
#########################################################
# teams_request = requests.get("https://api.opendota.com/api/teams")
# teams_data = teams_request.json()
#
# with open('main/jsf/teams.json', 'w+') as teams_file:
#     json.dump(teams_data, teams_file, indent=4)

######################################################################
####################################################################
##################################################################
# import requests
# import json
# import time
# def match_up_h():
#     with open('main/jsf/hero_data_stats.json', 'r') as f:
#         hero = json.load(f)
#
#     request_count = 0
#     start_time = time.time()
#
#     for i in hero:
#         if request_count >= 30 and time.time() - start_time < 60:
#             sleep_time = 60 - (time.time() - start_time)
#             print(f"Слишком много запросов. Ожидание {sleep_time:.2f} секунд...")
#             time.sleep(sleep_time)
#             request_count = 0
#             start_time = time.time()
#
#         try:
#             match_up = requests.get(f"https://api.opendota.com/api/heroes/{i['id']}/matchups", timeout=10)
#             match_up.raise_for_status() # Проверяем на HTTP ошибки
#             match_up_req = match_up.json()
#             with open(f'main/calc_bot/matchupjson/{i["id"]}.json', 'w+') as f:
#                 json.dump(match_up_req, f, indent=4)
#             request_count += 1
#             print(f"Успешно получены данные для героя {i['id']}. Запросов в минуту: {request_count}")
#
#         except requests.exceptions.RequestException as e:
#             print(f"Ошибка при запросе к OpenDota API для героя {i['id']}: {e}")
#
#         time.sleep(0.1)
#
# match_up_h()


##########################################################################################################
#
# p = requests.get(f"https://api.opendota.com/api/schema")
# p_req = p.json()
#
#
# with open('p.json', 'w+') as f:
#     json.dump(p_req , f, indent=4)

#
# teams_request = requests.get("https://api.opendota.com/api/teams")
# teams_data = teams_request.json()
#
# with open('main/jsf/teams.json', 'w+') as teams_file:
#     json.dump(teams_data, teams_file, indent=4)

################################################################################


# ESL = requests.get(f'https://api.opendota.com/api/leagues/{17414}/teams')
# esl_req = ESL.json()
#
# with open('main/calc_bot/esl_2024.json', 'w+') as teams_file:
#     json.dump(esl_req, teams_file, indent=4)



# with open('main/calc_bot/esl_2024.json', 'r') as f:
#     esl_req = json.load(f)


# esl_matches = requests.get(f'https://api.opendota.com/api/leagues/{17414}/matches')
# esl_req_matches = esl_matches.json()
#
# with open('main/calc_bot/esl_matches.json', 'w+') as esl_file:
#     json.dump(esl_req_matches, esl_file, indent=4)

# test = requests.get('https://api.opendota.com/api/leagues')
# tst = test.json()
#
# with open('main/calc_bot/leagues.json', 'w+') as teams_file:
#     json.dump(tst, teams_file, indent=4)


# test = requests.get(f'https://api.opendota.com/api/teams/{3922738}/heroes')
# tst = test.json()
#
# with open('main/calc_bot/teams_heroes.json', 'w+') as teams_file:
#     json.dump(tst, teams_file, indent=4)
