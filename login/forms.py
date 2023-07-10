from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        error_messages={
            'required': 'El campo de usuario es obligatorio.',
            'max_length': 'El nombre de usuario es demasiado largo.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': 'El campo de contraseña es obligatorio.',
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError('El usuario o la contraseña son incorrectos.')

        return cleaned_data
