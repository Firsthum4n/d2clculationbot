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


    radiant_team_data = team_tensor(radiant_all_pick)
    dire_team_data = team_tensor(dire_all_pick)

    radiant_player_data = player_tensor(radiant_all_pick)
    dire_player_data = player_tensor(dire_all_pick)

    radiant_hero_data = hero_tensor(radiant_all_pick)
    dire_hero_data = hero_tensor(dire_all_pick)

    num_teams = 6
    num_players = 10
    num_heroes = 10
    embedding_dim = 32


    model = MainNetwork(num_teams, num_players, num_heroes, embedding_dim)

    with torch.no_grad():
        output = model(radiant_team_data, dire_team_data,
                       radiant_player_data, dire_player_data,
                       radiant_hero_data, dire_hero_data)
        print(f"\nВероятность победы Radiant: {output}")

    # print('radiant: ', radiant_tensor)

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
    (team_index, player_indices, hero_indices,
    team_stats, player_stats, hero_stats) = transform_data(team_data['team'],
                                                            team_data['players'],
                                                            team_data['heroes'],
                                                            team_data)
    return team_index, player_indices, hero_indices, team_stats, player_stats, hero_stats

def team_tensor(data):
    team_data = data
    (team_index, player_indices, hero_indices,
    team_stats, player_stats, hero_stats) = transform_data(team_data['team'],
                                                    team_data['players'],
                                                    team_data['heroes'],
                                                    team_data)
    return team_index, team_stats


def player_tensor(data):
    team_data = data
    (team_index, player_indices, hero_indices,
    team_stats, player_stats, hero_stats) = transform_data(team_data['team'],
                                                        team_data['players'],
                                                        team_data['heroes'],
                                                        team_data)
    return player_indices, player_stats


def hero_tensor(data):
    team_data = data
    (team_index, player_indices, hero_indices,
    team_stats, player_stats, hero_stats) = transform_data(team_data['team'],
                                                        team_data['players'],
                                                        team_data['heroes'],
                                                        team_data)
    return  hero_indices, hero_stats





class BranchTeam(nn.Module):
    def __init__(self, num_teams, embedding_dim):
        super().__init__()

        self.team_embedding = nn.Embedding(num_teams, embedding_dim)

        self.fc1 = nn.Linear(35, 75)
        self.fc2 = nn.Linear(150, 75)
        self.fc3 = nn.Linear(75, 1)

        self.sigmoid = nn.Sigmoid()


    def forward(self, radiant_team_data, dire_team_data):

        r_team_index, r_team_stats = radiant_team_data
        d_team_index, d_team_stats = dire_team_data

        r_team_index = torch.tensor([[r_team_index]])
        d_team_index = torch.tensor([[d_team_index]])

        r_team_emb = self.team_embedding(r_team_index)
        d_team_emb = self.team_embedding(d_team_index)

        r_team_stats = r_team_stats.unsqueeze(0).unsqueeze(1)
        d_team_stats = d_team_stats.unsqueeze(0).unsqueeze(1)

        r_team_block = torch.cat((r_team_emb, r_team_stats), dim=2)
        d_team_block = torch.cat((d_team_emb, d_team_stats), dim=2)

        r_x = self.fc1(r_team_block)
        d_x = self.fc1(d_team_block)

        x = torch.cat([r_x, d_x], dim=2)

        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x



class BranchPlayers(nn.Module):
    def __init__(self, num_players, embedding_dim):
        super().__init__()

        self.player_embedding = nn.Embedding(num_players, embedding_dim)

        self.fc1 = nn.Linear(34, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 1)

        self.sigmoid = nn.Sigmoid()

    def forward(self, radiant_player_data, dire_player_data):
        r_player_index, r_player_stats = radiant_player_data
        d_player_index, d_player_stats = dire_player_data

        r_player_index = torch.tensor([r_player_index])
        d_player_index = torch.tensor([d_player_index])

        r_player_emb = self.player_embedding(r_player_index)
        d_player_emb = self.player_embedding(d_player_index)

        r_player_stats = r_player_stats.unsqueeze(0)
        d_player_stats = d_player_stats.unsqueeze(0)


        r_player_block = torch.cat((r_player_emb, r_player_stats), dim=2)
        d_player_block = torch.cat((d_player_emb, d_player_stats), dim=2)

        r_x = self.fc1(r_player_block)
        d_x = self.fc1(d_player_block)

        x = torch.cat([r_x, d_x], dim=0)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x

class BranchHeroes(nn.Module):
    def __init__(self, num_heroes, embedding_dim):
        super().__init__()

        self.hero_embedding = nn.Embedding(num_heroes, embedding_dim)

        self.fc1 = nn.Linear(57, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 1)

        self.sigmoid = nn.Sigmoid()

    def forward(self, radiant_hero_data, dire_hero_data):
        r_hero_index, r_hero_stats = radiant_hero_data
        d_hero_index, d_hero_stats = dire_hero_data

        r_hero_index = torch.tensor([r_hero_index])
        d_hero_index = torch.tensor([d_hero_index])

        r_hero_emb = self.hero_embedding(r_hero_index)
        d_hero_emb = self.hero_embedding(d_hero_index)

        r_hero_stats = r_hero_stats.unsqueeze(0)
        d_hero_stats = d_hero_stats.unsqueeze(0)

        r_hero_block = torch.cat((r_hero_emb, r_hero_stats), dim=2)
        d_hero_block = torch.cat((d_hero_emb, d_hero_stats), dim=2)


        r_x = self.fc1(r_hero_block)
        d_x = self.fc1(d_hero_block)

        x = torch.cat([r_x, d_x], dim=0)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x



class MainNetwork(nn.Module):
    def __init__(self, num_teams, num_players, num_heroes, embedding_dim ):
        super().__init__()

        self.branch_t = BranchTeam(num_teams, embedding_dim)
        self.branch_p = BranchPlayers(num_players, embedding_dim)
        self.branch_h = BranchHeroes(num_heroes, embedding_dim)

        self.final_layer = nn.Linear(1, 1)

    def forward(self, radiant_team_data, dire_team_data, radiant_player_data, dire_player_data, radiant_hero_data, dire_hero_data):

        out_team = self.branch_t(radiant_team_data, dire_team_data)
        out_players = self.branch_p(radiant_player_data, dire_player_data)
        out_heroes = self.branch_h(radiant_hero_data, dire_hero_data)

        out_team = out_team.repeat(2,1,1)

        combined = torch.cat((out_team, out_players, out_heroes), dim=1)


        output = self.final_layer(combined)

        return output







