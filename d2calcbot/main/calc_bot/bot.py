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



def encryption(r_d):
    data_no_grad = DotaDataset_no_grad(r_d)
    batch_size = 1

    dataloader = DataLoader(data_no_grad, batch_size=batch_size)

    model = MainNetwork()
    model.load_state_dict(torch.load('main/calc_bot/actual_models/dota_model_ver00.pth'))
    model.eval()
    with torch.no_grad():
        for i, (batch_data) in enumerate(dataloader):
            output = model(batch_data)
            output = output.squeeze(1)
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
    team_heroes = {}

    for team in all_teams:
        if team_pick['team'] == team.name:
            team_players = team.get_players()
            team_all_pick['team'][0]['name'] = team.name
            team_all_pick['team'][0]['stats'] = [((team.wins / (team.wins + team.losses)) * 100, 100), (team.wins, team.wins + team.losses), (team.rating, 3000)]

            with open(f'main/calc_bot/matchupjsonteams/{team.team_id}.json', 'r') as f:
                teams_up = json.load(f)

            team_heroes[team.name] = []
            if len(teams_up) > 0:
                team_heroes[team.name] = [(th["wins"], th["games_played"])
                                          for hh in team_pick['heroes']
                                          for th in teams_up
                                          if hh in th["localized_name"]]

            if len(team_heroes[team.name]) < 5:
                for i in range(5 - len(team_heroes[team.name])):
                    team_heroes[team.name].append((0, 0))
            team_all_pick['team'][0]['stats'].extend(team_heroes[team.name])




            for i in range(min(len(team_players), 5)):

                team_total_games = team.wins + team.losses
                player_winrate = (team_players[i].wins / team_players[i].games_played) * 100 if team_players[i].games_played > 0 else 0
                player_rating = player_winrate * 0.7 + (team.rating / 5) * 0.3
                team_winrate = (team.wins / team_total_games) * 100 if team_total_games > 0 else 0

                team_all_pick['players'][i]['name'] = [team_players[i].name if team_players else None]
                team_all_pick['players'][i]['stats'] = [(team_players[i].wins, team_players[i].games_played),
                                                        (player_winrate, 100),
                                                        ((team_players[i].wins / team.wins) * 100, 100),
                                                        ((player_winrate - team_winrate) / team_winrate, 100),
                                                        ((team_players[i].wins / team.wins) * 100, 100),
                                                        (team.rating / 5, 3000),
                                                        (player_winrate / team_winrate, 100) if team_winrate > 0 else 0,
                                                        (player_rating, 150)
                                                        if team_players else None]




    count = 0
    for h in team_pick['heroes']:
        for hero in all_heroes:
            if h == hero.name:
                with open(f'main/calc_bot/matchupjson/{hero.hero_id}.json', 'r') as f:
                    match_up  = json.load(f)
                stats[hero.name] = [((m['wins'] / m["games_played"]) * 100, 100) for m in match_up if m['hero_id'] in enemy_ids]
                total_hero_winrate = 0
                for i in stats[hero.name]:
                    total_hero_winrate += i[0]

                team_all_pick['heroes'][count]['name'] = [hero.name]
                team_all_pick['heroes'][count]['stats'] = [(hero.pro_win, hero.pro_pick), ((hero.pro_win / hero.pro_pick) * 100, 100)]
                team_all_pick['heroes'][count]['stats'].extend(stats[hero.name])
                team_all_pick['heroes'][count]['stats'].append((total_hero_winrate / 5, 100))
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

    embedding_dim = 8
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

    team_stats_list = []
    for stat in team_data[0]['stats']:
        if isinstance(stat, tuple):
            team_stats_list.append(list(stat))
        else:
            team_stats_list.append([stat])

    team_stats = torch.tensor(team_stats_list, dtype=torch.float32)
    player_stats = torch.tensor([player['stats'] for player in player_data], dtype=torch.float32)

    all_stats = []
    for hero in hero_data:
        hero_stats_lst = []
        for stat in hero['stats']:
            if isinstance(stat, tuple):
                hero_stats_lst.append(list(stat))
            else:
                hero_stats_lst.append([stat])
        all_stats.append(hero_stats_lst)

    hero_stats = torch.tensor(all_stats, dtype=torch.float32)



    return team_index, player_indices, hero_indices, team_stats, player_stats, hero_stats


