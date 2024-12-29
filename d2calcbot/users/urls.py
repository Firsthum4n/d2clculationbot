from django.urls import path
from . import  views


app_name = 'users'

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('history/', views.History.as_view(), name='history'),
    path('api/auth/', views.auth_user_tg, name='auth'),
    path('notin/', views.LogoutView.as_view(), name='notin'),
]
