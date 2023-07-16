from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'admin'

    def handle_no_permission(self):
        print("No tienes permisos!")
        messages.error(
            self.request, "No tienes permisos!"
        )
        return redirect(to='/')


class TrabajadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'trabajador'

    def handle_no_permission(self):
        print("No tienes permisos!")
        messages.error(
            self.request, "No tienes permisos!"
        )
        return redirect(to='/')


class ClienteRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'cliente'

    def handle_no_permission(self):
        print("No tienes permisos!")
        messages.error(
            self.request, "No tienes permisos!"
        )
        return redirect(to='/')



class AdminOrTrabajadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user_role = self.request.user.role
        return user_role == 'admin' or user_role == 'trabajador'

    def handle_no_permission(self):
        print("No tienes permisos!")
        messages.error(
            self.request, "No tienes permisos!"
        )
        return redirect(to='/')