def dataset(data, enemy_data):
    num_teams = 1
    num_players = 5
    num_heroes = 5
    embedding_dim = 8

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

    team_emb_repeated = team_emb.unsqueeze(1).repeat(1, 8, 1)
    team_block = torch.cat((team_emb_repeated, team_stats), dim=2)


    player_emb_repeated = player_emb.unsqueeze(1).repeat(1, 8, 1)
    player_block = torch.cat((player_emb_repeated, player_stats), dim=2)


    hero_emb_repeated = hero_emb.unsqueeze(1).repeat(1, 8, 1)
    hero_block = torch.cat((hero_emb_repeated, hero_stats), dim=2)

    return team_block, player_block, hero_block







def data_for_dataset_no_grad(x_data):
    radiant_data_for_encryption = []
    dire_data_for_encryption = []
    for i in range(len(x_data)):
        radiant_data_for_encryption.append(x_data[i]['game'][0]['radiant'])
        dire_data_for_encryption.append(x_data[i]['game'][1]['dire'])


    radiant_encryption_list = []
    dire_decryption_list = []

    for i in range(len(radiant_data_for_encryption)):
        radiant_encryption_list.append(encryption_level_1(radiant_data_for_encryption[i], dire_data_for_encryption[i]))
        dire_decryption_list.append(encryption_level_1(dire_data_for_encryption[i], radiant_data_for_encryption[i]))

    radiant_tensor_list = []
    dire_tensor_list = []

    for i in range(len(radiant_encryption_list)):
        (r_team_index, r_player_indices, r_hero_indices,
         r_team_stats, r_player_stats, r_hero_stats) = transform_data(radiant_encryption_list[i]['team'],
                                                                    radiant_encryption_list[i]['players'],
                                                                    radiant_encryption_list[i]['heroes'],
                                                                    radiant_encryption_list[i])

        radiant_tensor_list.append((r_team_index, r_player_indices, r_hero_indices,
         r_team_stats, r_player_stats, r_hero_stats))


    for i in range(len(dire_decryption_list)):
        (d_team_index, d_player_indices, d_hero_indices,
         d_team_stats, d_player_stats, d_hero_stats) = transform_data(dire_decryption_list[i]['team'],
                                                                    dire_decryption_list[i]['players'],
                                                                    dire_decryption_list[i]['heroes'],
                                                                    dire_decryption_list[i])

        dire_tensor_list.append((d_team_index, d_player_indices, d_hero_indices,
         d_team_stats, d_player_stats, d_hero_stats))



    return radiant_tensor_list, dire_tensor_list

