from django.urls import path
from .views import CanchaListView, CanchaCreateView, CanchaUpdateView, CanchaDeleteView,AgendaListView,TipoCanchaListView

app_name = 'agendas'

urlpatterns = [
    path('c/listar/', CanchaListView.as_view(), name='cancha-listar'),
    path('c/agregar/', CanchaCreateView.as_view(), name='cancha-crear'),
    path('c/actualizar/<int:pk>/', CanchaUpdateView.as_view(), name='cancha-actualizar'),
    path('c/eliminar/<int:pk>/', CanchaDeleteView.as_view(), name='cancha-eliminar'),


    path('a/tipos/', TipoCanchaListView.as_view(), name='tipo_cancha_listar'),
    path('a/listar/', AgendaListView.as_view(), name='agenda-listar'),
    
]
