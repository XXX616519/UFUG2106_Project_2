import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RSA.rsa import RSA, RSAKeyGenerator

# 参数设置
key_length = 2048
CHUNK_SIZE = 117  # RSA 2048位密钥最大加密块大小

# 生成密钥
private_key, public_key = RSAKeyGenerator.generate_keypair(key_length)

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

with open(encrypt_path, 'w') as f_enc:
    chunks = split_into_chunks(plaintext, CHUNK_SIZE)
    for chunk in chunks:
        encrypted = public_rsa.encrypt(chunk)
        f_enc.write(hex(encrypted) + '\n')  # 每行存储一个加密块

# 分段解密并写入decrypt.txt
decrypt_path = os.path.join(script_dir, 'decrypt.txt')

with open(encrypt_path, 'r') as f_enc, open(decrypt_path, 'wb') as f_dec:
    for line in f_enc:
        encrypted_hex = line.strip()
        encrypted = int(encrypted_hex, 16)
        decrypted = private_rsa.decrypt(encrypted)
        f_dec.write(decrypted)

# 验证解密结果
with open(decrypt_path, 'rb') as f:
    decrypted = f.read()
    assert decrypted == plaintext, "解密结果与原始明文不匹配"

print("加密解密完成，结果已保存")
