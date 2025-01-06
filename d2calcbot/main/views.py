from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, TemplateView
from django.http import JsonResponse
from sympy import xring

from .models import *
import json
from .utils import *
from .calculation import  low_calculation
from .db_update.heroes import create_or_update_heroes, del_all_heroes_and_ids
from .db_update.teams import create_or_update_teams
from main.calc_bot.bot import encryption, DotaDataset, MainNetwork
from main.calc_bot.test_data import matches_test


import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

x_data, y_data = matches_test()
y_data = torch.tensor(y_data, dtype=torch.float32)


radiant_team_data = DotaDataset(x_data, 'radiant', 0)
dire_team_data = DotaDataset(x_data, 'dire', 1)



r = radiant_team_data[0]
d = dire_team_data[0]

winner = y_data[0]
winner = winner.unsqueeze(0)

batch_size = 32
dataloader = DataLoader(list(zip(r, d)), batch_size=batch_size, shuffle=True)

num_teams = 6
num_players = 10
num_heroes = 10
embedding_dim = 32

model = MainNetwork()
# output = model(r, d)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

EPOCHS = 5


for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for i, (radiant_batch, dire_batch) in enumerate(dataloader):
        optimizer.zero_grad()
        output = model(radiant_batch, dire_batch)
        output = output.squeeze(1)


        print(output)
        print(winner)
        print(output.size())
        print(winner.size())
        loss = criterion(output, winner)
        loss.backward(retain_graph=True)
        optimizer.step()
        running_loss += loss.item()

    print(f'Epoch {epoch+1}, Loss: {running_loss / len(x_data):.4f}')

print("Обучение завершено.")


# test = matches_test()
#
# print(test[0])


# create_or_update_teams()
# create_or_update_heroes()



class MainHomeView(LoginRequiredMixin,DataMixin, ListView):
    """
    Класс представления страницы выбоар героеев
    """

    model = Heroes
    template_name = 'main/index.html'
    context_object_name = 'heroes'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context.update(c_def)
        context['teams'] = Teams.objects.all()
        return context




class All_pick(View):
    def post(self, request):
        data = json.loads(request.body)
        radiant_pick = data.get('radiantPick', [])
        request.session['radiantPick'] = radiant_pick
        print(radiant_pick)

        dire_pick = data.get('direPick', [])
        request.session['direPick'] = dire_pick
        print(dire_pick)

        result = encryption(radiant_pick, dire_pick)



        return JsonResponse(
            {'result': result}
        )


class Matches(TemplateView, DataMixin,):
    template_name = "main/matches.html"
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Матчи')
        return dict(list(context.items()) + list(c_def.items()))