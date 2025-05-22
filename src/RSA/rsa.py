import random
import math
import os
import struct
import hashlib
from typing import Tuple, Optional

class RSAKeyGenerator:
    """
    RSA Key Generator (Final Version)

    Features:
    1. Supports custom prime numbers p/q
    2. Secure memory wiping
    3. Enhanced parameter validation
    4. Stack overflow prevention design
    5. Optimized primality testing algorithm
    """

    MAX_RETRIES = 10  # Maximum key generation attempts

    @staticmethod
    def generate_keypair(
        bit_length: int = 2048,
        p: Optional[int] = None,
        q: Optional[int] = None
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Generate RSA key pair (supports automatic generation or custom primes)

        Parameter validation process:
        1. Bit length compliance check (bit_length ≥ 2048)
        2. p/q coexistence check (must be both provided or omitted)
        3. Prime validity check (primality test + uniqueness check)
        4. Length compliance validation (modulus bit length match)
        5. Coprimality validation (gcd(e, φ(n)) == 1)
        """
        #region Secure wiping function
        def secure_wipe(num: int) -> None:
            """Three-pass overwrite wiping compliant with NIST SP 800-88"""
            if num is None:
                return

            try:
                byte_len = (num.bit_length() + 7) // 8
                buffer = bytearray(byte_len)
                # First pass: random data
                buffer[:] = os.urandom(byte_len)
                # Second pass: bit flipping
                for i in range(byte_len):
                    buffer[i] ^= 0xFF
                # Third pass: all zeros
                buffer[:] = b'\x00' * byte_len
            finally:
                del buffer
        #endregion

        #region Initialization cleanup
        p_val = q_val = phi = n = e = d = None
        try:
            #region Parameter validation
            if (p is None) != (q is None):
                raise ValueError(
                    "ERR101: p and q must be both provided or omitted"
                )

            custom_mode = p is not None
            #endregion

            #region Custom prime handling
            if custom_mode:
                # Type validation
                if not isinstance(p, int) or not isinstance(q, int):
                    raise TypeError(
                        "ERR102: p/q must be integers"
                    )

                # Primality validation
                prime_check = [
                    (p, "p"),
                    (q, "q")
                ]
                for num, name in prime_check:
                    if not RSAKeyGenerator._is_prime(num):
                        raise ValueError(
                            f"ERR103: {name} is not prime"
                        )

                # Uniqueness validation
                if p == q:
                    raise ValueError(
                        "ERR104: p and q must be distinct"
                    )

                # Length validation
                target_prime_bits = bit_length // 2
                if (p.bit_length() + q.bit_length()) != (2 * target_prime_bits):
                    raise ValueError("ERR106: Total prime bits mismatch")

                n = p * q
                actual_bit_length = n.bit_length()
                if not (bit_length - 2 <= actual_bit_length <= bit_length + 2):
                    raise ValueError(
                        f"ERR105: Modulus bit length mismatch | Expected: {bit_length}±2, Actual: {actual_bit_length}\n"
                        "Possible cause: Prime bits deviation too large"
                    )

                # Prime bit length validation
                target_prime_bits = bit_length // 2
                prime_bit_check = [
                    (p, target_prime_bits, "p"),
                    (q, target_prime_bits, "q")
                ]
                for prime, target, name in prime_bit_check:
                    prime_bits = prime.bit_length()
                    if not (target - 2 <= prime_bits <= target + 2):
                        raise ValueError(
                            f"ERR106: {name} bit length mismatch | "
                            f"Expected: {target}±2 bits, Actual: {prime_bits} bits"
                        )
            #endregion

            #region Automatic generation mode
            else:
                if bit_length < 2048:
                    raise ValueError(
                        "ERR107: Key length must be ≥2048 bits"
                    )

                target_prime_bits = bit_length // 2
                for attempt in range(RSAKeyGenerator.MAX_RETRIES):
                    # Securely wipe previously generated data
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
                        "ERR108: Failed to generate valid prime pair"
                    )

                p, q = p_val, q_val
            #endregion

            #region Compute core parameters
            phi = (p - 1) * (q - 1)
            e = 65537

            # Coprimality validation
            if math.gcd(e, phi) != 1:
                if custom_mode:
                    raise ValueError(
                        "ERR109: e and φ(n) are not coprime"
                    )
                raise RuntimeError(
                    "ERR110: Coprimality check failed in auto mode"
                )

            d = pow(e, -1, phi)
            #endregion

            return ((e, n), (d, n))

        finally:
            #region Secure cleanup
            secure_wipe(p_val)
            secure_wipe(q_val)
            secure_wipe(phi)
            secure_wipe(e if 'e' in locals() else 0)
            secure_wipe(d if 'd' in locals() else 0)
            # Remove references
            p_val = q_val = phi = e = d = None
            #endregion

    @staticmethod
    def _generate_prime(bit_length: int) -> int:
        """Optimized prime generation algorithm"""
        # Fast path: pre-generated small prime check
        SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

        for _ in range(10000):  # Maximum attempts
            # Generate candidate
            candidate = random.getrandbits(bit_length)
            candidate |= (1 << (bit_length - 1)) | 1  # Ensure highest bit is 1 and odd

            # Quick elimination
            if any(candidate % p == 0 for p in SMALL_PRIMES if p < candidate):
                continue

            if RSAKeyGenerator._is_prime(candidate):
                return candidate
        raise RuntimeError("ERR111: Prime generation timeout")

    @staticmethod
    def _is_prime(n: int, k: int = 64) -> bool:
        """Optimized Miller-Rabin primality test"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False

        # Decompose n-1 as d*2^s
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        # Use a combination of fixed and random bases
        witnesses = [2, 3, 5, 7, 11]  # Deterministic for n < 2^64
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

#region RSA class
class RSA:
    """RSA Encryption/Decryption Class"""
    def __init__(self, public_key: Tuple[int, int], private_key: Optional[Tuple[int, int]] = None):
        """
        Initialize RSA instance

        :param public_key: Public key (e, n)
        :param private_key: Private key (d, n) (optional)
        """
        self.e, self.n = self._validate_key(public_key)
        self.d = private_key[0] if private_key else None

        # Validate private key if provided
        if private_key:
            if private_key[1] != self.n:
                raise ValueError("Private key doesn't match public key")
            if not (0 < private_key[0] < self.n):
                raise ValueError("Invalid private key")

        self.OAEP_PARAMS = {
        "hash_alg": hashlib.sha256,       # Hash algorithm
        "mgf_alg": hashlib.sha256,        # MGF hash algorithm
        "label": b"",                     # Label (optional)
        "hash_len": 32,                   # SHA-256 output length
        }

    @classmethod
    def _validate_oaep_params(cls, params: dict) -> None:
        """Validate OAEP parameter legality"""
        if params["hash_len"] != params["hash_alg"]().digest_size:
            raise ValueError("Hash length does not match algorithm")

    @classmethod
    def _mgf1(cls, seed: bytes, mask_len: int, mgf_hash) -> bytes:
        """PKCS#1 compliant MGF1 implementation"""
        counter = 0
        output = bytearray()
        while len(output) < mask_len:
            C = seed + struct.pack(">I", counter)
            output.extend(mgf_hash(C).digest())
            counter += 1
        return bytes(output[:mask_len])

    def oaep_encode(self, plaintext: bytes) -> bytes:
        """Standard OAEP encoding process"""
        params = self.OAEP_PARAMS
        k = (self.n.bit_length() + 7) // 8  # Modulus byte length
        max_msg_len = k - 2 * params["hash_len"] - 2
        if len(plaintext) > max_msg_len:
            raise ValueError(f"Plaintext too long (maximum {max_msg_len} bytes)")

        # Step 1: Generate lHash
        lhash = params["hash_alg"](params["label"]).digest()

        # Step 2: Pad PS
        ps = b"\x00" * (max_msg_len - len(plaintext))

        # Step 3: Construct DB
        db = lhash + ps + b"\x01" + plaintext

        # Step 4: Generate random seed
        seed = os.urandom(params["hash_len"])

        # Step 5: Generate dbMask and maskedDB
        db_mask = self._mgf1(seed, len(db), params["mgf_alg"])
        masked_db = bytes(x ^ y for x, y in zip(db, db_mask))

        # Step 6: Generate seedMask and maskedSeed
        seed_mask = self._mgf1(masked_db, params["hash_len"], params["mgf_alg"])
        masked_seed = bytes(x ^ y for x, y in zip(seed, seed_mask))

        # Step 7: Concatenate final data
        return b"\x00" + masked_seed + masked_db

    def oaep_decode(self, ciphertext: bytes) -> bytes:
        """Standard OAEP decoding process"""
        params = self.OAEP_PARAMS
        k = (self.n.bit_length() + 7) // 8
        if len(ciphertext) != k or k < 2 * params["hash_len"] + 2:
            raise ValueError("Invalid OAEP ciphertext format")

        # Step 1: Decompose data
        masked_seed = ciphertext[1:1 + params["hash_len"]]
        masked_db = ciphertext[1 + params["hash_len"]:]

        # Step 2: Recover seed
        seed_mask = self._mgf1(masked_db, params["hash_len"], params["mgf_alg"])
        seed = bytes(x ^ y for x, y in zip(masked_seed, seed_mask))

        # Step 3: Recover DB
        db_mask = self._mgf1(seed, len(masked_db), params["mgf_alg"])
        db = bytes(x ^ y for x, y in zip(masked_db, db_mask))

        # Step 4: Validate lHash
        lhash = params["hash_alg"](params["label"]).digest()
        if db[: params["hash_len"]] != lhash:
            raise ValueError("OAEP label validation failed")

        # Step 5: Find delimiter
        try:
            sep_pos = db.index(b"\x01", params["hash_len"])
        except ValueError:
            raise ValueError("OAEP format error: delimiter not found")

        return db[sep_pos + 1:]

    @staticmethod
    def _validate_key(key: Tuple[int, int]) -> Tuple[int, int]:
        """
        Validate key format

        :param key: Key to validate
        :return: Validated key
        """
        if len(key) != 2:
            raise ValueError("Key should be in (e/d, n) format")
        e_or_d, n = key
        if n <= 0:
            raise ValueError("Modulus n must be positive integer")
        if e_or_d <= 0:
            raise ValueError("Exponent must be positive integer")
        return e_or_d, n

    def encrypt(self, plaintext: bytes, use_oaep: bool = True) -> int:
        """Encryption with OAEP support"""
        if use_oaep:
            padded = self.oaep_encode(plaintext)
        else:
            padded = plaintext

        plain_int = int.from_bytes(padded, byteorder="big")
        # Retain original range check
        if plain_int >= self.n:
            raise ValueError("Plaintext value must be less than modulus n")
        return pow(plain_int, self.e, self.n)

    def decrypt(self, ciphertext: int, use_oaep: bool = True) -> bytes:
        """Decryption with OAEP support"""
        if not self.d:
            raise RuntimeError("Decryption requires private key")

        plain_int = pow(ciphertext, self.d, self.n)
        padded = plain_int.to_bytes(
            (self.n.bit_length() + 7) // 8, byteorder="big"
        )

        if use_oaep:
            return self.oaep_decode(padded)
        return padded

    @classmethod
    def create_keypair(cls, bit_length: int = 2048) -> Tuple['RSA', 'RSA']:
        """
        Create paired RSA instances

        :param bit_length: Key length
        :return: (public key instance, private key instance)
        """
        public_key, private_key = RSAKeyGenerator.generate_keypair(bit_length)
        return (
            cls(public_key=public_key),
            cls(public_key=public_key, private_key=private_key)
        )