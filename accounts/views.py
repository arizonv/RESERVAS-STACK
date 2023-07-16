from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User

from django.views.generic import CreateView, UpdateView, FormView, DetailView
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserAdminCreationForm

from django.views.generic import ListView, DeleteView
from django.shortcuts import render, get_object_or_404


# view protegida
class IndexView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/index.html'
    login_url = reverse_lazy('Login:login')
        
    def get_object(self):
        return self.request.user


## FUNCIONES DE USUARIO   ##


class UserListView(ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'



class UserDeleteView(DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('account:user_list')
    context_object_name = 'user'


class RegisterView(CreateView):

    model = User
    template_name = 'accounts/register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('account:index')
    
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
    success_url = reverse_lazy('account:index')

    def get_object(self):
        return self.request.user

class UserEditAdminView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/update_admin.html'
    fields = ['name', 'email', 'is_staff']
    success_url = reverse_lazy('account:index')

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')  
        return get_object_or_404(User, pk=user_id)



class UpdatePasswordView(LoginRequiredMixin, FormView):

    template_name = 'accounts/update_password.html'
    login_url = reverse_lazy('Login:login')
    success_url = reverse_lazy('account:index')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_password_validation'] = False  # Agrega esta línea
        return context




index = IndexView.as_view()
register = RegisterView.as_view()

update_user = UpdateUserView.as_view()
update_admin = UserEditAdminView.as_view()

update_password = UpdatePasswordView.as_view()
user_list = UserListView.as_view()
user_delete = UserDeleteView.as_view()






