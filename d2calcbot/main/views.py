from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, TemplateView
from django.http import JsonResponse
from .models import *
import json
from .utils import *
from .calculation import  low_calculation
from .db_update.heroes import create_or_update_heroes, del_all_heroes_and_ids
from .db_update.teams import create_or_update_teams

#
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




class Heroes_pick(View):
    def post(self, request):
        data = json.loads(request.body)
        radiant_heroes = data.get('radiant_heroes', [])
        request.session['radiant_heroes'] = radiant_heroes
        print(radiant_heroes)

        dire_heroes = data.get('dire_heroes', [])
        request.session['dire_heroes'] = dire_heroes
        print(dire_heroes)

        result = low_calculation(radiant_heroes, dire_heroes)


        return JsonResponse(
            {'result': result,
             'radiant_heroes': radiant_heroes,}
        )


class Matches(TemplateView, DataMixin,):
    template_name = "main/matches.html"
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Матчи')
        return dict(list(context.items()) + list(c_def.items()))