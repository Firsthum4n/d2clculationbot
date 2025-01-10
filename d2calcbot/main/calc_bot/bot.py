from sympy.codegen.ast import float32

from main.db_update.heroes import create_or_update_heroes
from main.db_update.teams import create_or_update_teams
from .test_data import matches_test

from main.models import *

import torch
import torch.nn as nn

import torch.optim as optim
import torch.nn.functional as F

from torch.utils.data import Dataset, DataLoader, random_split

import os
import json



def encryption(radiant, dire):
    radiant_team_data = dataset(radiant)
    dire_team_data = dataset(dire)


    model = MainNetwork()
    model.load_state_dict(torch.load('main/calc_bot/dota_model.pth'))

    model.eval()
    with torch.no_grad():
        output = model(radiant_team_data,dire_team_data)
        if output.item() < 0.5:
            print(f'победа radiant {output.item()}')
        elif output.item() > 0.5:
            print(f'победа dire {output.item()}')



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

    embedding_dim = 32
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
    num_teams = 6
    num_players = 10
    num_heroes = 10
    embedding_dim = 32

    team_embedding = nn.Embedding(num_teams, embedding_dim)
    player_embedding = nn.Embedding(num_players, embedding_dim)
    hero_embedding = nn.Embedding(num_heroes, embedding_dim)

    team_data = encryption_level_1(data)
    (team_index, player_indices, hero_indices,
    team_stats, player_stats, hero_stats) = transform_data(team_data['team'],
                                                            team_data['players'],
                                                            team_data['heroes'],
                                                            team_data)

    team_index = torch.tensor([team_index])
    team_emb = team_embedding(team_index)
    team_stats = team_stats.unsqueeze(0)

    player_indices = torch.tensor(player_indices)
    player_emb = player_embedding(player_indices)

    hero_indices = torch.tensor(hero_indices)
    hero_emb = hero_embedding(hero_indices)

    team_block = torch.cat((team_emb, team_stats), dim=1)
    player_block = torch.cat((player_emb, player_stats), dim=1)
    hero_block = torch.cat((hero_emb, hero_stats), dim=1)

    return team_block, player_block, hero_block


class DotaDataset(Dataset):
    def __init__(self, data, team, index):
        self.data = data
        self.team = team
        self.index = index

        num_teams = 6
        num_players = 10
        num_heroes = 10
        embedding_dim = 32

        self.team_embedding = nn.Embedding(num_teams, embedding_dim)
        self.player_embedding = nn.Embedding(num_players, embedding_dim)
        self.hero_embedding = nn.Embedding(num_heroes, embedding_dim)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_for_encryption = self.data[idx]['game'][self.index][self.team]
        team_data = encryption_level_1(data_for_encryption)



        (team_index, player_indices, hero_indices,
        team_stats, player_stats, hero_stats) = transform_data(team_data['team'],
                                                                team_data['players'],
                                                                team_data['heroes'],
                                                                team_data)


        team_index = torch.tensor([team_index])
        team_emb = self.team_embedding(team_index)
        team_stats = team_stats.unsqueeze(0)

        player_indices = torch.tensor(player_indices)
        player_emb = self.player_embedding(player_indices)

        hero_indices = torch.tensor(hero_indices)
        hero_emb = self.hero_embedding(hero_indices)

        team_block = torch.cat((team_emb, team_stats), dim=1)
        player_block = torch.cat((player_emb, player_stats), dim=1)
        hero_block = torch.cat((hero_emb, hero_stats), dim=1)


        return team_block, player_block, hero_block









