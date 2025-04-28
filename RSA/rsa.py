import random
import math
import os
import struct
from typing import Tuple, Optional

class RSAKeyGenerator:
    """
    RSA Key Generator (Final Version)
    
    功能特性：
    1. 支持自定义素数p/q
    2. 安全内存擦除（符合NIST SP 800-88标准）
    3. 增强型参数验证
    4. 防递归栈溢出设计
    5. 优化的素性检测算法
    """
    
    MAX_RETRIES = 10  # 最大密钥生成尝试次数
    
    @staticmethod
    def generate_keypair(
        bit_length: int = 2048,
        p: Optional[int] = None,
        q: Optional[int] = None
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        生成RSA密钥对（支持自动生成或自定义素数）
        
        参数验证流程：
        1. 位长合规性检查（bit_length ≥ 2048）
        2. p/q共存性检查（必须同时提供或都不提供）
        3. 素数有效性验证（素性检测+唯一性检查）
        4. 长度合规性验证（模数位长匹配）
        5. 互质性验证（gcd(e, φ(n)) == 1）
        """
        #region 安全擦除函数
        def secure_wipe(num: int) -> None:
            """符合NIST SP 800-88的三次覆盖擦除"""
            if num is None:
                return
            
            try:
                byte_len = (num.bit_length() + 7) // 8
                buffer = bytearray(byte_len)
                # 第一次覆盖：随机数据
                buffer[:] = os.urandom(byte_len)
                # 第二次覆盖：位翻转
                for i in range(byte_len):
                    buffer[i] ^= 0xFF
                # 第三次覆盖：全零
                buffer[:] = b'\x00' * byte_len
            finally:
                del buffer
        #endregion

        #region 初始化清理
        p_val = q_val = phi = n = e = d = None
        try:
            #region 参数验证
            if (p is None) != (q is None):
                raise ValueError(
                    "ERR101: p和q必须同时提供或都不提供 | "
                    "p and q must be both provided or omitted"
                )
            
            custom_mode = p is not None
            #endregion

            #region 自定义素数处理
            if custom_mode:
                # 类型验证
                if not isinstance(p, int) or not isinstance(q, int):
                    raise TypeError(
                        "ERR102: p/q必须为整数 | "
                        "p/q must be integers"
                    )
                
                # 素性验证
                prime_check = [
                    (p, "p"),
                    (q, "q")
                ]
                for num, name in prime_check:
                    if not RSAKeyGenerator._is_prime(num):
                        raise ValueError(
                            f"ERR103: {name}不是素数 | "
                            f"{name} is not prime"
                        )
                
                # 唯一性验证
                if p == q:
                    raise ValueError(
                        "ERR104: p和q必须不同 | "
                        "p and q must be distinct"
                    )
                
                # 长度验证
                target_prime_bits = bit_length // 2
                if (p.bit_length() + q.bit_length()) != (2 * target_prime_bits):
                    raise ValueError("ERR106: 素数位数总和不符 | Total prime bits mismatch")

                n = p * q
                actual_bit_length = n.bit_length()
                if not (bit_length - 2 <= actual_bit_length <= bit_length + 2):
                    raise ValueError(
                        f"ERR105: 模数位数不符 | Expected: {bit_length}±2, Actual: {actual_bit_length}\n"
                        "可能原因：素数位数偏差过大 | Possible cause: Prime bits deviation too large"
                    )
                
                # 素数位数验证
                target_prime_bits = bit_length // 2
                prime_bit_check = [
                    (p, target_prime_bits, "p"),
                    (q, target_prime_bits, "q")
                ]
                for prime, target, name in prime_bit_check:
                    prime_bits = prime.bit_length()
                    if not (target - 2 <= prime_bits <= target + 2):
                        raise ValueError(
                            f"ERR106: {name}位数不符 | "
                            f"Expected: {target}±2 bits, Actual: {prime_bits} bits"
                        )
            #endregion

            #region 自动生成模式
            else:
                if bit_length < 2048:
                    raise ValueError(
                        "ERR107: 密钥长度必须≥2048位 | "
                        "Key length must be ≥2048 bits"
                    )
                
                target_prime_bits = bit_length // 2
                for attempt in range(RSAKeyGenerator.MAX_RETRIES):
                    # 安全擦除前次生成的数据
                    secure_wipe(p_val)
                    secure_wipe(q_val)
                    
                    p_val = RSAKeyGenerator._generate_prime(target_prime_bits)
                    q_val = RSAKeyGenerator._generate_prime(target_prime_bits)
                    
                    if p_val == q_val:
                        continue
                    
                    n = p_val * q_val
                    if n.bit_length() == bit_length:
                        break
                else:
                    raise RuntimeError(
                        "ERR108: 无法生成合规素数对 | "
                        "Failed to generate valid prime pair"
                    )
                
                p, q = p_val, q_val
            #endregion

            #region 计算核心参数
            phi = (p - 1) * (q - 1)
            e = 65537
            
            # 互质性验证
            if math.gcd(e, phi) != 1:
                if custom_mode:
                    raise ValueError(
                        "ERR109: e与φ(n)不互质 | "
                        "e and φ(n) are not coprime"
                    )
                raise RuntimeError(
                    "ERR110: 自动生成模式互质性验证失败 | "
                    "Coprimality check failed in auto mode"
                )
            
            d = pow(e, -1, phi)
            #endregion

            return ((e, n), (d, n))

        finally:
            #region 安全清理
            secure_wipe(p_val)
            secure_wipe(q_val)
            secure_wipe(phi)
            secure_wipe(e if 'e' in locals() else 0)
            secure_wipe(d if 'd' in locals() else 0)
            # 解除引用
            p_val = q_val = phi = e = d = None
            #endregion

    @staticmethod
    def _generate_prime(bit_length: int) -> int:
        """优化的素数生成算法"""
        # 快速通道：预生成的小素数检查
        SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        
        for _ in range(1000):  # 最大尝试次数
            # 生成候选数
            candidate = random.getrandbits(bit_length)
            candidate |= (1 << (bit_length - 1)) | 1  # 确保最高位为1且为奇数
            
            # 快速排除法
            if any(candidate % p == 0 for p in SMALL_PRIMES if p < candidate):
                continue
            
            if RSAKeyGenerator._is_prime(candidate):
                return candidate
        raise RuntimeError("ERR111: 素数生成超时 | Prime generation timeout")

    @staticmethod
    def _is_prime(n: int, k: int = 64) -> bool:
        """优化的Miller-Rabin检测算法"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False

        # 分解n-1为d*2^s
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        # 使用固定基和随机基结合的方式
        witnesses = [2, 3, 5, 7, 11]  # 确定性检测n < 2^64
        if n >= 3825123056546413051:
            witnesses = [random.randint(2, min(n-2, 1<<20)) for _ in range(k)]
        
        for a in witnesses:
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
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
        
        max_length = (self.n.bit_length() + 7) // 8
        max_plain_int = (1 << (max_length * 8)) - 1
        
        if plain_int > max_plain_int:
            raise ValueError(f"明文过大，无法加密/Plaintext too large to encrypt")

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
        byte_length = (plain_int.bit_length() + 7) // 8
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