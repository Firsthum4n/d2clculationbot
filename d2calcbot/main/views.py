from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, TemplateView
from django.http import JsonResponse

from .models import *
import json
from .utils import *
from .db_update.heroes import create_or_update_heroes, del_all_heroes_and_ids
from .db_update.teams import create_or_update_teams, update_teams
from .db_update.match_up import teams_hero_matchup, hero_matchup
from main.calc_bot.bot import encryption, DotaDataset, MainNetwork
from main.calc_bot.test_data import matches_result, matches_test
from main.calc_bot.test_data2 import matches_result_2, matches_test_2
from main.calc_bot.test_data3 import matches_result_3, matches_test_3
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import random



x_data = matches_result_3()
# print(len(x_data))
# random.shuffle(x_data)


t_data = x_data[:270]
v_data = x_data[270:300]

train_data = DotaDataset(t_data)
valid_data = DotaDataset(v_data)

batch_size = 1
model = MainNetwork(10, 32, 2)
# model.load_state_dict(torch.load('main/calc_bot/actual_models/dota_model_ver0_1.pth'))


criterion = nn.BCELoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=6, gamma=0.1)

EPOCHS = 2


dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
valid_dataloader = DataLoader(valid_data, batch_size=batch_size)

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for i, (batch_data , winners) in enumerate(dataloader):
        optimizer.zero_grad()
        output = model(batch_data)
        loss = criterion(output, winners)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        print(f'{i+1}---Epoch {epoch+1}, Loss: {running_loss / len(x_data):.4f}, out:{output.item()}, winner:{winners.item()}')

    scheduler.step()
print("Обучение завершено.")
torch.save(model.state_dict(), 'main/calc_bot/actual_models/dota_model_ver0_2.pth')



model.load_state_dict(torch.load('main/calc_bot/actual_models/dota_model_ver0_2.pth'))

radiant_0 = 0
dire_1 = 0
right = 0

model.eval()
val_loss = 0.0
with torch.no_grad():
    for i, (batch_data , winners) in enumerate(valid_dataloader):
        output = model(batch_data)
        loss = criterion(output, winners)
        val_loss += loss.item()

        print(f' Loss: {val_loss / len(x_data):.4f}, out:{output.item()}, result: {1 if output.item() >= 0.5 else 0}, winner:{winners.item()}')

        if output.item() >= 0.5:
            dire_1 += 1
        if output.item() < 0.5:
            radiant_0 += 1
        if round(output.item()) == winners.item():
            right += 1
print(f"Обучение завершено.\n"
      f"radiant: {radiant_0}\n"
      f"dire: {dire_1}\n"
      f"right: {right}")





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

        all_pick = [
    {
        "game": [
            {
                "radiant": {
                    "team": '',
                    "heroes": []
                }
            },
            {
                "dire": {
                    "team": '',
                    "heroes": [

                    ]
                }
            }

        ]
    }]

        all_pick[0]['game'][0]['radiant']['team'] = radiant_pick['team']
        all_pick[0]['game'][0]['radiant']['heroes'].extend(radiant_pick['heroes'])
        all_pick[0]['game'][1]['dire']['team'] = dire_pick['team']
        all_pick[0]['game'][1]['dire']['heroes'].extend(dire_pick['heroes'])

        print(all_pick)

        result = encryption(all_pick)


        return JsonResponse(
            {'result': result}
        )


class Matches(TemplateView, DataMixin,):
    template_name = "main/matches.html"
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Матчи')
        return dict(list(context.items()) + list(c_def.items()))