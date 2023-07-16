from django.contrib import admin
from .models import Cliente, Reserva, Boleta

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'sexo')
    list_filter = ('sexo',)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'agenda', 'dia', 'confirmada')
    list_filter = ('confirmada', 'agenda__cancha__numeracion','agenda__cancha__tipo')  # Filtrar por numeración de cancha

class BoletaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'reserva', 'fecha')
    list_filter = ('fecha',)

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Boleta, BoletaAdmin)
