from django.urls import path
from .views import CanchaListView, CanchaCreateView, CanchaUpdateView, CanchaDeleteView,AgendaListView,TipoCanchaListView

app_name = 'agendas'

urlpatterns = [
    path('listar/', CanchaListView.as_view(), name='cancha-listar'),
    path('agregar/', CanchaCreateView.as_view(), name='cancha-crear'),
    path('actualizar/<int:pk>/', CanchaUpdateView.as_view(), name='cancha-actualizar'),
    path('eliminar/<int:pk>/', CanchaDeleteView.as_view(), name='cancha-eliminar'),
    path('agenda_reserva/', AgendaListView.as_view(), name='agenda-reserva'),
    
]
