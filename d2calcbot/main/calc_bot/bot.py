from main.db_update.heroes import create_or_update_heroes
from main.db_update.teams import create_or_update_teams
from main.models import *

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader


def encryption(radiant, dire):
    dataset = DotaDataset(radiant, dire)
    print(dataset)





"""функция создающий словарь со всеми именами и статами команды, игроков и героев"""
def encryption_level_1(team_pick):
    team_all_pick = {
        'team': [
            {
                'name': [],
                'stats': []
            }
        ],
        'players': [
            {
                'name': [],'stats': []
            },
            {
                'name': [], 'stats': []
            },
            {
                'name': [], 'stats': []
            },
            {
                'name': [], 'stats': []
            },
            {
                'name': [], 'stats': []
            },
        ],
        'heroes': [
            {
                'name': [], 'stats': []
            },
            {
                'name': [], 'stats': []
            },
            {
                'name': [], 'stats': []
            },
            {
                'name': [], 'stats': []
            },
            {
                'name': [], 'stats': []
            },
        ]
    }

    all_heroes = Heroes.objects.all()
    all_teams = Teams.objects.all().prefetch_related('players')

    for team in all_teams:
        if team_pick['team'] == team.name:
            team_players = team.get_players()
            team_all_pick['team'][0]['name'] = team.name
            team_all_pick['team'][0]['stats'] = [team.rating, team.wins, team.losses]
            for i in range(min(len(team_players), 5)):
                team_all_pick['players'][i]['name'] = [team_players[i].name if team_players else None]
                team_all_pick['players'][i]['stats'] = [team_players[i].games_played, team_players[i].wins if team_players else None]

    count = 0
    for h in team_pick['heroes']:
        for hero in all_heroes:
            if h == hero.name:
                team_all_pick['heroes'][count]['name'] = [hero.name]
                team_all_pick['heroes'][count]['stats'] = [hero.pro_pick, hero.pro_win, hero.pro_lose, hero.base_health, hero.base_health_regen,
                                                           hero.base_mana, hero.base_mana_regen, hero.base_armor, hero.base_mr,
                                                           hero.base_attack_min, hero.base_attack_max, hero.base_str, hero.base_agi,
                                                           hero.base_int, hero.str_gain, hero.agi_gain, hero.int_gain, hero.attack_range,
                                                           hero.projectile_speed, hero.attack_rate, hero.base_attack_time, hero.attack_point,
                                                           hero.move_speed, hero.day_vision, hero.night_vision]
                if count < 4:
                    count += 1

    return team_all_pick

"""функция создания словарей для embedding слоя"""
def ad_to_dict(team_pick):
    team_names = set()
    player_names = set()
    hero_names = set()

    for team in team_pick['team']:
        team_names.add(team['name'])

    for player in team_pick['players']:
        for name in player['name']:
            player_names.add(name)

    for hero in team_pick['heroes']:

        for name in hero['name']:
            hero_names.add(name)


    return team_names, player_names, hero_names


"""Функция создания embedding слоя"""
def embedding_create(team_pick):
    team_names, player_names, hero_names = ad_to_dict(team_pick)

    embedding_dim = 32  # Размерность векторов Embedding
    team_embedding = nn.Embedding(len(team_names), embedding_dim)
    player_embedding = nn.Embedding(len(player_names), embedding_dim)
    hero_embedding = nn.Embedding(len(hero_names), embedding_dim)

    return team_embedding, player_embedding, hero_embedding


"""функция Создание словарей для индексации"""
def create_dict_for_index(team_pick):
    team_names, player_names, hero_names = ad_to_dict(team_pick)

    team_to_ix = {name: i for i, name in enumerate(team_names)}
    player_to_ix = {name: i for i, name in enumerate(player_names)}
    hero_to_ix = {name: i for i, name in enumerate(hero_names)}

    return team_to_ix, player_to_ix, hero_to_ix


"""Функция для преобразования данных в тензоры"""
def transform_data(team_data, player_data, hero_data, team_pick):

    team_to_ix, player_to_ix, hero_to_ix = create_dict_for_index(team_pick)

    team_index = team_to_ix[team_data[0]['name']]
    player_indices = [player_to_ix[player['name'][0]] for player in player_data]
    hero_indices = [hero_to_ix[hero['name'][0]] for hero in hero_data]


    team_stats = torch.tensor(team_data[0]['stats'], dtype=torch.float32)
    player_stats = torch.tensor([player['stats'] for player in player_data], dtype=torch.float32)
    hero_stats = torch.tensor([hero['stats'] for hero in hero_data], dtype=torch.float32)

    return team_index, player_indices, hero_indices, team_stats, player_stats, hero_stats


class DotaDataset(Dataset):
    def __init__(self, radiant, dire):
        self.data = []
        radiant_data = encryption_level_1(radiant)
        dire_data = encryption_level_1(dire)
        self.data.append(radiant_data)
        self.data.append(dire_data)


    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

      radiant_team_data = self.data[0]
      dire_team_data = self.data[1]

      radiant_team_index, radiant_player_indices, radiant_hero_indices, radiant_team_stats, radiant_player_stats, radiant_hero_stats = transform_data(radiant_team_data['team'], radiant_team_data['players'], radiant_team_data['heroes'], radiant_team_data)
      dire_team_index, dire_player_indices, dire_hero_indices, dire_team_stats, dire_player_stats, dire_hero_stats = transform_data(dire_team_data['team'], dire_team_data['players'], dire_team_data['heroes'], dire_team_data)

      return (radiant_team_index, radiant_player_indices, radiant_hero_indices, radiant_team_stats, radiant_player_stats, radiant_hero_stats), \
              (dire_team_index, dire_player_indices, dire_hero_indices, dire_team_stats, dire_player_stats, dire_hero_stats)




