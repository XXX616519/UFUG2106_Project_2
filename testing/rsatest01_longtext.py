import sys
import os
import time
import psutil
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RSA.rsa import RSA, RSAKeyGenerator

# 参数设置
key_length = 2048
CHUNK_SIZE = 117  # RSA 2048位密钥最大加密块大小

# 记录初始内存
start_mem = psutil.Process().memory_info().rss / 1024 / 1024

# 生成密钥
start_time = time.time()
private_key, public_key = RSAKeyGenerator.generate_keypair(key_length)
keygen_time = time.time() - start_time
print(f'密钥生成时间: {keygen_time:.4f}秒')

# 初始化RSA实例
public_rsa = RSA(public_key)
private_rsa = RSA(public_key, private_key)

# 获取脚本所在目录
script_dir = os.path.dirname(__file__)

def split_into_chunks(data, chunk_size):
    """将数据分成固定大小的块"""
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

# 读取data.txt内容作为明文
data_path = os.path.join(script_dir, 'data.txt')
with open(data_path, 'r', encoding='utf-8') as f:
    plaintext = f.read().encode('utf-8')  # 转换为字节串

# 分段加密并写入encrypt.txt
encrypt_path = os.path.join(script_dir, 'encrypt.txt')
total_encrypt_time = 0
chunk_count = 0

with open(encrypt_path, 'w') as f_enc:
    chunks = split_into_chunks(plaintext, CHUNK_SIZE)
    chunk_count = len(chunks)
    for chunk in chunks:
        start_time = time.time()
        encrypted = public_rsa.encrypt(chunk)
        encrypt_time = time.time() - start_time
        total_encrypt_time += encrypt_time
        f_enc.write(hex(encrypted) + '\n')  # 每行存储一个加密块

avg_encrypt_time = total_encrypt_time / chunk_count if chunk_count > 0 else 0
print(f'总加密时间: {total_encrypt_time:.4f}秒')
print(f'平均每块加密时间: {avg_encrypt_time:.6f}秒')

# 分段解密并写入decrypt.txt
decrypt_path = os.path.join(script_dir, 'decrypt.txt')
total_decrypt_time = 0

with open(encrypt_path, 'r') as f_enc, open(decrypt_path, 'wb') as f_dec:
    for line in f_enc:
        encrypted_hex = line.strip()
        encrypted = int(encrypted_hex, 16)
        start_time = time.time()
        decrypted = private_rsa.decrypt(encrypted)
        decrypt_time = time.time() - start_time
        total_decrypt_time += decrypt_time
        f_dec.write(decrypted)

avg_decrypt_time = total_decrypt_time / chunk_count if chunk_count > 0 else 0
print(f'总解密时间: {total_decrypt_time:.4f}秒')
print(f'平均每块解密时间: {avg_decrypt_time:.6f}秒')

# 验证解密结果
with open(decrypt_path, 'rb') as f:
    decrypted = f.read()
    assert decrypted == plaintext, "解密结果与原始明文不匹配"

# 内存使用
end_mem = psutil.Process().memory_info().rss / 1024 / 1024
print(f'当前内存使用: {end_mem:.2f} MB')
print(f'内存增量: {abs(end_mem - start_mem):.2f} MB')

# 性能摘要
print("\n性能摘要:")
print(f"密钥生成: {keygen_time:.4f}秒")
print(f"总加密时间: {total_encrypt_time:.4f}秒 (平均: {avg_encrypt_time:.6f}秒/块)")
print(f"总解密时间: {total_decrypt_time:.4f}秒 (平均: {avg_decrypt_time:.6f}秒/块)")
print(f"处理块数: {chunk_count}")
print(f"内存增量: {abs(end_mem - start_mem):.2f} MB")
print("长文本分段加密解密完成，结果已保存")
