from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', MainHomeView.as_view(), name='index'),
    path('pick/heroes/', Heroes_pick.as_view(), name='heroes'),
    path('matches', Matches.as_view(), name='matches'),
]
