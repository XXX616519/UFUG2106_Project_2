import random
import math
from typing import Tuple, Optional

class RSAKeyGenerator:
    @staticmethod
    def generate_keypair(
        bit_length: int = 2048,
        p: Optional[int] = None,
        q: Optional[int] = None
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        生成RSA密钥对(支持自定义p和q)
        Generate RSA key pair (with custom p/q support)
        
        :param bit_length: 目标模数位数/target modulus bit length
        :param p: 可选的自定义素数p/optional custom prime p
        :param q: 可选的自定义素数q/optional custom prime q
        :return: (公钥, 私钥)/(public key, private key)
        
        参数校验规则/Validation rules:
        1. p和q必须同时提供或都不提供/p and q must be both provided or omitted
        2. 自定义素数必须通过素性检测/custom primes must pass primality test
        3. 素数长度需符合要求/prime length must match requirements
        4. 生成的模数需符合目标长度/generated modulus must match target length
        5. e必须与phi(n)互质/e must be coprime with phi(n)
        """
        # 参数共存性检查/Co-existence check
        if (p is None) != (q is None):
            raise ValueError("必须同时提供p和q或都不提供/p and q must be both provided or omitted")

        # 处理自定义素数的情况/Custom primes handling
        if p is not None and q is not None:
            # 素性检测/Primality check
            if not RSAKeyGenerator._is_prime(p):
                raise ValueError("p必须是素数/p must be prime")
            if not RSAKeyGenerator._is_prime(q):
                raise ValueError("q必须是素数/q must be prime")
            
            # 唯一性检查/Uniqueness check
            if p == q:
                raise ValueError("p和q必须不同/p and q must be distinct")
            
            # 长度验证/Length validation
            target_bits = bit_length // 2
            allowed_range = range(target_bits-2, target_bits+3)  # 允许±2位误差/allow ±2 bits tolerance
            if p.bit_length() not in allowed_range or q.bit_length() not in allowed_range:
                raise ValueError(
                    f"素数位数需接近{target_bits}位/"
                    f"Prime bits should be near {target_bits} bits\n"
                    f"实际位数(p): {p.bit_length()}, (q): {q.bit_length()}"
                )
            
            # 计算模数/Calculate modulus
            n = p * q
            if n.bit_length() != bit_length:
                raise ValueError(
                    f"模数位数不符/Invalid modulus bit length\n"
                    f"预期/Expected: {bit_length}, 实际/Actual: {n.bit_length()}"
                )

        # 自动生成素数/Auto-generate primes
        else:
            if bit_length < 2048:
                raise ValueError("密钥长度必须至少为2048位/Key length must be at least 2048 bits")
            
            target_bits = bit_length // 2
            p = RSAKeyGenerator._generate_prime(target_bits)
            q = RSAKeyGenerator._generate_prime(target_bits)
            while p == q:
                q = RSAKeyGenerator._generate_prime(target_bits)
            n = p * q

        # 计算欧拉函数/Calculate Euler's totient
        phi = (p - 1) * (q - 1)
        
        # 设置公共指数并验证/Set and validate public exponent
        e = 65537
        if math.gcd(e, phi) != 1:
            if p is not None:  # 用户提供了自定义素数时抛出错误/Error for custom primes
                raise ValueError("e与phi(n)不互质/e and phi(n) are not coprime")
            return RSAKeyGenerator.generate_keypair(bit_length)  # 递归重新生成/Recursively regenerate
        
        # 计算私钥指数/Calculate private exponent
        d = pow(e, -1, phi)
        
        # 安全清理内存/Secure memory cleanup
        p = q = phi = 0  
        
        return ((e, n), (d, n))

    @staticmethod
    def _generate_prime(bit_length: int) -> int:
        """
        生成指定位数的素数
        Generate prime number with specified bit length
        
        :param bit_length: 目标位数/target bit length
        :return: 生成的素数/generated prime number
        """
        while True:
            # 生成候选数（确保奇数和正确位数）
            # Generate candidate (ensure odd and correct bit length)
            candidate = random.getrandbits(bit_length)
            candidate |= (1 << (bit_length - 1)) | 1
            if RSAKeyGenerator._is_prime(candidate):
                return candidate

    @staticmethod
    def _is_prime(n: int, k: int = 128) -> bool:
        """
        增强型Miller-Rabin素性检测
        Enhanced Miller-Rabin primality test
        
        :param n: 待检测的数/number to test
        :param k: 检测轮数/number of test rounds
        :return: 是否为素数/boolean indicating primality
        """
        if n <= 1:
            return False
        
        # 快速检查小素数/Quick check for small primes
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
            if n % p == 0:
                return n == p
        
        # 分解n-1为d*2^s/Write n-1 as d*2^s
        d, s = n - 1, 0
        while d % 2 == 0:
            d //= 2
            s += 1
        
        # 进行k轮检测/Perform k rounds of testing
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for __ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

class RSA:
    """RSA加密解密类/RSA Encryption/Decryption Class"""
    def __init__(self, public_key: Tuple[int, int], private_key: Optional[Tuple[int, int]] = None):
        """
        初始化RSA实例
        Initialize RSA instance
        
        :param public_key: 公钥(e, n)/public key (e, n)
        :param private_key: 私钥(d, n)/private key (d, n) (optional)
        """
        self.e, self.n = self._validate_key(public_key)
        self.d = private_key[0] if private_key else None
        
        # 验证私钥有效性/Validate private key if provided
        if private_key:
            if private_key[1] != self.n:
                raise ValueError("私钥与公钥不匹配/Private key doesn't match public key")
            if not (0 < private_key[0] < self.n):
                raise ValueError("无效的私钥/Invalid private key")

    @staticmethod
    def _validate_key(key: Tuple[int, int]) -> Tuple[int, int]:
        """
        验证密钥格式有效性
        Validate key format
        
        :param key: 待验证的密钥/key to validate
        :return: 验证后的密钥/validated key
        """
        if len(key) != 2:
            raise ValueError("密钥应为(e, n)或(d, n)格式/Key should be in (e/d, n) format")
        e_or_d, n = key
        if n <= 0:
            raise ValueError("模数n必须为正整数/Modulus n must be positive integer")
        if e_or_d <= 0:
            raise ValueError("指数必须为正整数/Exponent must be positive integer")
        return e_or_d, n

    def encrypt(self, plaintext: bytes) -> int:
        """
        使用公钥加密数据
        Encrypt data with public key
        
        :param plaintext: 明文字节数据/plaintext bytes
        :return: 加密后的整数密文/encrypted integer ciphertext
        
        实现步骤/Implementation steps:
        1. 类型检查/Type checking
        2. 字节转整数/Convert bytes to integer
        3. 明文范围验证/Plaintext range validation
        4. 模幂运算加密/Modular exponentiation encryption
        """
        if not isinstance(plaintext, bytes):
            raise TypeError("明文必须是字节串/Plaintext must be bytes")

        plain_int = int.from_bytes(plaintext, byteorder='big')
        
        if plain_int >= self.n:
            raise ValueError(f"明文过大，最大允许值为{self.n-1}/Plaintext too large, max allowed is {self.n-1}")

        return pow(plain_int, self.e, self.n)

    def decrypt(self, ciphertext: int) -> bytes:
        """
        使用私钥解密数据
        Decrypt data with private key
        
        :param ciphertext: 整数密文/integer ciphertext
        :return: 解密后的字节数据/decrypted bytes
        
        实现步骤/Implementation steps:
        1. 私钥可用性检查/Private key availability check
        2. 类型检查/Type checking
        3. 密文范围验证/Ciphertext range validation
        4. 模幂运算解密/Modular exponentiation decryption
        5. 整数转字节转换/Convert integer to bytes
        """
        if not self.d:
            raise RuntimeError("未提供私钥，无法解密/No private key provided for decryption")

        if not isinstance(ciphertext, int):
            raise TypeError("密文必须是整数/Ciphertext must be integer")
        
        if ciphertext >= self.n:
            raise ValueError(f"密文过大，最大允许值为{self.n-1}/Ciphertext too large, max allowed is {self.n-1}")

        plain_int = pow(ciphertext, self.d, self.n)
        byte_length = (self.n.bit_length() + 7) // 8
        return plain_int.to_bytes(byte_length, byteorder='big')

    @classmethod
    def create_keypair(cls, bit_length: int = 2048) -> Tuple['RSA', 'RSA']:
        """
        创建配对的RSA实例
        Create paired RSA instances
        
        :param bit_length: 密钥长度/key length
        :return: (公钥实例，私钥实例)/(public key instance, private key instance)
        """
        public_key, private_key = RSAKeyGenerator.generate_keypair(bit_length)
        return (
            cls(public_key=public_key),
            cls(public_key=public_key, private_key=private_key)
        )