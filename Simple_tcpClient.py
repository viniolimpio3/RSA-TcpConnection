from socket import *
from RSA import RSA
import json

serverName = "10.1.70.16"
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

# Receber chave pública do servidor
server_public_key_data = clientSocket.recv(65000)
server_public_key = tuple(json.loads(server_public_key_data.decode('utf-8')))

print(f"Chave pública recebida do servidor: {server_public_key}")

print("Gerando chaves RSA do cliente...")
rsa = RSA()
client_public_key, private_key = rsa.generate_keypair(4096)

# Enviar chave pública para o servidor
client_public_key_data = json.dumps(client_public_key).encode('utf-8')
clientSocket.send(client_public_key_data)

# Obter mensagem do usuário
sentence = input("Digite a mensagem em minúsculas: ")

# Criptografar mensagem com a chave pública
encrypted_message = RSA.encrypt(sentence, server_public_key)
print(f"Mensagem criptografada: {encrypted_message}")

# Enviar mensagem criptografada
clientSocket.send(str(encrypted_message).encode('utf-8'))

# Receber resposta criptografada do servidor
encrypted_data = clientSocket.recv(65000)
encrypted_message = int(encrypted_data.decode('utf-8'))

print(f"Mensagem criptografada recebida: {encrypted_message}")

# Descriptografar mensagem

decrypted_int = RSA.decrypt(encrypted_message, private_key)
decrypted_message = RSA.int_to_string(decrypted_int)

print("Resposta do servidor:", decrypted_message)
clientSocket.close()