from django.urls import path
from . import  views


app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('login_from_telegram/', views.login_from_telegram, name='login_from_telegram'),
]
