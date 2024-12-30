from main.db_update.heroes import create_or_update_heroes
from main.db_update.teams import create_or_update_teams
from main.models import *


radiant_pick = {
    'team':
        'Liquid',
    'heroes':
        ['Timbersaw', 'Dragon Knight', 'Templar Assassin', 'Muerta', 'Enchantress']
    }

dire_pick = {
    'team':
        'Tundra',
    'heroes':
        ['Beastmaster', 'Storm Spirit', 'Lifestealer', 'Clockwerk', 'Shadow Demon']
    }

def encryption(radiant, dire):
    all_heroes = Heroes.objects.all()
    all_teams = Teams.objects.all()
    all_players = Players.objects.all()
    radiant_all_pick = {
        'team':[
            {
                'name':[],
                'stats':[]
            }
        ],
        'players':[
            {
                'name':[],
                'stats':[]
            }
        ],
        'heroes':[
            {
                'name': [],
                'stats': []
            }
        ]
   }

    dire_all_pick = {
        'team':[
            {
                'name':[],
                'stats':[]
            }
        ],
        'players':[
            {
                'name':[],
                'stats':[]
            }
        ],
        'heroes':[
            {
                'name': [],
                'stats': []
            }
        ]
   }


    for value in radiant.values():
        for i in all_teams:
            if value == i.name:
                print(value)
