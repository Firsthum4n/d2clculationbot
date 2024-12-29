import requests
import json
from main.models import *




TIER_1 = (
    "PARIVISION", "BetBoom", "Liquid", "FLCN", "Tundra", "C9",
    "Aurora", "TSpirit", "GG", "Geek", "XG", "TALON", "AVULUS",
    "Heroic", "YB", "BOOM", "Apex", "SR", "OG", "NGX", "NAVI",
    "MOUZ", "VP", "L1", "1w", "Waska"
    )

def create_or_update_teams():
    """"добавление или обновление команд"""
    teams_request = requests.get("https://api.opendota.com/api/teams")
    teams_data = teams_request.json()

    with open('main/jsf/teams.json', 'w+') as teams_file:
        json.dump(teams_data, teams_file, indent=4)

    try:
        for tm in range(len(teams_data)):
            team_id = teams_data[tm]['team_id']
            if teams_data[tm]['tag'] in TIER_1:
                try:
                    team = Teams.objects.get(name=teams_data[tm]['tag'])
                    team.rating = teams_data[tm]['rating']
                    team.wins = teams_data[tm]['wins']
                    team.losses = teams_data[tm]['losses']
                    team.save()

                except Teams.DoesNotExist:
                    team, created = Teams.objects.get_or_create(
                        name=teams_data[tm]['tag'],
                        team_id=teams_data[tm]['team_id'],
                        rating=teams_data[tm]['rating'],
                        wins=teams_data[tm]['wins'],
                        losses=teams_data[tm]['losses'],
                    )
                    team.save()
                    if created:

                        players_request = requests.get(f"https://api.opendota.com/api/teams/{team_id}/players")
                        players_data = players_request.json()

                        with open('main/jsf/players.json', 'w+') as players_file:
                            json.dump(players_data, players_file, indent=4)

                            for plyr in range(len(players_data)):
                                if players_data[plyr]['name'] is not None:
                                    try:

                                        is_current_team_member = players_data[plyr]['is_current_team_member']
                                        team_member = Teams.objects.get(name=teams_data[tm]['tag'])

                                        player = Players.objects.get(name=players_data[plyr]['name'])
                                        player.games_played = players_data[plyr]['games_played']
                                        player.wins = players_data[plyr]['wins']
                                        if is_current_team_member:
                                            player.team = team_member
                                        player.save()


                                    except Players.DoesNotExist:
                                        player, created = Players.objects.get_or_create(
                                            name=players_data[plyr]['name'],
                                            games_played=players_data[plyr]['games_played'],
                                            wins=players_data[plyr]['wins'],
                                        )
                                        if created and is_current_team_member:
                                                player.team = team_member
                                        player.save()

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return False
    except Teams.DoesNotExist:
        print("Ошибка при доступе к модели Teams")
        return False
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return False








