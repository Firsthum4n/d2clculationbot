import requests
import json

test = requests.get('https://api.opendota.com/api/leagues')
tst = test.json()

with open('leagues.json', 'w+') as teams_file:
    json.dump(tst, teams_file, indent=4)


ESL = requests.get(f'https://api.opendota.com/api/leagues/{17509}/teams')
esl_req = ESL.json()

with open('esl_2024.json', 'w+') as teams_file:
    json.dump(esl_req, teams_file, indent=4)


esl_matches = requests.get(f'https://api.opendota.com/api/leagues/{17509}/matches')
esl_req_matches = esl_matches.json()

with open('esl_matches.json', 'w+') as teams_file:
    json.dump(esl_req_matches, teams_file, indent=4)



esl_match_info = requests.get(f'https://api.opendota.com/api/matches/{8082925992}')
esl_req_match_info = esl_match_info.json()
with open('esl_match_info.json', 'w+') as esl_match_file:
    json.dump(esl_req_match_info, esl_match_file, indent=4)
    for pick in esl_req_match_info['picks_bans']:
        if pick['is_pick']:
            print(pick['hero_id'])
