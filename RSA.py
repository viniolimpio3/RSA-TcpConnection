
import random

class RSA: 
    def __init__(self, p=None, q=None, e=65537):
        if p and q:
            self.p = p
            self.q = q
            self.n = p * q
            self.e = e
            self.phi = (p - 1) * (q - 1)
            self.d = pow(e, -1, self.phi)
        else:
            # Se p e q não forem fornecidos, gerar chaves automaticamente
            self.generate_keypair()

    @staticmethod
    def gcd(a, b):
        """Algoritmo de Euclides para calcular o MDC"""
        while b:
            a, b = b, a % b
        return a

    @classmethod
    def mod_inverse(cls, a, m):
        """Algoritmo de Euclides Estendido para calcular o inverso modular"""
        if cls.gcd(a, m) != 1:
            return None
        
        # Encontrar x tal que (a * x) % m = 1
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, x, _ = extended_gcd(a, m)
        return (x % m + m) % m

    @staticmethod
    def is_prime(n, k=5):
        if n < 2:
            return False
        # atalhos para pequenos primos / divisores
        small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        if n in small:
            return True
        for p in small:
            if n % p == 0:
                return False

        # escreve n-1 como d*2^s com d ímpar
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        def witness(a: int) -> bool:
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                return True
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    return True
            return False  # testemunha de composição

        # bases determinísticas para n < 2**64
        if n < (1 << 64):
            bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
        else:
            k = 12
            bases = [random.randrange(2, n - 2) for _ in range(k)]

        for a in bases:
            a %= n
            if a == 0:
                continue
            if not witness(a):
                return False
        return True
    @classmethod
    def generate_prime(cls, bits):
        """Gera um número primo com o número especificado de bits"""
        while True:
            # Gerar número ímpar aleatório
            n = random.getrandbits(bits)
            n |= (1 << bits - 1) | 1  # Garantir que tenha o número correto de bits e seja ímpar
            
            if cls.is_prime(n):
                return n

    def generate_keypair(self, keysize=4096):
        """Gera um par de chaves RSA"""
        print(f"Gerando chaves RSA de {keysize} bits...")
        
        # Passo 1: Gerar dois números primos grandes p e q
        self.p = self.generate_prime(keysize // 2)
        self.q = self.generate_prime(keysize // 2)
        
        print(f"p = {self.p}")
        print(f"q = {self.q}")
        
        # Passo 2: Calcular n = p * q
        self.n = self.p * self.q
        print(f"n = p * q = {self.n}")
        
        # Passo 3: Calcular φ(n) = (p-1)(q-1)
        self.phi = (self.p - 1) * (self.q - 1)
        print(f"φ(n) = {self.phi}")
        
        # Passo 4: Escolher e tal que 1 < e < φ(n) e gcd(e, φ(n)) = 1
        # Comumente usa-se e = 65537
        self.e = 65537
        if self.gcd(self.e, self.phi) != 1:
            # Se 65537 não for coprimo com phi, encontrar outro e
            self.e = 3
            while self.gcd(self.e, self.phi) != 1:
                self.e += 2
        
        print(f"e = {self.e}")
        
        # Passo 5: Calcular d tal que (d * e) % φ(n) = 1
        self.d = self.mod_inverse(self.e, self.phi)
        print(f"d = {self.d}")
        
        # Chave pública: (e, n)
        # Chave privada: (d, n)
        public_key = (self.e, self.n)
        private_key = (self.d, self.n)
        
        return public_key, private_key

    @staticmethod
    def encrypt(message, public_key):
        """Criptografa uma mensagem usando a chave pública"""
        e, n = public_key
        
        # Converter string para números
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
            message_int = int.from_bytes(message_bytes, 'big')
        else:
            message_int = message
        
        # Verificar se a mensagem não é maior que n
        if message_int >= n:
            raise ValueError("Mensagem muito grande para a chave fornecida")
        
        # Criptografar: c = m^e mod n
        ciphertext = pow(message_int, e, n)
        return ciphertext

    @staticmethod
    def decrypt(ciphertext, private_key):
        """Descriptografa uma mensagem usando a chave privada"""
        d, n = private_key
        
        # Descriptografar: m = c^d mod n
        message_int = pow(ciphertext, d, n)
        
        return message_int

    @staticmethod
    def int_to_string(message_int):
        """Converte inteiro de volta para string"""
        try:
            # Calcular o número de bytes necessários
            byte_length = (message_int.bit_length() + 7) // 8
            message_bytes = message_int.to_bytes(byte_length, 'big')
            return message_bytes.decode('utf-8')
        except:
            return str(message_int)
