import requests
import json
from main.models import *
from test import all_teams

TIER_1 = (
    "PARIVISION", "BetBoom Team", "Team Liquid", "Team Falcons", "Tundra Esports", "Cloud9",
    "Aurora.1xBet", "Team Spirit", "Gaimin Gladiators", "AVULUS", "Shopify Rebellion", "Nigma Galaxy",
    "HEROIC", "Yakult Brothers", "Gaozu", "BOOM Esports", "Natus Vincere", "OG",
    "MOUZ", "M80", "beastcoast"
    )

TIER_1_2 = ("Xtreme Gaming", "Looking for org", "Azure Ray", "nouns")

TIER_1_3 = ("Chimera", )

def create_or_update_teams():
    """"добавление или обновление команд"""
    teams_request = requests.get("https://api.opendota.com/api/teams")
    teams_data = teams_request.json()

    with open('main/jsf/teams.json', 'w+') as teams_file:
        json.dump(teams_data, teams_file, indent=4)

    try:
        for tm in range(len(teams_data)):
            team_id = teams_data[tm]['team_id']
            if teams_data[tm]['name'] in TIER_1_3:
                try:
                    team = Teams.objects.get(name=teams_data[tm]['name'])
                    team.rating = teams_data[tm]['rating']
                    team.wins = teams_data[tm]['wins']
                    team.losses = teams_data[tm]['losses']
                    team.save()

                except Teams.DoesNotExist:
                    team, created = Teams.objects.get_or_create(
                        name=teams_data[tm]['name'],
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
                                        team_member = Teams.objects.get(name=teams_data[tm]['name'])

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




def update_teams():
    teams_request = requests.get("https://api.opendota.com/api/teams")
    teams_data = teams_request.json()

    with open('main/jsf/teams.json', 'w+') as teams_file:
        json.dump(teams_data, teams_file, indent=4)

    all_team = Teams.objects.all()
    for tm in range(len(teams_data)):
        try:
            for teams in all_team:
                team_id = teams_data[tm]['team_id']
                if team_id == teams.team_id:
                    team = Teams.objects.get(name=teams_data[tm]['name'])
                    team.rating = teams_data[tm]['rating']
                    team.wins = teams_data[tm]['wins']
                    team.losses = teams_data[tm]['losses']
                    team.save()

        except Exception as e:
            print(e, team)





