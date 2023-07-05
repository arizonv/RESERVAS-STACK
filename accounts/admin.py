from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User



class UserAdmin(BaseUserAdmin):
    # Los campos que se mostrarán en el formulario de creación de usuario
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('name', 'email')}),
        ('Permisos', {'fields': ('is_superuser',)}),
        ('Estado', {'fields': ('is_active',)}),
    )

    # Los campos que se mostrarán en la visualización del detalle de usuario
    readonly_fields = ('last_login', 'date_joined')

    # Los campos que se mostrarán en la lista de usuarios
    list_display = ('username', 'name', 'email', 'is_staff', 'is_active')

    # Los filtros que se mostrarán en la lista de usuarios
    list_filter = ('is_staff', 'is_active')

    # Los campos de búsqueda que se utilizarán en la lista de usuarios
    search_fields = ('username', 'name', 'email')


# Registra el modelo User con la clase UserAdmin personalizada
admin.site.register(User, UserAdmin)
