# 更改绝对地址部分
# 密钥长度和区块长度是可调节参数,对于英语和中文可用最大值是不同的

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

# 分块长度
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
def get_avg_memory_usage(process, samples=5, interval=0.1):
    """获取平均内存使用量"""
    total = 0
    for _ in range(samples):
        total += process.memory_info().rss
        time.sleep(interval)
    return total / samples / 1024 / 1024  # MB

start_time = time.time()
process = psutil.Process(os.getpid())
mem_before = get_avg_memory_usage(process)

# 长度参数 
alice_public, alice_private = ElGamal.create_keypair(512)

keygen_time = time.time() - start_time
mem_after = get_avg_memory_usage(process)
mem_usage = max(0, mem_after - mem_before)  # 确保不为负
print(f"\n密钥生成性能:")
print(f"时间: {keygen_time:.4f}秒")
print(f"内存使用: {mem_usage:.2f} MB")

def read_file_content(file_path):
    """读取文件内容"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, 'r', encoding='utf-8') as file:
        return file.read()

# 长文本加密测试
long_text = read_file_content('data.txt')


print("\n原始长文本长度:", len(long_text), "字符")

# 加密
start_time = time.time()
mem_before = get_avg_memory_usage(process)

# 加密并保存结果到文件
encrypted_chunks = encrypt_long_text(alice_public, long_text)
with open('c:/Users/26406/Desktop/discrete math project 2/UFUG2106_Project_2-main/testing/encrypt.txt', 'w', encoding='utf-8') as f:
    for chunk in encrypted_chunks:
        f.write(f"{chunk}\n")

encrypt_time = time.time() - start_time
mem_after = get_avg_memory_usage(process)
mem_usage = max(0, mem_after - mem_before)
print(f"\n加密性能:")
print(f"时间: {encrypt_time:.4f}秒") 
print(f"内存使用: {mem_usage:.2f} MB")
print("加密后的分段数量:", len(encrypted_chunks))

# 解密
start_time = time.time()
mem_before = get_avg_memory_usage(process)

# 解密并保存结果到文件
decrypted_text = decrypt_long_text(alice_private, encrypted_chunks)
with open('c:/Users/26406/Desktop/discrete math project 2/UFUG2106_Project_2-main/testing/decrypt.txt', 'w', encoding='utf-8') as f:
    f.write(decrypted_text)

decrypt_time = time.time() - start_time
mem_after = get_avg_memory_usage(process)
mem_usage = max(0, mem_after - mem_before)
print(f"\n解密性能:")
print(f"时间: {decrypt_time:.4f}秒")
print(f"内存使用: {mem_usage:.2f} MB")
print("\n解密结果预览(前100字符):")
print(decrypted_text[:100] + "...")

# 验证解密结果是否与原文一致
print("\n解密结果与原文一致:", decrypted_text == long_text)
print("完整解密结果已保存到:", 'c:/Users/26406/Desktop/discrete math project 2/UFUG2106_Project_2-main/testing/decrypt.txt')
