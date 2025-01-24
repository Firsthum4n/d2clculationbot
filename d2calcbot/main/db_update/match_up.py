import json
import requests
from main.models import *
import time


def hero_matchup():
    with open('main/jsf/hero_data_stats.json', 'r') as f:
            hero = json.load(f)

    request_count = 0
    start_time = time.time()

    for i in hero:
        if request_count >= 30 and time.time() - start_time < 60:
            sleep_time = 35
            print(f"Слишком много запросов. Ожидание {sleep_time:.2f} секунд...")
            time.sleep(sleep_time)
            request_count = 0
            start_time = time.time()

        try:
            match_up = requests.get(f"https://api.opendota.com/api/heroes/{i['id']}/matchups", timeout=10)
            match_up.raise_for_status()
            match_up_req = match_up.json()
            with open(f'main/calc_bot/matchupjson/{i["id"]}.json', 'w+') as f:
                json.dump(match_up_req, f, indent=4)
            request_count += 1
            print(f"Успешно получены данные для героя {i['id']}. Запросов в минуту: {request_count}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к OpenDota API для героя {i['id']}: {e}")

        time.sleep(0.1)


def teams_hero_matchup():
    al_t = Teams.objects.all()

    for i in al_t:
        teams_up = requests.get(f"https://api.opendota.com/api/teams/{i.team_id}/heroes")
        teams_up_req = teams_up.json()
        with open(f'main/calc_bot/matchupjsonteams/{i.team_id}.json', 'w+') as f:
            json.dump(teams_up_req , f, indent=4)

