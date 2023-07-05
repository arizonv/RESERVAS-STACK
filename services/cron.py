import schedule
import time
import datetime
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)

def validar_agenda(cancha, horario):
    # Validar si ya existe una agenda para la cancha y horario específico
    if cancha.agenda_set.filter(horario=horario, disponible=True).exists():
        return False
    return True

def crear_agendas():
    logger.info("Iniciando proceso de agenda...")
    time.sleep(2)
    from .models import Cancha, Agenda
    canchas = Cancha.objects.all()
    hoy = datetime.date.today()
    proximo_domingo = hoy + datetime.timedelta(days=(6 - hoy.weekday() + 7) % 7)
    proximo_lunes = proximo_domingo + datetime.timedelta(days=1)
    proximo_viernes = proximo_lunes + datetime.timedelta(days=4)

    for cancha in canchas:
        for horario, _ in Agenda.HORAS_CHOICES:
            if validar_agenda(cancha, horario):
                Agenda.objects.create(cancha=cancha, horario=horario, disponible=True)
    logger.info("Agendas creadas exitosamente.")

def run_schedule():
    schedule.every().sunday.at("00:00").do(crear_agendas)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Configurar el registro de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    run_schedule()

# import schedule
# import time
# import datetime
# from django.core.management.base import BaseCommand
# from django.core.management import call_command
# from django.apps import AppConfig
# from django.utils import timezone

# def crear_agendas():
#     from .models import Cancha, Agenda
#     canchas = Cancha.objects.all()
#     hoy = datetime.date.today()
#     proximo_domingo = hoy + datetime.timedelta(days=(6 - hoy.weekday() + 7) % 7)
#     proximo_lunes = proximo_domingo + datetime.timedelta(days=1)
#     proximo_viernes = proximo_lunes + datetime.timedelta(days=4)

#     for cancha in canchas:
#         for horario, _ in Agenda.HORAS_CHOICES:
#             if not cancha.agenda_set.filter(horario=horario, disponible=True).exists():
#                 Agenda.objects.create(cancha=cancha, horario=horario, disponible=True)

#     print("Agendas creadas exitosamente.")

# def run_schedule():
#     print("Procesando agenda...")
#     schedule.every().sunday.at("00:00").do(crear_agendas)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)










# # import schedule
# # import time
# # import datetime
# # from django.core.management.base import BaseCommand
# # from django.core.management import call_command
# # from django.apps import AppConfig
# # from django.utils import timezone

# # def crear_agendas():
# #     from .models import Cancha, Agenda
# #     canchas = Cancha.objects.all()
# #     hoy = datetime.date.today()
# #     proximo_lunes = hoy + datetime.timedelta(days=(0 - hoy.weekday()) % 7)
# #     proximo_viernes = proximo_lunes + datetime.timedelta(days=4)

# #     for cancha in canchas:
# #         for horario, _ in Agenda.HORAS_CHOICES:
# #             if not cancha.agenda_set.filter(horario=horario, disponible=True).exists():
# #                 Agenda.objects.create(cancha=cancha, horario=horario, disponible=True)

# #     print("Agendas creadas exitosamente.")

# # def run_schedule():
# #     print("Procesando agenda...")
# #     schedule.every(1).minutes.do(crear_agendas) 

# #     while True:
# #         schedule.run_pending()
# #         time.sleep(1)


# # import schedule
# # import time
# # import datetime
# # from django.core.management.base import BaseCommand
# # from django.core.management import call_command
# # from django.apps import AppConfig
# # from django.utils import timezone

# # def crear_agendas():
# #     from .models import Cancha, Agenda
# #     canchas = Cancha.objects.all()
# #     hoy = datetime.date.today()
# #     proximo_lunes = hoy + datetime.timedelta(days=(0 - hoy.weekday()) % 7)
# #     proximo_viernes = proximo_lunes + datetime.timedelta(days=4)

# #     for cancha in canchas:
# #         for horario, _ in Agenda.HORAS_CHOICES:
# #             if not cancha.agenda_set.filter(horario=horario, fecha__range=[proximo_lunes, proximo_viernes]).exists():
# #                 Agenda.objects.create(cancha=cancha, horario=horario, fecha=proximo_lunes)

# #     print("Agendas creadas exitosamente.")


# # def run_schedule():
# #     schedule.every().sunday.at("00:00").do(crear_agendas)

# #     while True:
# #         schedule.run_pending()
# #         time.sleep(1)
