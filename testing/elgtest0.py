import sys
import os
import time
import csv
import math
from pathlib import Path
import psutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ElGamal.ElGamal import ElGamal, ElGamalKeyGenerator

# 生成密钥对
start_time = time.time()
process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / 1024 / 1024  # MB

alice_public, alice_private = ElGamal.create_keypair(512)

keygen_time = time.time() - start_time
mem_after = process.memory_info().rss / 1024 / 1024
print(f"\n密钥生成性能:")
print(f"时间: {keygen_time:.4f}秒")
print(f"内存使用: {mem_after - mem_before:.2f} MB")

# 加密测试
# 导入字节串信息
start_time = time.time()
mem_before = process.memory_info().rss / 1024 / 1024  # MB

message = b"Hello, ElGamal, I'm Keyu Hu!"
ciphertext = alice_public.encrypt(message)

encrypt_time = time.time() - start_time
mem_after = process.memory_info().rss / 1024 / 1024
print(f"\n加密性能:")
print(f"时间: {encrypt_time:.4f}秒") 
print(f"内存使用: {mem_after - mem_before:.2f} MB")
print("加密结果:", ciphertext)
print("公钥:", alice_public.p, alice_public.g, alice_public.h)
print("私钥:", alice_private.x)

# 解密测试
start_time = time.time()
mem_before = process.memory_info().rss / 1024 / 1024  # MB

decrypted = alice_private.decrypt(ciphertext)

decrypt_time = time.time() - start_time
mem_after = process.memory_info().rss / 1024 / 1024
print(f"\n解密性能:")
print(f"时间: {decrypt_time:.4f}秒")
print(f"内存使用: {mem_after - mem_before:.2f} MB")
print("解密结果:", decrypted.decode('utf-8'))
