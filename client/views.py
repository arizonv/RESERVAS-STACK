from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Reserva, Agenda
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservaForm
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm

#cliente

def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/listar.html', {'clientes': clientes})


@login_required(login_url='login')
def crear_cliente(request):
    cliente_existente = Cliente.objects.filter(user=request.user).first()  # Verificar si existe un cliente para el usuario actual

    if cliente_existente:  # Si el cliente existe, rellenar los datos en el formulario
        form = ClienteForm(instance=cliente_existente)
    else:
        form = ClienteForm()

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente_existente)  # Pasar la instancia existente al formulario en caso de edición

        try:
            if form.is_valid():
                cliente = form.save(commit=False)
                cliente.user = request.user
                cliente.save()
                return redirect('agendas:tipo_cancha_listar')
        except Exception as e:
            error_message = str(e)
            form.add_error(None, error_message)

    return render(request, 'cliente/agregar.html', {'form': form})



def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('client:cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente/modificar.html', {'form': form})



def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente deleted successfully.')
        return redirect(to='cliente_list')
    else:
        messages.warning(request, 'Invalid request.')
        return redirect(to='cliente_list')



#reservas
def reserva_list(request):
    reservas = Reserva.objects.all()
    return render(request, 'reserva/listar.html', {'reservas': reservas})


from django.urls import reverse

@login_required(login_url='login')
def listar_reservas_usuario(request):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.warning(request, 'Necesitas crear un Cliente para acceder a esta página')
        return redirect(reverse('client:cliente_create'))

    reservas = Reserva.objects.filter(cliente=cliente)
    return render(request, 'reserva/listar_reservas_usuario.html', {'reservas': reservas})



# @login_required(login_url='login')
# def crear_reserva(request, agenda_id):
#     agenda = get_object_or_404(Agenda, id=agenda_id)
#     form = ReservaForm(initial={'agenda': agenda})

#     try:
#         cliente = request.user.cliente
#     except Cliente.DoesNotExist:
#         messages.warning(request, 'Necesitas los DATOS COMPLEMENTARIOS para realizar una reserva')
#         return redirect(to='client:cliente_create')

#     if request.method == 'POST':
#         form = ReservaForm(request.POST)
#         if form.is_valid():
#             reserva = form.save(commit=False)
#             reserva.agenda = agenda
#             reserva.cliente = cliente
#             # Check if a reservation already exists for the agenda and selected date
#             if Reserva.objects.filter(agenda=agenda, dia=reserva.dia).exists():
#                 messages.error(request, 'La fecha ya está reservada.')
#             else:
#                 reserva.save()
#                 messages.success(request, 'Reserva Exitosa!')
#                 return redirect(to='home')

#     dias_reservados = Reserva.objects.filter(agenda__cancha=agenda.cancha, agenda__horario=agenda.horario).values_list('dia', flat=True)
#     dias_reservados_str = ', '.join([dia.strftime('%d/%m/%Y') for dia in dias_reservados])
#     dias_reservados_json = json.dumps(dias_reservados_str)

#     contexto = {
#         'form': form,
#         'agenda': agenda,
#         'dias_reservados_json': dias_reservados_json,
#     }
#     return render(request, 'reserva/crear.html', contexto)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import requests

@login_required(login_url='login')
def crear_reserva(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    form = ReservaForm(initial={'agenda': agenda})

    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.warning(request, 'Necesitas los DATOS COMPLEMENTARIOS para realizar una reserva')
        return redirect(to='client:cliente_create')

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.agenda = agenda
            reserva.cliente = cliente
            if Reserva.objects.filter(agenda=agenda, dia=reserva.dia).exists():
                messages.error(request, 'La fecha ya está reservada.')
            else:
                reserva.save()
                messages.success(request, 'Reserva Exitosa!')

                # Lógica para crear una transacción en Transbank
                url = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions'
                headers = {
                    'Tbk-Api-Key-Id': '597055555532',
                    'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
                    'Content-Type': 'application/json'
                }

                # Obtener datos de la reserva
                buy_order = '00-' + str(reserva.id).zfill(8) # ID de la reserva
                session_id = str(request.session.session_key)  # ID de sesión actual
                amount = agenda.cancha.tipo.precio/2  # Precio de la cancha

                data = {
                    "buy_order": buy_order,
                    "session_id": session_id,
                    "amount": int(amount),
                    "return_url": "http://www.comercio.cl/webpay/retorno"
                }

                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    transaction_data = response.json()
                    print(transaction_data)
                    return render(request, 'reserva/crear.html', {'transaction_data': transaction_data})
                else:
                    return render(request, 'transbank/error.html')


    dias_reservados = Reserva.objects.filter(agenda__cancha=agenda.cancha, agenda__horario=agenda.horario).values_list('dia', flat=True)
    dias_reservados_str = ', '.join([dia.strftime('%d/%m/%Y') for dia in dias_reservados])
    dias_reservados_json = json.dumps(dias_reservados_str)

    contexto = {
        'form': form,
        'agenda': agenda,
        'dias_reservados_json': dias_reservados_json,
    }
    return render(request, 'reserva/crear.html', contexto)

