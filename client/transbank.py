from django.shortcuts import render
import requests

def create_transaction(request):
    # Lógica para crear una transacción en Transbank
    url = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions'
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json'
    }
    data = {
        "buy_order": "ordenCompra12345678",
        "session_id": "sesion1234557545",
        "amount": 10000,
        "return_url": "http://www.comercio.cl/webpay/retorno"
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        transaction_data = response.json()
        return render(request, 'transbank/payment.html', {'transaction_data': transaction_data})
    else:
        # Manejar el error en caso de que la transacción no se pueda crear
        return render(request, 'transbank/error.html')

def confirm_transaction(request, token):
    # Lógica para confirmar una transacción en Transbank
    url = f'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}'
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json'
    }
    
    response = requests.put(url, headers=headers)
    if response.status_code == 200:
        transaction_data = response.json()
        return render(request, 'transbank/confirmation.html', {'transaction_data': transaction_data})
    else:
        # Manejar el error en caso de que la transacción no se pueda confirmar
        return render(request, 'transbank/error.html')
