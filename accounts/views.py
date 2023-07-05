from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import User

from django.views.generic import CreateView, UpdateView, FormView, DetailView
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserAdminCreationForm


class TestMixinIsAdmin(UserPassesTestMixin):
    def test_func(self):
        is_admin_or_is_staff = self.request.user.is_superuser or \
            self.request.user.is_staff
        return bool(is_admin_or_is_staff)

    def handle_no_permission(self):
        print("No tienes permisos!")
        messages.error(
            self.request, "No tienes permisos!"
        )
        return redirect(to='/')

###  FUNCION protegida  ###

class IndexView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/index.html'
    login_url = reverse_lazy('Login:login')
        
    def get_object(self):
        return self.request.user



## FUNCIONES DE USUARIO   ##
class RegisterView(CreateView):

    model = User
    template_name = 'accounts/register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('accounts:index')
    
    def form_valid(self, form):
        messages.info(
            self.request, "Registro realizado con exito"
        )
        return super().form_valid(form)

class UpdateUserView(LoginRequiredMixin, UpdateView):

    model = User
    login_url = reverse_lazy('Login:login')
    template_name = 'accounts/update_user.html'
    fields = ['name', 'email']
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        return self.request.user


class UpdatePasswordView(LoginRequiredMixin, FormView):

    template_name = 'accounts/update_password.html'
    login_url = reverse_lazy('Login:login')
    success_url = reverse_lazy('accounts:index')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UpdatePasswordView, self).form_valid(form)








index = IndexView.as_view()
register = RegisterView.as_view()
update_user = UpdateUserView.as_view()
update_password = UpdatePasswordView.as_view()

