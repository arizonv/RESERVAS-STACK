from flask import render_template
from flask import request
import traceback
import os
import requests
from urllib.parse import urlparse

def app_transbank_pay_view(app):
    # Valores por defecto
    API_REST_HOST = 'localhost'
    API_REST_PORT = '5000'

    @app.route('/transbank-pay', methods=['GET', 'POST'])
    def transbank_pay_view():
        print('METHOD', request.method)

        if request.method == 'GET':

            buy_order = '10029393040405'
            amount = 250000
            context = {
                'buy_order': buy_order,
                'amount': amount
            }
            return render_template('transbank-pay.html', context=context)



        elif request.method == 'POST':

            buy_order = request.form.get('buy-order')
            session_id = 12345786
            amount = request.form.get('amount')
            return_url = 'http://{0}:{1}/commit-pay'.format(host, port)

            body = {
                "buy_order": buy_order,
                "session_id": session_id,
                "amount": amount,
                "return_url": return_url
            }
          

            url = 'http://webpay3gint.transbank.cl/api/v1/transbank/transaction/create'
            response = requests.post(url, json=body)
            json_response = response.json()

            if response.status_code == 200:
                context = {
                    'amount': amount,
                    'transbank': json_response
                }
                return render_template('send-pay.html', context=context)
            else:
                return render_template('ERROR TRANSBANK CREATE TRANSACTION')
