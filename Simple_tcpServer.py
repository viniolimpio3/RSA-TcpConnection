from socket import *
from RSA import RSA
import json

serverPort = 12345
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(5)

# Gerar chaves RSA
print("Gerando chaves RSA...")
rsa = RSA()
server_public_key, private_key = rsa.generate_keypair(4096) 

print ("TCP Server com RSA\n")
print(f"Chave pública: {server_public_key}")

connectionSocket, addr = serverSocket.accept()

# Enviar chave pública para o cliente
server_public_key_data = json.dumps(server_public_key).encode('utf-8')
connectionSocket.send(server_public_key_data)

# Recebe a chave pública do cliente
client_public_key_data = connectionSocket.recv(65000)
client_public_key = tuple(json.loads(client_public_key_data.decode('utf-8')))

# Receber mensagem criptografada
encrypted_data = connectionSocket.recv(65000)
encrypted_message = int(encrypted_data.decode('utf-8'))

print(f"Mensagem criptografada recebida: {encrypted_message}")

# Descriptografar mensagem
decrypted_int = RSA.decrypt(encrypted_message, private_key)
decrypted_message = RSA.int_to_string(decrypted_int)

print("Mensagem descriptografada do cliente:", decrypted_message)

# Processar mensagem (converter para maiúscula)
processed_message = decrypted_message.upper()
print("Mensagem processada:", processed_message)

# Enviar resposta criptografada de volta ao cliente
encrypted_response = RSA.encrypt(processed_message, client_public_key)
print(f"Resposta criptografada: {encrypted_response}")
connectionSocket.send(str(encrypted_response).encode('utf-8'))

print("Resposta enviada para o cliente")
connectionSocket.close()
serverSocket.close()
