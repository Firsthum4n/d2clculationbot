from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', MainHomeView.as_view(), name='index'),
    path('profile/', Profile.as_view(), name='profile'),
    path('api/heroes/', Heroes_pick.as_view(), name='heroes'),
]
