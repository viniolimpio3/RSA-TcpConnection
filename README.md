# RSA-TcpConnection

Um projeto que implementa comunicação TCP segura usando criptografia RSA em Python. O sistema permite troca de mensagens criptografadas entre cliente e servidor usando chaves RSA geradas dinamicamente.

## 📋 Descrição

Este projeto demonstra a implementação de um protocolo de comunicação segura entre cliente e servidor TCP, onde:

- O **servidor** processa mensagens (converte para maiúsculas)
- Toda comunicação é **criptografada usando RSA**
- Ambos cliente e servidor geram seus próprios **pares de chaves RSA**
- As **chaves públicas são trocadas** no início da comunicação
- Mensagens são criptografadas com a chave pública do destinatário

## 🏗️ Arquitetura do Sistema

```
Cliente                                    Servidor
   |                                          |
   |-------- Conexão TCP (porta 12345) -------|
   |                                          |
   |<----- Chave Pública do Servidor ---------|
   |                                          |
   |------ Chave Pública do Cliente --------->|
   |                                          |
   |----- Mensagem Criptografada (RSA) ------>|
   |                                          | (Descriptografa e processa)
   |<---- Resposta Criptografada (RSA) -------|
   |                                          |
```

## 🔧 Componentes

### 1. RSA.py
Implementa a classe `RSA` com funcionalidades completas de criptografia:

- **Geração de números primos** (Teste de Miller-Rabin)
- **Geração de pares de chaves** RSA
- **Criptografia e descriptografia** de mensagens
- **Funções auxiliares** (MDC, inverso modular, etc.)

#### Teste de Primalidade:
O algoritmo de teste de primalidade Miller-Rabin foi implementado por **Fábio Cabrini (2025)** com:
- Estrutura procedural simples
- Entrada/saída padronizadas e medição de tempo
- Valor de teste padrão (Enter): `282739948845173`

#### Principais métodos:
```python
RSA()                           # Construtor com geração automática de chaves
generate_keypair(keysize)       # Gera par de chaves RSA
encrypt(message, public_key)    # Criptografa mensagem
decrypt(ciphertext, private_key) # Descriptografa mensagem
```

### 2. Simple_tcpServer.py
Servidor TCP que:

- **Gera chaves RSA** de 4096 bits na inicialização
- **Aceita conexões** na porta 12345
- **Troca chaves públicas** com o cliente
- **Recebe mensagens criptografadas** e descriptografa
- **Processa** mensagens (conversão para maiúsculas)
- **Envia respostas criptografadas** de volta

### 3. Simple_tcpClient.py
Cliente TCP que:

- **Conecta-se ao servidor** (IP configurável)
- **Gera suas próprias chaves RSA** de 4096 bits
- **Troca chaves públicas** com o servidor
- **Criptografa mensagens** do usuário
- **Recebe e descriptografa** respostas do servidor

## 🚀 Como Executar

### Pré-requisitos
- Python 3.6 ou superior
- Módulos: `socket`, `random`, `json` (incluídos no Python)

### Passo 1: Executar o Servidor
```bash
python Simple_tcpServer.py
```

**Saída esperada:**
```
Gerando chaves RSA...
Gerando chaves RSA de 4096 bits...
p = [número primo grande]
q = [número primo grande]
n = p * q = [produto]
φ(n) = [phi de n]
e = 65537
d = [chave privada]
TCP Server com RSA

Chave pública: (65537, [número grande])
```

### Passo 2: Executar o Cliente
```bash
python Simple_tcpClient.py
```

**Fluxo de execução:**
1. Cliente se conecta ao servidor
2. Recebe chave pública do servidor
3. Gera suas próprias chaves RSA
4. Envia sua chave pública para o servidor
5. Solicita mensagem do usuário
6. Criptografa e envia mensagem
7. Recebe e descriptografa resposta

## 🔒 Segurança

### Características de Segurança:
- **Chaves RSA de 4096 bits** para alta segurança
- **Troca segura de chaves públicas** no início da comunicação
- **Criptografia bidirecional** - ambas as direções são protegidas
- **Geração de números primos** usando teste de Miller-Rabin
- **Chaves únicas** geradas a cada execução

### Algoritmos Implementados:
- **Teste de Primalidade:** Miller-Rabin (Autor: Fábio Cabrini - 2025)
  - Estrutura procedural simples, entrada/saída padronizadas e medição de tempo
  - Valor de teste padrão: 282739948845173
- **Geração de Primos:** Método probabilístico
- **MDC:** Algoritmo de Euclides
- **Inverso Modular:** Algoritmo de Euclides Estendido
- **Criptografia:** RSA com exponente público 65537

## ⚙️ Configuração

### Parâmetros Configuráveis:

**No servidor (`Simple_tcpServer.py`):**
```python
serverPort = 12345          # Porta do servidor
keysize = 4096             # Tamanho das chaves RSA em bits
```

**No cliente (`Simple_tcpClient.py`):**
```python
serverName = "10.1.70.16"  # IP do servidor
serverPort = 12345         # Porta do servidor
keysize = 4096            # Tamanho das chaves RSA em bits
```

## 🔍 Exemplo de Uso

### Terminal do Servidor:
```
PS C:\Users\...\Tcp-RSA> python Simple_tcpServer.py
Gerando chaves RSA...
Gerando chaves RSA de 4096 bits...
[... geração de chaves ...]
TCP Server com RSA

Chave pública: (65537, 123456789...)
Mensagem criptografada recebida: 987654321...
Mensagem descriptografada do cliente: hello world
Mensagem processada: HELLO WORLD
Resposta criptografada: 456789123...
Resposta enviada para o cliente
```

### Terminal do Cliente:
```
PS C:\Users\...\Tcp-RSA> python Simple_tcpClient.py
Chave pública recebida do servidor: (65537, 123456789...)
Gerando chaves RSA do cliente...
[... geração de chaves ...]
Digite a mensagem em minúsculas: hello world
Mensagem criptografada: 987654321...
Mensagem criptografada recebida: 456789123...
Resposta do servidor: HELLO WORLD
```

## 🛠️ Possíveis Melhorias

1. **Autenticação de Chaves:** Implementar certificados digitais
2. **Múltiplos Clientes:** Suporte a conexões simultâneas
3. **Persistent Connections:** Manter conexões abertas para múltiplas mensagens
4. **Logging:** Sistema de logs detalhado
5. **Interface Gráfica:** GUI para facilitar o uso
6. **Protocolo Híbrido:** Combinar RSA com criptografia simétrica (AES)

## 📝 Notas Técnicas

- **Limitação de Tamanho:** Mensagens devem ser menores que o módulo RSA
- **Performance:** Chaves de 4096 bits podem ser lentas em hardware antigo
- **Segurança:** Para produção, considere usar bibliotecas criptográficas estabelecidas
- **Rede:** Configure firewalls para permitir comunicação na porta escolhida

## 👥 Autor

Projeto desenvolvido como demonstração de criptografia RSA em comunicação TCP.

### Créditos:
- **Algoritmo de Teste de Primalidade Miller-Rabin:** Fábio Cabrini (2025)
  - Implementação com estrutura procedural simples
  - Entrada/saída padronizadas e medição de tempo
  - Valor de teste padrão: 282739948845173

## 📄 Licença

Este projeto é de uso educacional e demonstrativo.