class DotaDataset_no_grad(Dataset):
    def __init__(self, x_data):
        self.x_data = x_data

        num_teams = 1
        num_players = 5
        num_heroes = 5
        embedding_dim = 8

        self.team_embedding = nn.Embedding(num_teams, embedding_dim)
        self.player_embedding = nn.Embedding(num_players, embedding_dim)
        self.hero_embedding = nn.Embedding(num_heroes, embedding_dim)

    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, idx):
        self.radiant_tensor_list, self.dire_tensor_list = data_for_dataset_no_grad(self.x_data)

        r_team_index = self.radiant_tensor_list[idx][0]
        r_player_indices = self.radiant_tensor_list[idx][1]
        r_hero_indices = self.radiant_tensor_list[idx][2]
        r_team_stats = self.radiant_tensor_list[idx][3]
        r_player_stats = self.radiant_tensor_list[idx][4]
        r_hero_stats = self.radiant_tensor_list[idx][5]


        r_team_index = torch.tensor([r_team_index])

        r_team_emb = self.team_embedding(r_team_index)
        r_team_stats = r_team_stats.unsqueeze(0)

        r_player_indices = torch.tensor(r_player_indices)
        r_player_emb = self.player_embedding(r_player_indices)

        r_hero_indices = torch.tensor(r_hero_indices)
        r_hero_emb = self.hero_embedding(r_hero_indices)


        r_team_emb_repeated = r_team_emb.unsqueeze(1).repeat(1, 8, 1)
        r_team_block = torch.cat((r_team_emb_repeated, r_team_stats), dim=2)

        r_player_emb_repeated = r_player_emb.unsqueeze(1).repeat(1, 8, 1)
        r_player_block = torch.cat((r_player_emb_repeated, r_player_stats), dim=2)

        r_hero_emb_repeated = r_hero_emb.unsqueeze(1).repeat(1, 8, 1)
        r_hero_block = torch.cat((r_hero_emb_repeated, r_hero_stats), dim=2)

        d_team_index = self.dire_tensor_list[idx][0]
        d_player_indices = self.dire_tensor_list[idx][1]
        d_hero_indices = self.dire_tensor_list[idx][2]
        d_team_stats = self.dire_tensor_list[idx][3]
        d_player_stats = self.dire_tensor_list[idx][4]
        d_hero_stats = self.dire_tensor_list[idx][5]

        d_team_index = torch.tensor([d_team_index])

        d_team_emb = self.team_embedding(d_team_index)
        d_team_stats = d_team_stats.unsqueeze(0)

        d_player_indices = torch.tensor(d_player_indices)
        d_player_emb = self.player_embedding(d_player_indices)

        d_hero_indices = torch.tensor(d_hero_indices)
        d_hero_emb = self.hero_embedding(d_hero_indices)

        d_team_emb_repeated = d_team_emb.unsqueeze(1).repeat(1, 8, 1)
        d_team_block = torch.cat((d_team_emb_repeated, d_team_stats), dim=2)

        d_player_emb_repeated = d_player_emb.unsqueeze(1).repeat(1, 8, 1)
        d_player_block = torch.cat((d_player_emb_repeated, d_player_stats), dim=2)

        d_hero_emb_repeated = d_hero_emb.unsqueeze(1).repeat(1, 8, 1)
        d_hero_block = torch.cat((d_hero_emb_repeated, d_hero_stats), dim=2)

        r_flag = torch.zeros((r_team_block.shape[0], 8, 1), device=r_team_block.device).expand(-1, -1, 5)
        d_flag = torch.ones((d_team_block.shape[0], 8, 1), device=d_team_block.device).expand(-1, -1, 5)

        r_team_block = torch.cat((r_team_block, r_flag), dim=-1)
        d_team_block = torch.cat((d_team_block, d_flag), dim=-1)

        r_flag = torch.zeros((r_player_block.shape[0], 8, 1), device=r_player_block.device)
        d_flag = torch.ones((d_player_block.shape[0], 8, 1), device=d_player_block.device)


        r_player_block = torch.cat((r_player_block, r_flag), dim=-1)
        d_player_block = torch.cat((d_player_block,  d_flag), dim=-1)

        r_hero_block = torch.cat((r_hero_block,  r_flag), dim=-1)
        d_hero_block = torch.cat((d_hero_block,  d_flag), dim=-1)


        return r_team_block, r_player_block, r_hero_block, d_team_block, d_player_block, d_hero_block



def data_for_dataset(x_data):
    radiant_data_for_encryption = []
    dire_data_for_encryption = []
    winner = []
    for i in range(len(x_data)):
        radiant_data_for_encryption.append(x_data[i]['game'][0]['radiant'])
        dire_data_for_encryption.append(x_data[i]['game'][1]['dire'])
        winner.append(x_data[i]['game'][2]['winner'])

    radiant_encryption_list = []
    dire_decryption_list = []

    for i in range(len(radiant_data_for_encryption)):
        radiant_encryption_list.append(encryption_level_1(radiant_data_for_encryption[i], dire_data_for_encryption[i]))
        dire_decryption_list.append(encryption_level_1(dire_data_for_encryption[i], radiant_data_for_encryption[i]))

    radiant_tensor_list = []
    dire_tensor_list = []

    for i in range(len(radiant_encryption_list)):
        (r_team_index, r_player_indices, r_hero_indices,
         r_team_stats, r_player_stats, r_hero_stats) = transform_data(radiant_encryption_list[i]['team'],
                                                                    radiant_encryption_list[i]['players'],
                                                                    radiant_encryption_list[i]['heroes'],
                                                                    radiant_encryption_list[i])

        radiant_tensor_list.append((r_team_index, r_player_indices, r_hero_indices,
         r_team_stats, r_player_stats, r_hero_stats))


    for i in range(len(dire_decryption_list)):
        (d_team_index, d_player_indices, d_hero_indices,
         d_team_stats, d_player_stats, d_hero_stats) = transform_data(dire_decryption_list[i]['team'],
                                                                    dire_decryption_list[i]['players'],
                                                                    dire_decryption_list[i]['heroes'],
                                                                    dire_decryption_list[i])

        dire_tensor_list.append((d_team_index, d_player_indices, d_hero_indices,
         d_team_stats, d_player_stats, d_hero_stats))


    winner_tensor_list = torch.tensor(winner, dtype=torch.float32)



    return radiant_tensor_list, dire_tensor_list, winner_tensor_list


