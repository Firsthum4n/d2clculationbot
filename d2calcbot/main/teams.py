import requests
import json
from .models import *




TIER_1 = (
    "PARIVISION", "BetBoom", "Liquid", "FLCN", "Tundra", "C9",
    "Aurora", "TSpirit", "GG", "Geek", "XG", "TALON", "AVULUS",
    "Heroic", "YB", "BOOM", "Apex", "SR", "OG", "NGX", "NAVI",
    "MOUZ", "VP", "L1", "1w", "Waska"
    )

def update_teams_info():

    teams_request = requests.get("https://api.opendota.com/api/teams")
    teams_data = teams_request.json()

    with open('main/jsf/teams.json', 'w+') as teams_file:
        json.dump(teams_data, teams_file, indent=4)

    try:
        for i in range(len(teams_data)):
            team_id = teams_data[i]['team_id']
            if teams_data[i]['tag'] in TIER_1:
                print(teams_data[i]['tag'])
                try:
                    team = Teams.objects.get(name=teams_data[i]['tag'])
                    team.rating = teams_data[i]['rating']
                    team.wins = teams_data[i]['wins']
                    team.losses = teams_data[i]['losses']
                    team.save()

                except Teams.DoesNotExist:
                    team, created = Teams.objects.get_or_create(
                        name=teams_data[i]['tag'],
                        team_id=teams_data[i]['team_id'],
                        rating=teams_data[i]['rating'],
                        wins=teams_data[i]['wins'],
                        losses=teams_data[i]['losses'],
                    )
                    team.save()
                    if created:

                        players_request = requests.get(f"https://api.opendota.com/api/teams/{team_id}/players")
                        players_data = players_request.json()

                        with open('main/jsf/players.json', 'w+') as players_file:
                            json.dump(players_data, players_file, indent=4)

                            for p in range(len(players_data)):
                                if players_data[p]['name'] is not None:
                                    try:

                                        is_current_team_member = players_data[p]['is_current_team_member']
                                        team_member = Teams.objects.get(name=teams_data[i]['tag'])

                                        player = Players.objects.get(name=players_data[p]['name'])
                                        player.games_played = players_data[p]['games_played']
                                        player.wins = players_data[p]['wins']
                                        if is_current_team_member:
                                            player.team = team_member
                                        player.save()


                                    except Players.DoesNotExist:
                                        player, created = Players.objects.get_or_create(
                                            name=players_data[p]['name'],
                                            games_played=players_data[p]['games_played'],
                                            wins=players_data[p]['wins'],
                                        )
                                        if created and is_current_team_member:
                                                player.team = team_member
                                        player.save()

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return False
    except Teams.DoesNotExist:
        print("Ошибка при доступе к модели Heroes")
        return False
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return False








