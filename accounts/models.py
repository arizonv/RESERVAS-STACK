import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)


class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(
        'Usuario', max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'ingrese un nombre de usuario valido '
                'Este valor debe contener solo letras, números '
                'excepto: @/./+/-/_.'
                ,  'invalid'
            )
        ], help_text='Un nombre corto que sera usado'+
                    ' para identificarlo de forma unica en la plataforma.'
    )
    
    name = models.CharField('Name', max_length=100)
    email = models.EmailField('Email', unique=True)
    is_staff = models.BooleanField('Admin', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.name or self.username
    
    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(' ')[0]
