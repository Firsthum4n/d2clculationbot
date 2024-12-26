import requests
import json
from .models import *


hero_request = requests.get("https://api.opendota.com/api/heroStats")
hero_data = hero_request.json()
with open('jsf/hero_data_stats.json', 'w+') as hero_file:
    json.dump(hero_data, hero_file, indent=4)



def update_teams_info():
    teams_request = requests.get("https://api.opendota.com/api/teams")
    teams_data = teams_request.json()

    with open('jsf/teams.json', 'w+') as teams_file:
        json.dump(teams_data, teams_file, indent=4)

    try:
        for i in range(len(teams_data)):
            print(teams_data[i]['team_id'])
            team, created = Teams.objects.update_or_create(
                id=teams_data[i]['team_id'],
                name=teams_data[i]['tag'],
                team_id=teams_data[i]['id'],
                raiting=teams_data[i]['raiting'],
                wins=teams_data[i]['wins'],
                losses=teams_data[i]['losses']

            )





    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return False
    # except Teams.DoesNotExist:
    #     print("Ошибка при доступе к модели Heroes")
    #     return False
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return False



update_teams_info()


# players_request = requests.get(f"https://api.opendota.com/api/teams/{team_id}/players")
# players_data = players_request.json()
#
# with open('main/jsf/players.json', 'w+') as js_file:
#     json.dump(players_data, js_file, indent=4)

