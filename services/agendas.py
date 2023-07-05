from .models import Horario, Agenda, Cancha
from django.core.exceptions import ValidationError

def create_agenda(cancha):
    horarios = Horario.objects.all()
    for horario in horarios:
        agenda = Agenda(cancha=cancha, horario=horario)
        try:
            agenda.full_clean()
            agenda.save()
        except ValidationError as e:
            # Manejar la validación de errores aquí
            pass
