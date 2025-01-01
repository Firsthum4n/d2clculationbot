from main.db_update.heroes import create_or_update_heroes
from main.db_update.teams import create_or_update_teams
from main.models import *

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader


def encryption(radiant, dire):

    radiant_all_pick = encryption_level_1(radiant)
    dire_all_pick = encryption_level_1(dire)

    radiant_tensor = dataset(radiant_all_pick)
    dire_tensor = dataset(dire_all_pick)

    # print('radiant: ', radiant_tensor)
    num_teams = 2
    num_players = 10
    num_heroes = 10
    embedding_dim = 32
    team_stats_dim = 3
    player_stats_dim = 2
    hero_stats_dim = 25

    model = DotaNetwork(num_teams, num_players, num_heroes, embedding_dim, team_stats_dim, player_stats_dim, hero_stats_dim)



    with torch.no_grad():
        output = model(radiant_tensor, dire_tensor)
        print(f"\nВероятность победы Radiant: {output.item()}")




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


def dataset(data):

    team_data = data
    team_index, player_indices, hero_indices, team_stats, player_stats, hero_stats = transform_data(team_data['team'], team_data['players'], team_data['heroes'], team_data)


    return team_index, player_indices, hero_indices, team_stats, player_stats, hero_stats




class DotaNetwork(nn.Module):
    def __init__(self, num_teams, num_players, num_heroes, embedding_dim, team_stats_dim, player_stats_dim, hero_stats_dim): # добавлено player_stats_dim и hero_stats_dim
        super().__init__()
        self.team_embedding = nn.Embedding(num_teams, embedding_dim)
        self.player_embedding = nn.Embedding(num_players, embedding_dim)
        self.hero_embedding = nn.Embedding(num_heroes, embedding_dim)
        input_size = embedding_dim + 2 * num_players * embedding_dim + team_stats_dim + num_players * (player_stats_dim + hero_stats_dim)
        self.fc1 = nn.Linear(input_size, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, radiant_data, dire_data):
        r_team_index, r_player_indices, r_hero_indices, r_team_stats, r_player_stats, r_hero_stats = radiant_data
        d_team_index, d_player_indices, d_hero_indices, d_team_stats, d_player_stats, d_hero_stats = dire_data

        r_team_index = torch.tensor([[r_team_index]])
        r_player_indices = torch.tensor([r_player_indices])
        r_hero_indices = torch.tensor([r_hero_indices])

        d_team_index = torch.tensor([[d_team_index]])
        d_player_indices = torch.tensor([d_player_indices])
        d_hero_indices = torch.tensor([d_hero_indices])



        r_team_emb = self.team_embedding(r_team_index).squeeze(0).flatten()
        r_player_embs = self.player_embedding(r_player_indices)
        r_hero_embs = self.hero_embedding(r_hero_indices)

        input_size = sum([r_team_emb.size()[0], r_player_embs.size()[0], r_hero_embs.size()[0], r_team_stats.size()[0],
                          r_player_stats.size()[0], r_hero_stats.size()[0]])

        print(input_size)



        r_x = torch.cat([r_team_emb, r_player_embs.flatten(), r_hero_embs.flatten(), r_team_stats.flatten(),
                         r_player_stats.flatten(), r_hero_stats.flatten()], dim=0)

        r_x = self.fc1(r_x)

        d_team_emb = self.team_embedding(d_team_index).squeeze(0).flatten()
        d_player_embs = self.player_embedding(d_player_indices)
        d_hero_embs = self.hero_embedding(d_hero_indices)


        d_x = torch.cat([d_team_emb, d_player_embs.flatten(), d_hero_embs.flatten(), d_team_stats.flatten(),
                         d_player_stats.flatten(), d_hero_stats.flatten()], dim=0)

        d_x = self.fc1(d_x)

        x = torch.cat([r_x, d_x], dim=0)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x







