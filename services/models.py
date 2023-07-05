from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate
from django.dispatch import receiver




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

from .agendas import create_agenda

@receiver(post_migrate)
def generate_agenda(sender, **kwargs):
    if sender.name == 'services':
        if not Agenda.objects.exists():  # Verificar si existe la agenda
            canchas = Cancha.objects.all()
            for cancha in canchas:
                create_agenda(cancha)


