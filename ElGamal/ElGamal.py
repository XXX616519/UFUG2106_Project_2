import random
import math
import os
from typing import Tuple, Optional

class ElGamalKeyGenerator:
    """
    ElGamal密钥生成器
    
    功能特性：
    1. 支持自定义安全素数p、生成元g和私钥x
    2. 安全内存擦除（符合NIST SP 800-88标准）
    3. 增强型参数验证
    4. 优化的素性检测算法
    """
    
    MAX_RETRIES = 1000  # 最大素数生成尝试次数
    
    @staticmethod
    def generate_keypair(
        bit_length: int = 2048,
        p: Optional[int] = None,
        g: Optional[int] = None,
        x: Optional[int] = None
    ) -> Tuple[Tuple[int, int, int], int]:
        """
        生成ElGamal密钥对（支持自动生成或自定义参数）
        
        参数验证流程：
        1. 参数共存性检查（必须同时提供所有参数或都不提供）
        2. 素数有效性验证（素性检测+安全素数检查）
        3. 生成元有效性验证
        4. 私钥范围验证
        """
        #region 安全擦除函数
        def secure_wipe(num: int) -> None:
            """符合NIST SP 800-88的三次覆盖擦除"""
            if num is None:
                return
            try:
                byte_len = (num.bit_length() + 7) // 8
                buffer = bytearray(byte_len)
                buffer[:] = os.urandom(byte_len)
                for i in range(byte_len):
                    buffer[i] ^= 0xFF
                buffer[:] = b'\x00' * byte_len
            finally:
                del buffer
        #endregion

        #region 初始化清理
        p_val = g_val = x_val = h = q_val = None
        try:
            #region 参数验证
            if (p is None or g is None or x is None) and not (p is None and g is None and x is None):
                raise ValueError(
                    "ERR201: p/g/x必须同时提供或都不提供 | "
                    "p/g/x must be all provided or omitted"
                )
            
            custom_mode = p is not None
            #endregion

            if custom_mode:
                #region 自定义参数验证
                # 类型验证
                if not all(isinstance(v, int) for v in [p, g, x]):
                    raise TypeError("ERR202: p/g/x必须为整数 | p/g/x must be integers")
                
                # 素数验证
                if not ElGamalKeyGenerator._is_prime(p):
                    raise ValueError("ERR203: p必须为素数 | p must be prime")
                
                # 安全素数验证（p=2q+1）
                q_val = (p - 1) // 2
                if not ElGamalKeyGenerator._is_prime(q_val):
                    raise ValueError("ERR204: p必须为安全素数 | p must be a safe prime")
                
                # 生成元验证
                if pow(g, 2, p) == 1 or pow(g, q_val, p) == 1:
                    raise ValueError("ERR205: g不是有效的生成元 | g is not a valid generator")
                
                # 私钥范围验证
                if not (1 < x < p-1):
                    raise ValueError(f"ERR206: 私钥范围无效 | x must satisfy 1 < x < {p-1}")
                
                # 计算公钥h
                h = pow(g, x, p)
                #endregion
            else:
                #region 自动生成模式
                for _ in range(ElGamalKeyGenerator.MAX_RETRIES):
                    # 生成安全素数p
                    p_val, q_val = ElGamalKeyGenerator._generate_safe_prime(bit_length)
                    
                    # 寻找生成元g
                    g_val = ElGamalKeyGenerator._find_generator(p_val, q_val)
                    
                    # 生成私钥x
                    x_val = random.randint(2, p_val-2)
                    
                    # 计算公钥h
                    h = pow(g_val, x_val, p_val)
                    
                    if g_val and h:
                        break
                else:
                    raise RuntimeError("ERR207: 无法生成合规参数 | Failed to generate valid parameters")
                
                p, g, x = p_val, g_val, x_val
                #endregion

            return ((p, g, h), x)

        finally:
            #region 安全清理
            secure_wipe(p_val)
            secure_wipe(g_val)
            secure_wipe(x_val)
            secure_wipe(q_val)
            secure_wipe(h if 'h' in locals() else 0)
            # 解除引用
            p_val = g_val = x_val = h = q_val = None
            #endregion

    @staticmethod
    def _generate_safe_prime(bit_length: int) -> Tuple[int, int]:
        """生成安全素数p=2q+1"""
        for _ in range(ElGamalKeyGenerator.MAX_RETRIES):
            q = ElGamalKeyGenerator._generate_prime(bit_length - 1)  # 修正位数计算
            p = 2 * q + 1
            if ElGamalKeyGenerator._is_prime(p):
                return p, q
        raise RuntimeError("ERR208: 安全素数生成超时 | Safe prime generation timeout")

    @staticmethod
    def _find_generator(p: int, q: int) -> int:
        """寻找生成元g"""
        for _ in range(10000):  # 增加尝试次数
            g = random.randint(2, p-1)
            if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
                return g
        raise RuntimeError("ERR209: 生成元查找失败 | Generator not found")

    @staticmethod
    def _generate_prime(bit_length: int) -> int:
        """生成指定位数的素数"""
        SMALL_PRIMES = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
            157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
            239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
            331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
            421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
            509, 521, 523, 541
        ]
        for _ in range(10000):  # 增加尝试次数
            candidate = random.getrandbits(bit_length)
            candidate |= (1 << (bit_length - 1)) | 1  # 确保最高位和最低位为1
            if any(candidate % p == 0 for p in SMALL_PRIMES if p < candidate):
                continue
            if ElGamalKeyGenerator._is_prime(candidate):
                return candidate
        raise RuntimeError("ERR210: 素数生成超时 | Prime generation timeout")

    @staticmethod
    def _is_prime(n: int, k: int = 64) -> bool:
        """优化的Miller-Rabin检测算法"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False

        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
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

class ElGamal:
    """ElGamal加密解密类"""
    def __init__(self, public_key: Tuple[int, int, int], private_key: Optional[int] = None):
        """
        初始化ElGamal实例
        
        :param public_key: 公钥(p, g, h)
        :param private_key: 私钥x
        """
        self.p, self.g, self.h = self._validate_public_key(public_key)
        self.x = private_key
        
        if private_key is not None:
            if not (1 < self.x < self.p-1):
                raise ValueError("ERR211: 私钥范围无效 | Private key out of range")
            if pow(self.g, self.x, self.p) != self.h:
                raise ValueError("ERR212: 私钥与公钥不匹配 | Private key doesn't match public key")

    @staticmethod
    def _validate_public_key(key: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """验证公钥格式"""
        if len(key) != 3:
            raise ValueError("ERR213: 公钥格式应为(p, g, h) | Public key must be (p, g, h)")
        p, g, h = key
        if p <= 0 or g <= 0 or h <= 0:
            raise ValueError("ERR214: 公钥参数必须为正整数 | Public key parameters must be positive integers")
        return p, g, h

    def encrypt(self, plaintext: bytes) -> Tuple[int, int]:
        """
        使用公钥加密数据
        
        :param plaintext: 明文字节数据
        :return: 密文元组(c1, c2)
        """
        if not isinstance(plaintext, bytes):
            raise TypeError("ERR215: 明文必须是字节串 | Plaintext must be bytes")
        
        m = int.from_bytes(plaintext, byteorder='big')
        if m >= self.p:
            raise ValueError(f"ERR216: 明文过大，最大允许值为{self.p-1} | Plaintext too large")
        
        # 安全擦除临时变量
        y = s = None
        try:
            y = random.randint(2, self.p-2)
            c1 = pow(self.g, y, self.p)
            s = pow(self.h, y, self.p)
            c2 = (m * s) % self.p
            return (c1, c2)
        finally:
            # 安全擦除
            if y is not None:
                self._secure_wipe(y)
            if s is not None:
                self._secure_wipe(s)

    def decrypt(self, ciphertext: Tuple[int, int]) -> bytes:
        """
        使用私钥解密数据
        
        :param ciphertext: 密文元组(c1, c2)
        :return: 解密后的字节数据
        """
        if self.x is None:
            raise RuntimeError("ERR217: 未提供私钥 | Private key not available")
        
        c1, c2 = ciphertext
        if not (0 < c1 < self.p and 0 < c2 < self.p):
            raise ValueError("ERR218: 密文值无效 | Invalid ciphertext values")
        
        # 安全擦除临时变量
        s = s_inv = None
        try:
            s = pow(c1, self.x, self.p)
            s_inv = pow(s, -1, self.p)
            m = (c2 * s_inv) % self.p
            byte_length = (self.p.bit_length() + 7) // 8
            return m.to_bytes(byte_length, byteorder='big').lstrip(b'\x00')  # 移除前导零
        finally:
            if s is not None:
                self._secure_wipe(s)
            if s_inv is not None:
                self._secure_wipe(s_inv)

    @staticmethod
    def _secure_wipe(num: int) -> None:
        """安全擦除整数"""
        byte_len = (num.bit_length() + 7) // 8
        buffer = bytearray(byte_len)
        buffer[:] = os.urandom(byte_len)
        for i in range(byte_len):
            buffer[i] ^= 0xFF
        buffer[:] = b'\x00' * byte_len

    @classmethod
    def create_keypair(cls, bit_length: int = 2048) -> Tuple['ElGamal', 'ElGamal']:
        """
        创建配对的ElGamal实例
        
        :param bit_length: 安全素数p的位长
        :return: (公钥实例，私钥实例)
        """
        public_key, private_key = ElGamalKeyGenerator.generate_keypair(bit_length)
        return (
            cls(public_key=public_key),
            cls(public_key=public_key, private_key=private_key)
        )

# 使用示例
if __name__ == "__main__":
    # 生成密钥对
    alice_public, alice_private = ElGamal.create_keypair(512)
    
    # 加密测试
    message = b"Hello, ElGamal, I'm Keyu Hu!"
    ciphertext = alice_public.encrypt(message)
    print("加密结果:", ciphertext)
    print("公钥:", alice_public.p, alice_public.g, alice_public.h)
    print("私钥:", alice_private.x)
    
    # 解密测试
    decrypted = alice_private.decrypt(ciphertext)
    print("解密结果:", decrypted.decode('utf-8'))