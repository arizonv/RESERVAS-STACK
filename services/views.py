from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cancha,TipoCancha,Agenda
from client.models import Reserva
from django.utils import timezone
from client.models import Cliente

from django.contrib import messages
from django.shortcuts import redirect

from django.utils import timezone



class CanchaListView(ListView):
    model = Cancha
    template_name = 'servicios/listar.html'
    context_object_name = 'servicios'


class CanchaCreateView(CreateView):
    model = Cancha
    template_name = 'servicios/agregar.html'
    fields = '__all__'
    # form_class = ServicioForm

class CanchaUpdateView(UpdateView):
    model = Cancha
    template_name = 'servicios/actualizar.html'
    fields = '__all__'
    context_object_name = 'servicio'


class CanchaDeleteView(DeleteView):
    model = Cancha
    success_url = reverse_lazy('servicio-listar')

############# tipo ##############################

class TipoCanchaListView(ListView):
    model = TipoCancha
    template_name = 'servicios/tipo/listar.html'
    context_object_name = 'TipoCancha'


class TipoCanchaCreateView(CreateView):
    model = TipoCancha
    template_name = 'servicios/tipo/agregar.html'
    fields = '__all__'
    # form_class = ServicioForm

class TipoCanchaUpdateView(UpdateView):
    model = TipoCancha
    template_name = 'servicios/tipo/actualizar.html'
    fields = '__all__'
    context_object_name = 'TipoCancha'


class TipoCanchaDeleteView(DeleteView):
    model = TipoCancha
    success_url = reverse_lazy('TipoCancha-listar')


############# agenda ############################
class AgendaListView(ListView):
    model = TipoCancha
    template_name = 'agendas/listar.html'
    context_object_name = 'tipos_cancha'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('Login:login')

        try:
            cliente = request.user.cliente
        except Cliente.DoesNotExist:
            messages.warning(request, 'Necesitas los DATOS COMPLEMENTARIOS para realizar una reserva')
            return redirect('client:cliente_create')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        agendas_por_cancha = {}

        current_date = timezone.now().date()

        for tipo in context['tipos_cancha']:
            canchas = Cancha.objects.filter(tipo=tipo)
            agendas_por_cancha[tipo] = {}

            for cancha in canchas:
                agendas = Agenda.objects.filter(cancha=cancha, disponible=True)
                agendas_por_cancha[tipo][cancha] = agendas

        context['agendas_por_cancha'] = agendas_por_cancha

        return context






