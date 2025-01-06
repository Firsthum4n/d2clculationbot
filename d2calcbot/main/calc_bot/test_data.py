import requests
import json

from main.models import *

# test = requests.get('https://api.opendota.com/api/leagues')
# tst = test.json()
#
# with open('main/calc_bot/leagues.json', 'w+') as teams_file:
#     json.dump(tst, teams_file, indent=4)

with open('main/calc_bot/leagues.json', 'r') as f:
    tst = json.load(f)


# ESL = requests.get(f'https://api.opendota.com/api/leagues/{17509}/teams')
# esl_req = ESL.json()
#
# with open('main/calc_bot/esl_2024.json', 'w+') as teams_file:
#     json.dump(esl_req, teams_file, indent=4)

with open('main/calc_bot/esl_2024.json', 'r') as f:
    esl_req = json.load(f)


# esl_matches = requests.get(f'https://api.opendota.com/api/leagues/{17509}/matches')
# esl_req_matches = esl_matches.json()
#
# with open('main/calc_bot/esl_matches.json', 'w+') as esl_file:
#     json.dump(esl_req_matches, esl_file, indent=4)

with open('main/calc_bot/esl_matches.json', 'r') as f:
    esl_req_matches = json.load(f)



def matches_test():

    test_data_x = []
    test_data_y = []

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

    count2 = 1

    for match in esl_req_matches:

        count = 0

        match_id = match['match_id']
        radiant_team_id = match['radiant_team_id']
        dire_team_id = match['dire_team_id']


        if match["radiant_win"]:
            winner = 0
        if not match['radiant_win']:
            winner = 1


        # match_info = requests.get(f'https://api.opendota.com/api/matches/{match_id}')
        # req_match_info = match_info.json()
        # with open('main/calc_bot/f_match.json', 'w+') as esl_match_file:
        #     json.dump(req_match_info, esl_match_file, indent=4)

        with open('main/calc_bot/f_match.json', 'r') as f:
            req_match_info = json.load(f)



        for team in all_teams:
            if radiant_team_id == team.team_id:
                radiant_pick['team'] = team.name

                for hero in all_heroes:
                    for pick in req_match_info['picks_bans']:
                        if pick['is_pick'] == True and pick['team'] == 0:

                            hero_id = pick['hero_id']
                            if hero_id == hero.hero_id:

                                radiant_pick['heroes'].append(hero.name)

            if dire_team_id == team.team_id:
                dire_pick['team'] = team.name

                for hero in all_heroes:
                    for pick in req_match_info['picks_bans']:
                        if pick['is_pick'] == True and pick['team'] == 1:

                            hero_id = pick['hero_id']
                            if hero_id == hero.hero_id:

                                dire_pick['heroes'].append(hero.name)

                                count += 1

        if count == 5:
            test_data_x.append(
                {'game' :
                    [
                        {'radiant': radiant_pick},
                        {'dire': dire_pick},
                        {'winner': winner}
                    ]
                }
            )
            test_data_y.append(winner)

            test_file = test_data_x
            with open('main/calc_bot/test_data.json', 'w+') as test_data_file:
                json.dump(test_file, test_data_file, indent=4)

            radiant_pick = {
                'team': "",
                'heroes': []
            }

            dire_pick = {
                'team': "",
                'heroes': []
            }

            count2 += 1


    return test_data_x, test_data_y


