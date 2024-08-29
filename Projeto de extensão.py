import hashlib
import json
import requests  # type: ignore
import os
from cryptography.fernet import Fernet  # type: ignore

# Gerar uma chave de criptografia
def generate_key():
    return Fernet.generate_key()

# Salvar a chave em um arquivo
def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Carregar a chave de um arquivo
def load_key():
    if os.path.exists("secret.key"):
        return open("secret.key", "rb").read()
    else:
        raise FileNotFoundError("A chave de criptografia não foi encontrada. Certifique-se de gerá-la antes.")

# Função para criar hash do produto (certificação digital)
def generate_product_hash(product_data):
    product_json = json.dumps(product_data, sort_keys=True)
    return hashlib.sha256(product_json.encode()).hexdigest()

# Função para criptografar dados
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Função para descriptografar dados
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

# Função para rastrear entregas usando API dos Correios
def track_package(tracking_number):
    # Substitua pelo seu token de validação
    token = 'YOUR_API_TOKEN'
    url = f'https://api.correios.com.br/v1/track/{tracking_number}?token={token}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}

# Função principal para testar as funcionalidades
def main():
    # Gerar e salvar a chave
    key = generate_key()
    save_key(key)
    
    # Dados do produto
    product_data = {
        "id": "123456",
        "name": "Anel de Ouro",
        "price": 50000  # Considerando o valor em centavos
    }
    
    # Gerar hash do produto
    product_hash = generate_product_hash(product_data)
    print(f"Hash do produto: {product_hash}")
    
    # Criptografar dados do produto
    encrypted_data = encrypt_data(json.dumps(product_data), key)
    print(f"Dados criptografados: {encrypted_data}")
    
    # Descriptografar dados do produto
    decrypted_data = decrypt_data(encrypted_data, key)
    print(f"Dados descriptografados: {decrypted_data}")
    
    # Rastreamento de uma entrega
    tracking_number = "123456789"
    tracking_info = track_package(tracking_number)
    print(f"Informações de rastreamento: {tracking_info}")

if __name__ == "__main__":
    main()
