import requests
import json

from .bot import encryption_level_1
from main.models import *

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

with open('esl_matches.json', 'w+') as esl_file:
    json.dump(esl_req_matches, esl_file, indent=4)







test_data_x = []
test_data_y = []

def matches_test():
    radiant_pick = {
       'team': "",
        'heroes': []
    }

    dire_pick = {
        'team': "",
        'heroes': []
    }


    all_teams = Teams.objects.all().prefetch_related('players')
    all_heroes = Heroes.objects.all()

    for match in esl_req_matches:

        count = 0

        match_id = match['match_id']
        radiant_team_id = match['radiant_team_id']
        dire_team_id = match['dire_team_id']

        match_info = requests.get(f'https://api.opendota.com/api/matches/{match_id}')
        req_match_info = match_info.json()
        with open('main/jsf/f_match.json', 'w+') as esl_match_file:
            json.dump(req_match_info, esl_match_file, indent=4)

        for team in all_teams:
            if radiant_team_id == team.team_id:
                radiant_pick['team'] = team.name

                for hero in all_heroes:
                    for pick in req_match_info['picks_bans']:
                        if pick['is_pick'] == True and pick['team'] == 0:

                            hero_id = pick['hero_id']
                            if hero_id == hero.hero_id:


                                radiant_pick['heroes'].append(hero.name)
                                count += 1

        if count == 5:
            test_data_x.append(radiant_pick)
            radiant_pick = {
                'team': "",
                'heroes': []
    }
            count = 0
            print(test_data_x)


                    # hero_id = hero_set(match_id, 0)
                    # if hero_id == hero.hero_id:
                    #     radiant_pick['heroes'].append(hero.name)
                    #
                    #     print(radiant_pick)


            # if dire_team_id == team.team_id:
            #     dire_pick['team'] = team.name
            #
            #     for hero in all_heroes:
            #         hero_id = hero_set(match_id, 1)
            #         if hero_id == hero.hero_id:
            #             dire_pick['heroes'].append(hero.name)
            #             print(dire_pick)
            #



def hero_set(match_id, team):
    match_info = requests.get(f'https://api.opendota.com/api/matches/{match_id}')
    req_match_info = match_info.json()
    with open('main/jsf/f_match.json', 'w+') as esl_match_file:
        json.dump(req_match_info, esl_match_file, indent=4)

        for pick in req_match_info['picks_bans']:
            if pick['is_pick'] == True and pick['team'] == team:
                hero_id = pick['hero_id']

                return hero_id
