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



class Cliente(models.Model):
    SEXO = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    ]
    user = models.OneToOneField(
        'accounts.User',
        verbose_name='Usuario',
        on_delete=models.CASCADE
    )
    rut = models.CharField(max_length=10)
    sexo = models.CharField(max_length=10, choices=SEXO)

    def __str__(self):
        return f'{self.user.username}'


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    dia = models.DateTimeField()

    class Meta:
        unique_together = ('agenda', 'cliente', 'dia')

    def __str__(self):
        return f'{self.agenda} - Confirmada: {self.confirmada} - {self.dia.strftime("%Y-%m-%d")}'



class Boleta(models.Model):
    fecha = models.DateTimeField(default=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)

    class Meta:
        db_table = 'boleta'

    def __str__(self):
        return f'{self.reserva}'


class TipoCancha(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _('Tipo de Cancha')
        verbose_name_plural = _('Tipos de Canchas')


class Cancha(models.Model):
    NUMERACION_CHOICES = [
        ('1', 'Cancha 1'),
        ('2', 'Cancha 2'),
        ('3', 'Cancha 3'),
        ('4', 'Cancha 4'),
        ('5', 'Cancha 5'),
        ('6', 'Cancha 6'),
        ('7', 'Cancha 7'),
        ('8', 'Cancha 8'),
    ]
    numeracion = models.CharField(max_length=10, choices=NUMERACION_CHOICES)
    tipo = models.ForeignKey(TipoCancha, on_delete=models.CASCADE, related_name='canchas')

    def __str__(self):
        return f'Cancha {self.numeracion}'

    class Meta:
        verbose_name = _('Cancha')
        verbose_name_plural = _('Canchas')


class Horario(models.Model):
    AM = 'AM'
    PM = 'PM'
    HORAS_CHOICES = [
        ('09', '09:00 - 10:00'),
        ('10', '10:00 - 11:00'),
        ('11', '11:00 - 12:00'),
        ('12', '12:00 - 01:00'),
        ('16', '04:00 - 05:00'),
        ('17', '05:00 - 06:00'),
        ('18', '06:00 - 07:00'),
        ('19', '07:00 - 08:00'),
        ('20', '08:00 - 09:00'),
        ('21', '09:00 - 10:00'),
    ]
    MERIDIEM_CHOICES = [
        (AM, 'AM'),
        (PM, 'PM'),
    ]
    horario = models.CharField(max_length=10, choices=HORAS_CHOICES, unique=True)
    meridiem = models.CharField(max_length=2, choices=MERIDIEM_CHOICES, default=PM)

    def __str__(self):
        return f'{self.get_horario_display()} {self.get_meridiem_display()}'

    class Meta:
        verbose_name = _('Horario')
        verbose_name_plural = _('Horarios')



class Agenda(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.cancha.tipo} {self.cancha }- {self.horario}'

    class Meta:
        verbose_name = _('Agenda')
        verbose_name_plural = _('Agendas')
        unique_together = ('cancha', 'horario')







