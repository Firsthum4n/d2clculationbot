from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', MainHomeView.as_view(), name='index'),
    path('pick/heroes/', All_pick.as_view(), name='heroes'),
    path('matches', Matches.as_view(), name='matches'),

    path('train_model/', views.train_model, name='train_model'),
]
