import requests
import urllib3

# Desativar avisos de InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def validar_telefones_em_lote(numeros):
    try:
        instancia = '3CF688310DEA207A60B22A268ACD4084'  # ID da instância
        token = '44FCAA7CF3124A1CA04018F0'  # Token da instância
        url = f'https://api.z-api.io/instances/{instancia}/token/{token}/phone-exists-batch'
        
        headers = {
            'Content-Type': 'application/json',
            'client-token': 'Fd4a3fc33f81a4de6a91a66d264f3c730S'  # Token de segurança da conta
        }
        data = {
            'phones': numeros
        }
        
        print(f"Enviando requisição para {url} com os dados: {data}")
        
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()  # Levantar exceções para status de erro HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao validar telefones: {e}")
        if e.response:
            print(f"Resposta do servidor: {e.response.text}")
        return {'exists': False}
