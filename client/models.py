from django.db import models
from services.models import Agenda
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.utils import timezone
import datetime



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
    dia = models.DateField()
    confirmada = models.BooleanField(default=False)

    class Meta:
        unique_together = ('agenda', 'cliente', 'dia')


    def __str__(self):
        confirmacion = "Confirmada" if self.confirmada else "Pendiente"
        formatted_date = self.dia.strftime('%d-%m-%Y')
        return f"Reserva de {self.cliente} para el {formatted_date} ({confirmacion}), {self.agenda.cancha} {self.agenda.horario}"



@receiver(post_save, sender=Reserva)
def crear_boleta(sender, instance, created, **kwargs):
    if created or (not instance._state.adding and instance.confirmada):
        Boleta.objects.create(cliente=instance.cliente, reserva=instance)


class Boleta(models.Model):
    fecha = models.DateTimeField(default=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)

    class Meta:
        db_table = 'boleta'

    def __str__(self):
        return f'{self.reserva}'

    