class BranchTeam(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()

        self.fc1 = nn.Linear(35, 70)
        self.fc2 = nn.Linear(70, 70)
        self.fc3 = nn.Linear(70, 70)
        self.fc4 = nn.Linear(70, 35)
        self.fc5 = nn.Linear(35,35)

        self.sigmoid = nn.Sigmoid()


    def forward(self, radiant_team_data, dire_team_data):
        r_team_block, r_player_block, r_hero_block = radiant_team_data
        d_team_block, d_player_block, d_hero_block = dire_team_data

        r_x = self.fc1(r_team_block)
        d_x = self.fc1(d_team_block)

        x = torch.cat([r_x, d_x], dim=0)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.fc4(x)
        x = self.fc5(x)

        x = self.sigmoid(x)

        return x



class BranchPlayers(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()

        self.fc1 = nn.Linear(34, 170)
        self.fc2 = nn.Linear(170, 170)
        self.fc3 = nn.Linear(170, 85)
        self.fc4 = nn.Linear(85, 40)
        self.fc5 = nn.Linear(40,40)



        self.sigmoid = nn.Sigmoid()

    def forward(self, radiant_team_data, dire_team_data):
        r_team_block, r_player_block, r_hero_block = radiant_team_data
        d_team_block, d_player_block, d_hero_block = dire_team_data

        r_x = self.fc1(r_player_block)
        d_x = self.fc1(d_player_block)


        x = torch.cat([r_x, d_x], dim=0)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.fc4(x)
        x = self.fc5(x)


        self.sigmoid = nn.Sigmoid()

        return x

class BranchHeroes(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()
        self.leaky_relu2 = nn.LeakyReLU(0.2)

        self.fc1 = nn.Linear(57, 285)
        self.fc2 = nn.Linear(285, 285)
        self.fc3 = nn.Linear(285, 285)
        self.fc4 = nn.Linear(285, 228)
        self.fc5 = nn.Linear(228, 171)
        self.fc6 = nn.Linear(171, 114)
        self.fc7 = nn.Linear(114,64)

        self.sigmoid = nn.Sigmoid()

    def forward(self, radiant_team_data, dire_team_data):
        r_team_block, r_player_block, r_hero_block = radiant_team_data
        d_team_block, d_player_block, d_hero_block = dire_team_data

        r_x = self.fc1(r_hero_block)
        d_x = self.fc1(d_hero_block)


        x = torch.cat([r_x, d_x], dim=0)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.fc4(x)
        x = self.leaky_relu2(x)
        x = self.fc5(x)
        x = self.fc6(x)
        x = self.fc7(x)

        x = self.sigmoid(x)

        return x



class MainNetwork(nn.Module):
    def __init__(self):
        super().__init__()

        self.relu = nn.ReLU()

        self.branch_t = BranchTeam()
        self.branch_p = BranchPlayers()
        self.branch_h = BranchHeroes()

        self.final_layer1 = nn.Linear(139, 264)
        self.final_layer2 = nn.Linear(264, 192)
        self.final_layer3= nn.Linear(192, 128)
        self.final_layer4 = nn.Linear(128, 64)
        self.final_layer5 = nn.Linear(64, 32)
        self.final_layer6 = nn.Linear(32, 16)
        self.final_layer7 = nn.Linear(16, 8)
        self.final_layer8 = nn.Linear(8, 4)
        self.final_layer9 = nn.Linear(4, 2)
        self.final_layer10 = nn.Linear(2, 1)

        self.sigmoid = nn.Sigmoid()

    def forward(self, radiant_team_data, dire_team_data):

        out_team = self.branch_t(radiant_team_data, dire_team_data)
        out_players = self.branch_p(radiant_team_data, dire_team_data)
        out_heroes = self.branch_h(radiant_team_data, dire_team_data)


        combined = torch.cat([out_team.mean(dim=0, keepdim=True),
                              out_players.mean(dim=0, keepdim=True),
                              out_heroes.mean(dim=0, keepdim=True)], dim=1)



        output = self.final_layer1(combined)
        output = self.final_layer2(output)
        output = self.final_layer3(output)
        output = self.final_layer4(output)
        output = self.final_layer5(output)
        output = self.final_layer6(output)
        output = self.final_layer7(output)
        output = self.relu(output)
        output = self.final_layer8(output)
        output = self.final_layer9(output)
        output = self.relu(output)
        output = self.final_layer10(output)
        output = self.sigmoid(output)


        return output