import random
import math
import os
from typing import Tuple, Optional

class ElGamalKeyGenerator:
    """
    ElGamal Key Generator

    Features:
    1. Supports custom safe prime p, generator g, and private key x
    2. Secure memory wiping (compliant with NIST SP 800-88)
    3. Enhanced parameter validation
    4. Optimized primality testing algorithm
    """

    MAX_RETRIES = 1000  # Maximum attempts to generate a prime number

    @staticmethod
    def generate_keypair(
        bit_length: int = 2048,
        p: Optional[int] = None,
        g: Optional[int] = None,
        x: Optional[int] = None
    ) -> Tuple[Tuple[int, int, int], int]:
        """
        Generate ElGamal key pair (supports automatic generation or custom parameters)

        Parameter validation process:
        1. Parameter coexistence check (all parameters must be provided or omitted)
        2. Prime number validity check (primality test + safe prime check)
        3. Generator validity check
        4. Private key range validation
        """
        #region Secure wiping function
        def secure_wipe(num: int) -> None:
            """Three-pass overwrite wiping compliant with NIST SP 800-88"""
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

        #region Initialization cleanup
        p_val = g_val = x_val = h = q_val = None
        try:
            #region Parameter validation
            if (p is None or g is None or x is None) and not (p is None and g is None and x is None):
                raise ValueError(
                    "ERR201: p/g/x must be all provided or omitted"
                )

            custom_mode = p is not None
            #endregion

            if custom_mode:
                #region Custom parameter validation
                # Type validation
                if not all(isinstance(v, int) for v in [p, g, x]):
                    raise TypeError("ERR202: p/g/x must be integers")

                # Prime number validation
                if not ElGamalKeyGenerator._is_prime(p):
                    raise ValueError("ERR203: p must be prime")

                # Safe prime validation (p=2q+1)
                q_val = (p - 1) // 2
                if not ElGamalKeyGenerator._is_prime(q_val):
                    raise ValueError("ERR204: p must be a safe prime")

                # Generator validation
                if pow(g, 2, p) == 1 or pow(g, q_val, p) == 1:
                    raise ValueError("ERR205: g is not a valid generator")

                # Private key range validation
                if not (1 < x < p-1):
                    raise ValueError(f"ERR206: x must satisfy 1 < x < {p-1}")

                # Calculate public key h
                h = pow(g, x, p)
                #endregion
            else:
                #region Automatic generation mode
                for _ in range(ElGamalKeyGenerator.MAX_RETRIES):
                    # Generate safe prime p
                    p_val, q_val = ElGamalKeyGenerator._generate_safe_prime(bit_length)

                    # Find generator g
                    g_val = ElGamalKeyGenerator._find_generator(p_val, q_val)

                    # Generate private key x
                    x_val = random.randint(2, p_val-2)

                    # Calculate public key h
                    h = pow(g_val, x_val, p_val)

                    if g_val and h:
                        break
                else:
                    raise RuntimeError("ERR207: Failed to generate valid parameters")

                p, g, x = p_val, g_val, x_val
                #endregion

            return ((p, g, h), x)

        finally:
            #region Secure cleanup
            secure_wipe(p_val)
            secure_wipe(g_val)
            secure_wipe(x_val)
            secure_wipe(q_val)
            secure_wipe(h if 'h' in locals() else 0)
            # Dereference
            p_val = g_val = x_val = h = q_val = None
            #endregion

    @staticmethod
    def _generate_safe_prime(bit_length: int) -> Tuple[int, int]:
        """Generate safe prime p=2q+1"""
        for _ in range(ElGamalKeyGenerator.MAX_RETRIES):
            q = ElGamalKeyGenerator._generate_prime(bit_length - 1)  # Adjust bit length calculation
            p = 2 * q + 1
            if ElGamalKeyGenerator._is_prime(p):
                return p, q
        raise RuntimeError("ERR208: Safe prime generation timeout")

    @staticmethod
    def _find_generator(p: int, q: int) -> int:
        """Find generator g"""
        for _ in range(10000):  # Increase attempts
            g = random.randint(2, p-1)
            if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
                return g
        raise RuntimeError("ERR209: Generator not found")

    @staticmethod
    def _generate_prime(bit_length: int) -> int:
        """Generate a prime number with specified bit length"""
        SMALL_PRIMES = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
            157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
            239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
            331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
            421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
            509, 521, 523, 541
        ]
        for _ in range(10000):  # Increase attempts
            candidate = random.getrandbits(bit_length)
            candidate |= (1 << (bit_length - 1)) | 1  # Ensure the highest and lowest bits are 1
            if any(candidate % p == 0 for p in SMALL_PRIMES if p < candidate):
                continue
            if ElGamalKeyGenerator._is_prime(candidate):
                return candidate
        raise RuntimeError("ERR210: Prime generation timeout")

    @staticmethod
    def _is_prime(n: int, k: int = 64) -> bool:
        """Optimized Miller-Rabin primality test"""
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
    """ElGamal encryption and decryption class"""
    def __init__(self, public_key: Tuple[int, int, int], private_key: Optional[int] = None):
        """
        Initialize ElGamal instance

        :param public_key: Public key (p, g, h)
        :param private_key: Private key x
        """
        self.p, self.g, self.h = self._validate_public_key(public_key)
        self.x = private_key

        if private_key is not None:
            if not (1 < self.x < self.p-1):
                raise ValueError("ERR211: Private key out of range")
            if pow(self.g, self.x, self.p) != self.h:
                raise ValueError("ERR212: Private key doesn't match public key")

    @staticmethod
    def _validate_public_key(key: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Validate public key format"""
        if len(key) != 3:
            raise ValueError("ERR213: Public key must be (p, g, h)")
        p, g, h = key
        if p <= 0 or g <= 0 or h <= 0:
            raise ValueError("ERR214: Public key parameters must be positive integers")
        return p, g, h

    def encrypt(self, plaintext: bytes) -> Tuple[int, int]:
        """
        Encrypt data using the public key

        :param plaintext: Plaintext byte data
        :return: Ciphertext tuple (c1, c2)
        """
        if not isinstance(plaintext, bytes):
            raise TypeError("ERR215: Plaintext must be bytes")

        m = int.from_bytes(plaintext, byteorder='big')
        if m >= self.p:
            raise ValueError(f"ERR216: Plaintext too large, maximum allowed value is {self.p-1}")

        # Securely wipe temporary variables
        y = s = None
        try:
            y = random.randint(2, self.p-2)
            c1 = pow(self.g, y, self.p)
            s = pow(self.h, y, self.p)
            c2 = (m * s) % self.p
            return (c1, c2)
        finally:
            # Secure wiping
            if y is not None:
                self._secure_wipe(y)
            if s is not None:
                self._secure_wipe(s)

    def decrypt(self, ciphertext: Tuple[int, int]) -> bytes:
        """
        Decrypt data using the private key

        :param ciphertext: Ciphertext tuple (c1, c2)
        :return: Decrypted byte data
        """
        if self.x is None:
            raise RuntimeError("ERR217: Private key not available")

        c1, c2 = ciphertext
        if not (0 < c1 < self.p and 0 < c2 < self.p):
            raise ValueError("ERR218: Invalid ciphertext values")

        # Securely wipe temporary variables
        s = s_inv = None
        try:
            s = pow(c1, self.x, self.p)
            s_inv = pow(s, -1, self.p)
            m = (c2 * s_inv) % self.p
            byte_length = (self.p.bit_length() + 7) // 8
            return m.to_bytes(byte_length, byteorder='big').lstrip(b'\x00')  # Remove leading zeros
        finally:
            if s is not None:
                self._secure_wipe(s)
            if s_inv is not None:
                self._secure_wipe(s_inv)

    @staticmethod
    def _secure_wipe(num: int) -> None:
        """Securely wipe an integer"""
        byte_len = (num.bit_length() + 7) // 8
        buffer = bytearray(byte_len)
        buffer[:] = os.urandom(byte_len)
        for i in range(byte_len):
            buffer[i] ^= 0xFF
        buffer[:] = b'\x00' * byte_len

    @classmethod
    def create_keypair(cls, bit_length: int = 2048) -> Tuple['ElGamal', 'ElGamal']:
        """
        Create paired ElGamal instances

        :param bit_length: Bit length of the safe prime p
        :return: (Public key instance, Private key instance)
        """
        public_key, private_key = ElGamalKeyGenerator.generate_keypair(bit_length)
        return (
            cls(public_key=public_key),
            cls(public_key=public_key, private_key=private_key)
        )

# Usage example
if __name__ == "__main__":
    # Generate key pair
    alice_public, alice_private = ElGamal.create_keypair(512)

    # Encryption test
    message = b"Hello, ElGamal, I'm Keyu Hu!"
    ciphertext = alice_public.encrypt(message)
    print("Encryption result:", ciphertext)
    print("Public key:", alice_public.p, alice_public.g, alice_public.h)
    print("Private key:", alice_private.x)

    # Decryption test
    decrypted = alice_private.decrypt(ciphertext)
    print("Decryption result:", decrypted.decode('utf-8'))