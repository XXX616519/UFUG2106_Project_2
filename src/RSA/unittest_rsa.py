import unittest
from rsa import RSAKeyGenerator, RSA
import os
import struct

class TestHighBitRSA(unittest.TestCase):
    """High-bit RSA Comprehensive Test Class (≥2048 bits)"""
    
    @classmethod
    def setUpClass(cls):
        """Generate 2048-bit test key pair"""
        cls.public_key, cls.private_key = RSAKeyGenerator.generate_keypair(bit_length=2048)
        cls.rsa_pub = RSA(cls.public_key)
        cls.rsa_priv = RSA(cls.public_key, cls.private_key)
        
        # Precalculate large number test parameters
        cls.max_byte_length = (cls.public_key[1].bit_length() + 7) // 8
        cls.overflow_data = os.urandom(cls.max_byte_length + 1)
        cls.valid_large_data = os.urandom(cls.max_byte_length - 1)

    def test_key_generation_validation(self):
        """Test key generation parameter validation"""
        # Test illegal bit length
        with self.assertRaises(ValueError):
            RSAKeyGenerator.generate_keypair(bit_length=1024)
        
        # Test non-prime input
        with self.assertRaises(ValueError):
            RSAKeyGenerator.generate_keypair(
                bit_length=2048,
                p=123456,
                q=987654
            )
        
        # Verify auto-generated key parameters
        e, n = self.public_key
        d, _ = self.private_key
        self.assertEqual(e, 65537, "Public key exponent should be 65537")
        self.assertEqual(n.bit_length(), 2048, "Modulus should be 2048 bits")
        self.assertTrue(0 < d < (n-1), "Private key should be within valid range")

    def test_encryption_decryption_cycle(self):
        """Test complete encryption-decryption process"""
        test_vectors = [
            b"",                          # Empty data
            b"A",                         # ASCII character
            os.urandom(50),              # Random data (max supported length minus padding)
            b"\xFF\x00" * 80,            # Boundary byte value combinations
            "English test".encode('utf-8')  # Unicode data
        ]
        
        for plaintext in test_vectors:
            with self.subTest(plaintext=plaintext):
                # Convert plaintext to integer
                if isinstance(plaintext, str):
                    plaintext = plaintext.encode('utf-8')
                ciphertext = self.rsa_pub.encrypt(plaintext)
                decrypted = self.rsa_priv.decrypt(ciphertext)
                self.assertEqual(plaintext, decrypted, "Decrypted result should match original plaintext")

    def test_input_validation(self):
        """Test input type and boundary validation"""
        # Invalid input types
        with self.assertRaises(TypeError):
            self.rsa_pub.encrypt(123)  # Integer input
            
        with self.assertRaises(TypeError):
            self.rsa_pub.encrypt("Unencoded string")

        # Data length validation
        with self.assertRaises(ValueError):
            self.rsa_pub.encrypt(self.overflow_data)

        # Ciphertext range validation
        with self.assertRaises(ValueError):
            self.rsa_priv.decrypt(self.public_key[1] + 1)  # Exceeds modulus

    def test_custom_prime_operation(self):
        """Test custom prime mode"""
        # Use known secure primes to generate keys
        p = 106697219132480173106064317148705638676529121742557567770857687729397446898790451577487723991083173010242416863238099716044775658681981821407922722052778958942891831033512463262741053961681512908218003840408526915629689432111480588966800949428079015682624591636010678691927285321708935076221951173426894836169
        q = 144819424465842307806353672547344125290716753535239658417883828941232509622838692761917211806963011168822281666033695157426515864265527046213326145174398018859056439431422867957079149967592078894410082695714160599647180947207504108618794637872261572262805565517756922288320779308895819726074229154002310375209
   
        pub, priv = RSAKeyGenerator.generate_keypair(
            bit_length=2048,
            p=p,
            q=q
        )
        
        # Verify key parameters
        self.assertEqual(pub[1], p*q, "Modulus should be product of primes")
        self.assertEqual(pub[0], 65537, "Public key exponent should be 65537")
        
        # Verify encryption-decryption functionality
        test_data = b"Custom primes test"
        cipher = RSA(pub).encrypt(test_data)
        decrypted = RSA(pub, priv).decrypt(cipher)
        self.assertEqual(test_data, decrypted.rstrip(b'\x00'))

if __name__ == '__main__':
    unittest.main(verbosity=2)