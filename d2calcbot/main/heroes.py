from .models import *
import json
import requests
from django.db import connection
import os
from django.core.files.uploadedfile import SimpleUploadedFile


hero_request = requests.get("https://api.opendota.com/api/heroStats")
hero_data = hero_request.json()
with open('main/jsf/hero_data_stats.json', 'w+') as js_file:
    json.dump(hero_data, js_file, indent=4)


"""функция для добавляения героев и иконок героев"""
def hero_mod():
    for j in range(len(hero_data)):
        response = requests.get(f'https://cdn.cloudflare.steamstatic.com/{hero_data[j]["img"]}')
        with open(f'main/static/main/images/heroes/{hero_data[j]["localized_name"]}.png', 'wb') as f:
            f.write(response.content)

        hero_name = hero_data[j]['localized_name']
        icon_path = f'main/static/main/images/heroes/{hero_name}.png'

        if os.path.exists(icon_path):
            with open(icon_path, 'rb') as f:
                icon = f.read()

                icon_file = SimpleUploadedFile(
                    f"{hero_name}.png",
                    icon,
                    content_type='image/png'
                )

                Heroes.objects.create(name=hero_name, icon=icon_file)
        else:
            print(f"Изображение для {hero_name} не найдено.")



"""функция удаления всех записей и обнуления id"""
def del_all_heroes_and_ids():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM main_heroes")
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'main_heroes'")


def id_import():
    all_heroes = Heroes.objects.all()
    for i in range(len(hero_data)):
        hero_name = hero_data[i]['localized_name']
        for hero in all_heroes:
            if hero.name == hero_name:
                hero.hero_id = hero_data[i]['id']
                hero.save()