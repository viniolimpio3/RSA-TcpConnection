from socket import *
from RSA import RSA
import json

serverName = "127.0.0.1"
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

# Receber chave pública do servidor
public_key_data = clientSocket.recv(65000)
public_key = tuple(json.loads(public_key_data.decode('utf-8')))

print(f"Chave pública recebida do servidor: {public_key}")

# Obter mensagem do usuário
sentence = input("Digite a mensagem em minúsculas: ")

# Criptografar mensagem com a chave pública
encrypted_message = RSA.encrypt(sentence, public_key)
print(f"Mensagem criptografada: {encrypted_message}")

# Enviar mensagem criptografada
clientSocket.send(str(encrypted_message).encode('utf-8'))

# Receber resposta em texto claro
response_data = clientSocket.recv(65000)
response = response_data.decode('utf-8')

print("Resposta do servidor:", response)
clientSocket.close()