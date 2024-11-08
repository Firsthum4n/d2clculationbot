from django.urls import path
from . import  views


app_name = 'users'

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('api/register/', views.register_user_tg, name='register_tg'),
    path('api/login/', views.login_user_tg, name='login_tg'),
    path('notin/', views.LogoutView.as_view(), name='notin'),
]
