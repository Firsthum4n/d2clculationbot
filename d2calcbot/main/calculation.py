from d2api.src.entities import all_heroes

from .models import *

import json
import requests




hero_request = requests.get("https://api.opendota.com/api/heroStats")
hero_data = hero_request.json()
with open('hero_data_stats.json', 'w+') as js_file:
    json.dump(hero_data, js_file, indent=4)


def f_dict_with_ids(lst):
    dict_with_id = {}
    all_heroes_1 = Heroes.objects.all()
    for i in lst:
        for hero in all_heroes_1:
            if i == hero.name:
                dict_with_id[hero.name] = hero.hero_id

    return dict_with_id

def mid_calc(first_dict_id, second_dict_id):
    all_heroes_1 = Heroes.objects.all()
    match_up_winrate = 0
    for hero_1, id_1 in first_dict_id.items():
        match_up_request = requests.get(f"https://api.opendota.com/api/heroes/{id_1}/matchups")
        match_up = match_up_request.json()
        for m in range(len(match_up)):
            for hero_2, id_2 in second_dict_id.items():
                if match_up[m]['hero_id'] == id_2:
                    loses = match_up[m]['games_played'] - match_up[m]['wins']
                    winrate = match_up[m]['wins'] - loses
                    match_up_winrate += winrate

    return match_up_winrate



def hero_import(hero_list):
    hero_dict = {}
    result = 0
    all_heroes = Heroes.objects.all()
    for hero in all_heroes:
        for i in hero_list:
            if i == hero.name:
                hero_dict[i] = {
                                'winrate':hero.pro_win - hero.pro_lose
                                }
                result += (hero.pro_win - hero.pro_lose)
    return result



def low_calculation(radiant, dire):
    radiant_dict_id = f_dict_with_ids(radiant)
    dire_dict_id = f_dict_with_ids(dire)

    radiant_winrate = mid_calc(radiant_dict_id, dire_dict_id)
    dire_winrate = mid_calc(dire_dict_id, radiant_dict_id)

    radiant_result = hero_import(radiant) + radiant_winrate
    dire_result = hero_import(dire) + dire_winrate

    if radiant_result > dire_result:
        return f'Победа Radiant, radiant:{radiant_result}, dire:{dire_result}'
    elif radiant_result < dire_result:
        return f'Победа Dire, dire:{dire_result}, radiant:{radiant_result},'
    else:
        return f'ничья, radiant:{radiant_result}, dire:{dire_result}'










