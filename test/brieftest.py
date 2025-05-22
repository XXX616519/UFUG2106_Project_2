
import time

import os
import sys  
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.RSA.rsa import RSA
from src.RSA.rsa import RSAKeyGenerator
from src.ElGamal.ElGamal import ElGamal
from src.ElGamal.ElGamal import ElGamalKeyGenerator

# rsa_private_key, rsa_public_key = RSAKeyGenerator.generate_keypair(2048)
public_elgamal, private_elgamal = ElGamal.create_keypair(bit_length=1024)


test_data = (b"Hello. ", 
             b"Hello, this " ,
             b"Hello, this is a  " ,
             b"Hello, this is a test  " ,
             b"Hello, this is a test data  " ,
             b"Hello, this is a test data for encryption  " ,
             b"Hello, this is a test data for encryption and decryption. " ) 


# public_rsa = RSA(rsa_public_key)
# # public_elgamal = ElGamal(elgamal_public_key, elgamal_private_key)
# private_rsa = RSA(rsa_public_key,rsa_private_key) 
# times_original_data = 1
# for data in test_data:
#     start_time = time.perf_counter()
#     ciphertext = public_rsa.encrypt(data)
#     end_time01 = time.perf_counter()
#     decrypted_text = private_rsa.decrypt(ciphertext)
#     end_time02 = time.perf_counter()
#     print(f"Test {times_original_data}: bytes={len(data)} Encrypt={end_time01-start_time:.6f}s, Decrypt={end_time02-end_time01:.6f}s")
#     times_original_data += 1


times_original_data = 1
for data in test_data:
    start_time = time.perf_counter()
    ciphertext = public_elgamal.encrypt(data)
    end_time01 = time.perf_counter()
    decrypted = private_elgamal.decrypt(ciphertext)
    end_time02 = time.perf_counter()
    print(f"Test {times_original_data}: bytes={len(data)} Encrypt={end_time01-start_time:.6f}s, Decrypt={end_time02-end_time01:.6f}s")
    times_original_data += 1
