from ctypes.wintypes import HANDLE

from main.models import *
import json
import requests
from django.db import connection
import os
from django.core.files.uploadedfile import SimpleUploadedFile


def create_or_update_heroes():
    """"добавление или обновление героев"""
    hero_request = requests.get("https://api.opendota.com/api/heroStats")
    hero_data = hero_request.json()

    with open('main/jsf/hero_data_stats.json', 'w+') as hero_file:
        json.dump(hero_data, hero_file, indent=4)

    try:
        for hr in range(len(hero_data)):
            try:
                hero = Heroes.objects.get(name=hero_data[hr]['localized_name'], hero_id=hero_data[hr]['id'])
                hero.pro_pick = handle_none(hero_data[hr]['pro_pick'])
                hero.pro_win = handle_none(hero_data[hr]['pro_win'])
                hero.pro_lose = handle_none(hero_data[hr]['pro_pick'] - hero_data[hr]['pro_win'])
                hero.base_health = handle_none(hero_data[hr]['base_health'])
                hero.base_health_regen = handle_none(hero_data[hr]['base_health_regen'])
                hero.base_mana = handle_none(hero_data[hr]['base_mana'])
                hero.base_mana_regen = handle_none(hero_data[hr]['base_mana_regen'])
                hero.base_armor = handle_none(hero_data[hr]['base_armor'])
                hero.base_mr = handle_none(hero_data[hr]['base_mr'])
                hero.base_attack_min = handle_none(hero_data[hr]['base_attack_min'])
                hero.base_attack_max = handle_none(hero_data[hr]['base_attack_max'])
                hero.base_str = handle_none(hero_data[hr]['base_str'])
                hero.base_agi = handle_none(hero_data[hr]['base_agi'])
                hero.base_int = handle_none(hero_data[hr]['base_int'])
                hero.str_gain = handle_none(hero_data[hr]['str_gain'])
                hero.agi_gain = handle_none(hero_data[hr]['agi_gain'])
                hero.int_gain = handle_none(hero_data[hr]['int_gain'])
                hero.attack_range = handle_none(hero_data[hr]['attack_range'])
                hero.projectile_speed = handle_none(hero_data[hr]['projectile_speed'])
                hero.attack_rate = handle_none(hero_data[hr]['attack_rate'])
                hero.base_attack_time = handle_none(hero_data[hr]['base_attack_time'])
                hero.attack_point = handle_none(hero_data[hr]['attack_point'])
                hero.move_speed = handle_none(hero_data[hr]['move_speed'])
                hero.day_vision = handle_none(hero_data[hr]['day_vision'])
                hero.night_vision = handle_none(hero_data[hr]['night_vision'])
                hero.save()
            except Heroes.DoesNotExist:

                response = requests.get(f'https://cdn.cloudflare.steamstatic.com/{hero_data[hr]["img"]}')
                with open(f'main/static/main/images/heroes/{hero_data[hr]["localized_name"]}.png', 'wb') as f:
                    f.write(response.content)

                hero_name = hero_data[hr]['localized_name']
                icon_path = f'main/static/main/images/heroes/{hero_name}.png'

                if os.path.exists(icon_path):
                    with open(icon_path, 'rb') as f:
                        icon = f.read()

                        icon_file = SimpleUploadedFile(
                            f"{hero_name}.png",
                            icon,
                            content_type='image/png'
                        )


                hero, created = Heroes.objects.get_or_create(
                    icon=icon_file,
                    name=hero_data[hr]['localized_name'],
                    hero_id=hero_data[hr]['id'],
                    pro_pick=hero_data[hr]['pro_pick'],
                    pro_win=hero_data[hr]['pro_win'],
                    pro_lose=hero_data[hr]['pro_pick'] - hero_data[hr]['pro_win'],
                    base_health=hero_data[hr]['base_health'],
                    base_health_regen=hero_data[hr]['base_health_regen'],
                    base_mana=hero_data[hr]['base_mana'],
                    base_mana_regen=hero_data[hr]['base_mana_regen'],
                    base_armor=hero_data[hr]['base_armor'],
                    base_mr=hero_data[hr]['base_mr'],
                    base_attack_min = hero_data[hr]['base_attack_min'],
                    base_attack_max = hero_data[hr]['base_attack_max'],
                    base_str = hero_data[hr]['base_str'],
                    base_agi = hero_data[hr]['base_agi'],
                    base_int = hero_data[hr]['base_int'],
                    str_gain = hero_data[hr]['str_gain'],
                    agi_gain = hero_data[hr]['agi_gain'],
                    int_gain = hero_data[hr]['int_gain'],
                    attack_range = hero_data[hr]['attack_range'],
                    projectile_speed = hero_data[hr]['projectile_speed'],
                    attack_rate = hero_data[hr]['attack_rate'],
                    base_attack_time = hero_data[hr]['base_attack_time'],
                    attack_point = hero_data[hr]['attack_point'],
                    move_speed = hero_data[hr]['move_speed'],
                    day_vision = hero_data[hr]['day_vision'],
                    night_vision = hero_data[hr]['night_vision']
                )
                hero.save()

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return False
    except Teams.DoesNotExist:
        print("Ошибка при доступе к модели Heroes")
        return False
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return False


"""если значение равно None меняется на 0"""
def handle_none(value):
    return value if value is not None else 0


"""функция удаления всех записей и обнуления id"""
def del_all_heroes_and_ids():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM main_heroes")
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'main_heroes'")