class DotaDataset(Dataset):
    def __init__(self, x_data):
        self.x_data = x_data


        num_teams = 1
        num_players = 5
        num_heroes = 5
        embedding_dim = 8

        self.team_embedding = nn.Embedding(num_teams, embedding_dim)
        self.player_embedding = nn.Embedding(num_players, embedding_dim)
        self.hero_embedding = nn.Embedding(num_heroes, embedding_dim)

    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, idx):

        self.radiant_tensor_list, self.dire_tensor_list, self.winner_tensor_list = data_for_dataset(self.x_data)

        r_team_index = self.radiant_tensor_list[idx][0]
        r_player_indices = self.radiant_tensor_list[idx][1]
        r_hero_indices = self.radiant_tensor_list[idx][2]
        r_team_stats = self.radiant_tensor_list[idx][3]
        r_player_stats = self.radiant_tensor_list[idx][4]
        r_hero_stats = self.radiant_tensor_list[idx][5]





        r_team_index = torch.tensor([r_team_index])

        r_team_emb = self.team_embedding(r_team_index)
        r_team_stats = r_team_stats.unsqueeze(0)

        r_player_indices = torch.tensor(r_player_indices)
        r_player_emb = self.player_embedding(r_player_indices)

        r_hero_indices = torch.tensor(r_hero_indices)
        r_hero_emb = self.hero_embedding(r_hero_indices)


        r_team_emb_repeated = r_team_emb.unsqueeze(1).repeat(1, 8, 1)
        r_team_block = torch.cat((r_team_emb_repeated, r_team_stats), dim=2)

        r_player_emb_repeated = r_player_emb.unsqueeze(1).repeat(1, 8, 1)
        r_player_block = torch.cat((r_player_emb_repeated, r_player_stats), dim=2)

        r_hero_emb_repeated = r_hero_emb.unsqueeze(1).repeat(1, 8, 1)
        r_hero_block = torch.cat((r_hero_emb_repeated, r_hero_stats), dim=2)

        d_team_index = self.dire_tensor_list[idx][0]
        d_player_indices = self.dire_tensor_list[idx][1]
        d_hero_indices = self.dire_tensor_list[idx][2]
        d_team_stats = self.dire_tensor_list[idx][3]
        d_player_stats = self.dire_tensor_list[idx][4]
        d_hero_stats = self.dire_tensor_list[idx][5]

        d_team_index = torch.tensor([d_team_index])

        d_team_emb = self.team_embedding(d_team_index)
        d_team_stats = d_team_stats.unsqueeze(0)

        d_player_indices = torch.tensor(d_player_indices)
        d_player_emb = self.player_embedding(d_player_indices)

        d_hero_indices = torch.tensor(d_hero_indices)
        d_hero_emb = self.hero_embedding(d_hero_indices)

        d_team_emb_repeated = d_team_emb.unsqueeze(1).repeat(1, 8, 1)
        d_team_block = torch.cat((d_team_emb_repeated, d_team_stats), dim=2)

        d_player_emb_repeated = d_player_emb.unsqueeze(1).repeat(1, 8, 1)
        d_player_block = torch.cat((d_player_emb_repeated, d_player_stats), dim=2)

        d_hero_emb_repeated = d_hero_emb.unsqueeze(1).repeat(1, 8, 1)
        d_hero_block = torch.cat((d_hero_emb_repeated, d_hero_stats), dim=2)



        r_flag = torch.zeros((r_team_block.shape[0], 8, 1), device=r_team_block.device).expand(-1, -1, 5)
        d_flag = torch.ones((d_team_block.shape[0], 8, 1), device=d_team_block.device).expand(-1, -1, 5)

        r_team_block = torch.cat((r_team_block, r_flag), dim=-1)
        d_team_block = torch.cat((d_team_block, d_flag), dim=-1)

        r_flag = torch.zeros((r_player_block.shape[0], 8, 1), device=r_player_block.device)
        d_flag = torch.ones((d_player_block.shape[0], 8, 1), device=d_player_block.device)


        r_player_block = torch.cat((r_player_block, r_flag), dim=-1)
        d_player_block = torch.cat((d_player_block,  d_flag), dim=-1)

        r_hero_block = torch.cat((r_hero_block,  r_flag), dim=-1)
        d_hero_block = torch.cat((d_hero_block,  d_flag), dim=-1)


        return (r_team_block, r_player_block, r_hero_block, d_team_block, d_player_block, d_hero_block), self.winner_tensor_list[idx]





