import requests
import json
from django.db import connection
from django.utils.timezone import now
from django.utils.timezone import timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import Heroes




class Command(BaseCommand):
    help = "Обновляет данные о героях из API"

    def handle(self, *args, **options):
        hero_request = requests.get("https://api.opendota.com/api/heroStats")
        hero_data = hero_request.json()
        with open('main/jsf/hero_data_stats.json', 'w+') as js_file:
            json.dump(hero_data, js_file, indent=4)


        for hero in hero_data:
            hero_name = hero['localized_name']

            # Проверяем, есть ли герой в базе данных
            try:
                hero_instance = Heroes.objects.get(name=hero_name)
            except Heroes.DoesNotExist:
                print(f"Герой {hero_name} не найден в базе данных.")
                continue

            # Записываем данные из API в поля hero_instance
            hero_instance.pro_pick = hero['pro_pick']
            hero_instance.pro_win = hero['pro_win']
            hero_instance.pro_lose = hero['pro_pick'] - hero['pro_win']
            hero_instance.save()

        # Обновляем время последнего обновления
        settings.LAST_UPDATE_TIME = now()

        print("Данные о героях успешно обновлены.")


