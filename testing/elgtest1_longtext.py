import sys
import os
import time
import csv
import math
from pathlib import Path
import psutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ElGamal.ElGamal import ElGamal, ElGamalKeyGenerator

def split_text(text, chunk_size):
    """将文本分割成指定大小的块"""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def encrypt_long_text(public_key, text, chunk_size=50):
    """分段加密长文本"""
    chunks = split_text(text, chunk_size)
    encrypted_chunks = []
    for chunk in chunks:
        encrypted_chunks.append(public_key.encrypt(chunk.encode('utf-8')))
    return encrypted_chunks

def decrypt_long_text(private_key, encrypted_chunks):
    """分段解密长文本"""
    decrypted_chunks = []
    for chunk in encrypted_chunks:
        decrypted_chunks.append(private_key.decrypt(chunk).decode('utf-8'))
    return ''.join(decrypted_chunks)

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

# 长文本加密测试
long_text = 'ashoijhodigjvuosidjufosirujgferioguhjeal.ri55ruhgtyealiuheliruhgezilruhgnuidhgl.iezsruhglikzseurhgtkuze,ryftgtzsukyrhftgukzy  sZEIYugfhtwzyiurgftbzeusiyrgf  szyuiehgbfvezsrkiuygvhflzieusyrhgfzleuirskyghvbrzsdliuygfvzrluksyhgf rzilsyughzlsir.ugyhzrly.iguhybvzsrl.igvuhrszilvuygggszghrggggggligyggugvghgzggerjsli.g,vyzsrvl,kuizsrygh'


print("\n原始长文本:")
print(long_text)

# 加密
start_time = time.time()
mem_before = process.memory_info().rss / 1024 / 1024  # MB

encrypted_chunks = encrypt_long_text(alice_public, long_text)

encrypt_time = time.time() - start_time
mem_after = process.memory_info().rss / 1024 / 1024
print(f"\n加密性能:")
print(f"时间: {encrypt_time:.4f}秒") 
print(f"内存使用: {mem_after - mem_before:.2f} MB")
print("加密后的分段数量:", len(encrypted_chunks))

# 解密
start_time = time.time()
mem_before = process.memory_info().rss / 1024 / 1024  # MB

decrypted_text = decrypt_long_text(alice_private, encrypted_chunks)

decrypt_time = time.time() - start_time
mem_after = process.memory_info().rss / 1024 / 1024
print(f"\n解密性能:")
print(f"时间: {decrypt_time:.4f}秒")
print(f"内存使用: {mem_after - mem_before:.2f} MB")
print("\n解密结果:")
print(decrypted_text)

# 验证解密结果是否与原文一致
print("\n解密结果与原文一致:", decrypted_text == long_text)
