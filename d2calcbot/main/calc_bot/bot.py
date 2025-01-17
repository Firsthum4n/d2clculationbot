from django.db.models.expressions import result
from sympy.codegen.ast import float32
from main.db_update.heroes import create_or_update_heroes
from main.db_update.teams import create_or_update_teams
from .test_data import matches_result
from main.models import *
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, random_split
import os
import json
import requests
import time


def encryption(radiant, dire):
    radiant_team_data = dataset(radiant, dire)
    dire_team_data = dataset(dire, radiant)


    model = MainNetwork()
    model.load_state_dict(torch.load('main/calc_bot/dota_model_ver7777.pth'))

    model.eval()
    with torch.no_grad():
        output = model(radiant_team_data,dire_team_data)
        if output.item() <= 0.5:
            win = f'победа radiant {output.item()}'
        elif output.item() > 0.5:
            win = f'победа dire {output.item()}'
    return win



"""функция создающий словарь со всеми именами и статами команды, игроков и героев"""
def encryption_level_1(team_pick, enemy_team_pick):
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
    enemy_ids = []
    for i in all_heroes:
        for j in enemy_team_pick['heroes']:
            if j == i.name:
                enemy_ids.append(i.hero_id)
    stats = {}
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
                with open(f'main/calc_bot/matchupjson/{hero.hero_id}.json', 'r') as f:
                    match_up  = json.load(f)
                stats[hero.name] = [m['wins'] for m in match_up if m['hero_id'] in enemy_ids]
                team_all_pick['heroes'][count]['name'] = [hero.name]
                team_all_pick['heroes'][count]['stats'] = [hero.pro_pick, hero.pro_win]

                team_all_pick['heroes'][count]['stats'].extend(stats[hero.name])
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


def dataset(data, enemy_data):
    num_teams = 6
    num_players = 10
    num_heroes = 10
    embedding_dim = 32

    team_embedding = nn.Embedding(num_teams, embedding_dim)
    player_embedding = nn.Embedding(num_players, embedding_dim)
    hero_embedding = nn.Embedding(num_heroes, embedding_dim)

    team_data = encryption_level_1(data, enemy_data)
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
    def __init__(self, data, team, index, enemy_team, enemy_index):
        self.data = data
        self.team = team
        self.index = index
        self.enemy_team = enemy_team
        self.enemy_index = enemy_index

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
        enemy_data = self.data[idx]['game'][self.enemy_index][self.enemy_team]
        team_data = encryption_level_1(data_for_encryption, enemy_data)


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
        self.fc1 = nn.Linear(35, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 16)

    def forward(self, radiant_team_data, dire_team_data):
        r_team_block, r_player_block, r_hero_block = radiant_team_data
        d_team_block, d_player_block, d_hero_block = dire_team_data

        r_x = self.fc1(r_team_block)
        d_x = self.fc1(d_team_block)

        x = torch.cat([r_x, d_x], dim=0)
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        return x


class BranchPlayers(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(34, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 16)


    def forward(self, radiant_team_data, dire_team_data):
        r_team_block, r_player_block, r_hero_block = radiant_team_data
        d_team_block, d_player_block, d_hero_block = dire_team_data

        r_x = self.fc1(r_player_block)
        d_x = self.fc1(d_player_block)
        x = torch.cat([r_x, d_x], dim=0)
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        return x


class BranchHeroes(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(39, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 16)

    def forward(self, radiant_team_data, dire_team_data):
        r_team_block, r_player_block, r_hero_block = radiant_team_data
        d_team_block, d_player_block, d_hero_block = dire_team_data

        r_x = self.fc1(r_hero_block)
        d_x = self.fc1(d_hero_block)
        x = torch.cat([r_x, d_x], dim=0)
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        return x



class MainNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()
        self.branch_t = BranchTeam()
        self.branch_p = BranchPlayers()
        self.branch_h = BranchHeroes()
        self.final_layer1 = nn.Linear(48, 32)
        self.final_layer2 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()


    def forward(self, radiant_team_data, dire_team_data):
        out_team = self.branch_t(radiant_team_data, dire_team_data)
        out_players = self.branch_p(radiant_team_data, dire_team_data)
        out_heroes = self.branch_h(radiant_team_data, dire_team_data)

        combined = torch.cat([out_team.mean(dim=0, keepdim=True),
                              out_players.mean(dim=0, keepdim=True),
                              out_heroes.mean(dim=0, keepdim=True)], dim=1)
        output = self.relu(self.final_layer1(combined))
        output = self.final_layer2(output)
        output = self.sigmoid(output)
        return output