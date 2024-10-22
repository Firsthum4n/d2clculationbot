import requests
import json
from django.db import connection

from django.core.management.base import BaseCommand
from django.conf import settings


from main.models import Teams

class Command(BaseCommand):
    help = "Обновляет данные о коммандах из API"

    def handle(self, *args, **options):
        teams_request = requests.get("https://api.opendota.com/api/teams")
        teams_data = teams_request.json()
        with open('teams_data.json', 'w+') as js_file:
            json.dump(teams_data, js_file, indent=4)

            for team in teams_data:
                team_name = team['name']


                try:
                    team_instance = Teams.objects.get(id=team_name)
                except Teams.DoesNotExist:
                    print(f'команда {team_name} не найдена в базе данных')
                    continue



                name = team['name']
                tag = team['tag']


                team_instance.rating = team['rating']
                team_instance.wins = team['wins']
                team_instance.losses = team['losses']

            print("Данные о командах успешно обновлены.")


