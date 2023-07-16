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

import requests
from django.conf import settings
import random
import string



#cliente
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/listar.html', {'clientes': clientes})


@login_required(login_url='login:login')
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
                return redirect('servicio:agenda-reserva')
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
            return redirect('cliente:cliente_list')
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



@login_required(login_url='login')
def listar_reservas_usuario(request):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.warning(request, 'Necesitas crear un Cliente para acceder a esta página')
        return redirect(reverse('cliente:cliente_create'))

    reservas = Reserva.objects.filter(cliente=cliente)
    return render(request, 'reserva/reservas_usuario.html', {'reservas': reservas})


@login_required(login_url='login')
def crear_reserva(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    form = ReservaForm(initial={'agenda': agenda})

    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.warning(request, 'Necesitas los DATOS COMPLEMENTARIOS para realizar una reserva')
        return redirect(to='cliente:cliente_create')

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.agenda = agenda
            reserva.cliente = cliente
            if Reserva.objects.filter(agenda=agenda, dia=reserva.dia).exists():
                messages.error(request, 'La fecha ya está reservada.')
            else:
                reserva_session = request.session['reserva'] = reserva
                print(f'reserva actual: {reserva_session}')

                BASE_URL=  'http://127.0.0.1:8000/'
                # Construir la URL de retorno
                return_url = f"{BASE_URL}cliente/confirm-transaction/"

                # Lógica para crear una transacción en Transbank
                url = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions'
                headers = {
                    'Tbk-Api-Key-Id': '597055555532',
                    'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
                    'Content-Type': 'application/json'
                }

                # Generar un número de orden de compra aleatorio único de 15 dígitos
                digits = string.digits
                buy_order = "00-" + ''.join(random.choice(digits) for _ in range(13))

                session_id = str(request.session.session_key)  # ID de sesión actual
                amount = agenda.cancha.tipo.precio/2  # Precio de la cancha

                data = {
                    "buy_order": buy_order,
                    "session_id": session_id,
                    "amount": int(amount),
                    "return_url": return_url
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

