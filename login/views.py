from django.contrib.auth import authenticate
from django.contrib import auth

from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import LoginForm
from django.views.generic import FormView

from django.contrib.auth import login, logout
import requests
from django.http import HttpResponseRedirect

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from django.views import View
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


class LoginView(FormView):
    template_name = 'log/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        response = requests.post('http://127.0.0.1:8000/api/log/', json={'username': username, 'password': password})
        if response.status_code == 200:
            try:
                u = response.json()
                token = u['token']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(self.request, user)
                    response = HttpResponseRedirect(self.success_url)
                    response.set_cookie('access', value=token)
                    messages.success(self.request, 'Bienvenido')
                    return response
                else:
                    messages.error(self.request, 'No se pudo autenticar al usuario')
                    logger.error('autenticacion de usuario')
            except ValueError:
                messages.error(self.request, 'Error en la respuesta de la API de login')
                logger.error('Error API login')
        else:
            messages.error(self.request, 'No se pudo iniciar sesión. Por favor, intenta de nuevo más tarde.')
            logger.error('Credenciales incorrectas')
        return redirect('Login:login')


class LogoutView(View):

    def get(self, request):
        token = request.COOKIES.get('access')
        if not token:
            logout(request)
            response = redirect(to='home')
            response.delete_cookie('csrftoken')
            messages.error(request, 'No se ha proporcionado un token de autenticación.')
            return response

        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://127.0.0.1:8000/api/out/', headers=headers)
        if response.status_code == 200:
            logout(request)
            response = redirect('home')
            response.delete_cookie('access')
            response.delete_cookie('csrftoken')
            messages.success(request, 'Se ha cerrado sesión correctamente.')
            return response

        messages.error(request, 'No se pudo cerrar sesión. Por favor, intenta de nuevo más tarde.')
        return redirect('home')



