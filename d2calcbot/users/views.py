from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import  HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from users.forms import RegisterUserForm, LoginUserForm
from main.utils import DataMixin
from django.views.generic.edit import FormView
from .models import *



from django.views.generic.edit import FormView

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('users:profile')


    def form_valid(self, form):
        telegram_id = form.cleaned_data['telegram_id']
        telegram_username = form.cleaned_data['telegram_username']



        user = authenticate(telegram_id=telegram_id, telegram_username=telegram_username)

        if user and user.is_active:
            login(self.request, user, backend='users.authentication.TelegramIdAuth')
            return super().form_valid(form)


        else:
            form.add_error(None, 'Неправильный telegram-id или username')
            return super().form_invalid(form)



def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


class RegisterUser(FormView):
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        # Получите значения из формы
        telegram_id = form.cleaned_data['telegram_id']
        telegram_username = form.cleaned_data['telegram_username']


        existing_user = Custom_User.objects.filter(telegram_id=telegram_id).first()

        if existing_user:
            form.add_error(None, 'Пользователь с таким telegram-id уже существует.')
            return super().form_invalid(form)
        else:
            user = Custom_User.objects.create_user(
                telegram_id=telegram_id,
                telegram_username=telegram_username,
            )


            return super().form_valid(form)

class Profile(LoginRequiredMixin,DataMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мой профиль')
        return dict(list(context.items()) + list(c_def.items()))