class BranchTeam(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(15, 20)
        self.fc2 = nn.Linear(20, 10)



    def forward(self, data):
        r_team_block, r_player_block, r_hero_block, d_team_block, d_player_block, d_hero_block = data

        r_x = self.fc1(r_team_block)
        d_x = self.fc1(d_team_block)
        x = torch.cat([r_x, d_x], dim=0)
        x = self.relu(self.fc2(x))

        return x


class BranchPlayers(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(11, 20)
        self.fc2 = nn.Linear(20, 10)

    def forward(self, data):
        (r_team_block, r_player_block, r_hero_block, d_team_block, d_player_block, d_hero_block) = data

        r_x = self.fc1(r_player_block)
        d_x = self.fc1(d_player_block)
        x = torch.cat([r_x, d_x], dim=0)
        x = self.relu(self.fc2(x))


        return x


class BranchHeroes(nn.Module):
    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(11, 20)
        self.fc2 = nn.Linear(20, 10)




    def forward(self, data):
        (r_team_block, r_player_block, r_hero_block, d_team_block, d_player_block, d_hero_block) = data

        r_x = self.fc1(r_hero_block)
        d_x = self.fc1(d_hero_block)
        x = torch.cat([r_x, d_x], dim=0)
        x = self.relu(self.fc2(x))



        return x



# --- Модуль Self-Attention для тензоров ---
class TensorSelfAttention(nn.Module):
    def __init__(self, feature_dim, attention_heads=1):
        super(TensorSelfAttention, self).__init__()
        self.attention_heads = attention_heads
        self.feature_dim_head = feature_dim // attention_heads
        self.query_projection = nn.Linear(feature_dim, attention_heads * self.feature_dim_head)
        self.key_projection = nn.Linear(feature_dim, attention_heads * self.feature_dim_head)
        self.value_projection = nn.Linear(feature_dim, attention_heads * self.feature_dim_head)
        self.output_projection = nn.Linear(attention_heads * self.feature_dim_head, feature_dim)

    def forward(self, input_tensor):

        batch_size, num_objects, feature_dim = input_tensor.size()
        H = self.attention_heads
        D_head = self.feature_dim_head

        Q = self.query_projection(input_tensor).view(batch_size, num_objects, H, D_head).transpose(1, 2)
        K = self.key_projection(input_tensor).view(batch_size, num_objects, H, D_head).transpose(1, 2)
        V = self.value_projection(input_tensor).view(batch_size, num_objects, H, D_head).transpose(1, 2)

        attention_scores = torch.matmul(Q, K.transpose(-2, -1)) / (D_head ** 0.5)
        attention_weights = torch.softmax(attention_scores, dim=-1)
        attended_output = torch.matmul(attention_weights, V)

        attended_output = attended_output.transpose(1, 2).contiguous().view(batch_size, num_objects, H * D_head)
        output = self.output_projection(attended_output)
        return output

# --- Модуль Cross-Attention для тензоров ---
class TensorCrossAttention(nn.Module):
    def __init__(self, query_feature_dim, key_value_feature_dim, attention_heads=1):
        super(TensorCrossAttention, self).__init__()
        self.attention_heads = attention_heads
        self.feature_dim_head = query_feature_dim // attention_heads
        self.query_projection = nn.Linear(query_feature_dim, attention_heads * self.feature_dim_head)
        self.key_projection = nn.Linear(key_value_feature_dim, attention_heads * self.feature_dim_head)
        self.value_projection = nn.Linear(key_value_feature_dim, attention_heads * self.feature_dim_head)
        self.output_projection = nn.Linear(attention_heads * self.feature_dim_head, query_feature_dim)

    def forward(self, query_tensor, key_value_tensor):
        batch_size, num_queries, query_feature_dim = query_tensor.size()
        batch_size, num_key_values, key_value_feature_dim = key_value_tensor.size()
        H = self.attention_heads
        D_head = self.feature_dim_head

        Q = self.query_projection(query_tensor).view(batch_size, num_queries, H, D_head).transpose(1, 2)
        K = self.key_projection(key_value_tensor).view(batch_size, num_key_values, H, D_head).transpose(1, 2)
        V = self.value_projection(key_value_tensor).view(batch_size, num_key_values, H, D_head).transpose(1, 2)

        attention_scores = torch.matmul(Q, K.transpose(-2, -1)) / (D_head ** 0.5)
        attention_weights = torch.softmax(attention_scores, dim=-1)
        attended_output = torch.matmul(attention_weights, V)

        attended_output = attended_output.transpose(1, 2).contiguous().view(batch_size, num_queries, H * D_head)
        output = self.output_projection(attended_output)
        return output

# --- Гибридная модель с вниманием ---
class MainNetwork(nn.Module):
    def __init__(self, feature_dim, hidden_dim, output_dim, num_players=5, num_heroes=5, attention_heads=2):
        super(MainNetwork, self).__init__()
        self.num_players = num_players
        self.num_heroes = num_heroes
        self.feature_dim = feature_dim

        self.sigmoid = nn.Sigmoid()

        # Ветки для обработки team, players и heroes (пример - простые линейные слои)
        self.branch_t = BranchTeam()
        self.branch_p = BranchPlayers()
        self.branch_h = BranchHeroes()

        # Self-Attention для players и heroes
        self.self_attention_players = TensorSelfAttention(feature_dim, attention_heads=attention_heads)
        self.self_attention_heroes = TensorSelfAttention(feature_dim, attention_heads=attention_heads)

        # Cross-Attention между players и heroes (players смотрят на heroes)
        self.cross_attention_player_hero = TensorCrossAttention(feature_dim, feature_dim, attention_heads=attention_heads)

        # Финальный полносвязный слой для классификации (пример)
        self.fc = nn.Linear(feature_dim * (1 + 2 * num_players), 1) # Учитываем team и обработанные players и heroes

    def forward(self, batch_data):
        out_team = self.branch_t(batch_data)
        out_players = self.branch_p(batch_data).view(-1, self.num_players, self.feature_dim)
        out_heroes = self.branch_h(batch_data).view(-1, self.num_heroes, self.feature_dim)



        # Self-Attention
        attended_players = self.self_attention_players(out_players)
        attended_heroes = self.self_attention_heroes(out_heroes)

        out_team_replicated = out_team.view(attended_players.size(0), 1, -1)

        # Cross-Attention (players смотрят на heroes, обновляем представления игроков)
        attended_players_with_heroes = self.cross_attention_player_hero(attended_players, attended_heroes)



        # Объединение веток (пример - конкатенация)
        # Конкатенируем out_team и обработанные attended_players_with_heroes и attended_heroes
        combined_features_list = [out_team_replicated, attended_players_with_heroes, attended_heroes]
        combined_features = torch.cat(combined_features_list, dim=1)
        combined_features_flattened = combined_features.view(-1, self.feature_dim * (1 + 2 * self.num_players))

        # Финальный полносвязный слой
        output = self.fc(combined_features_flattened)

        output = output.mean()
        output = output.unsqueeze(0)

        output = self.sigmoid(output)

        return output