import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ElGamal.ElGamal import ElGamal, ElGamalKeyGenerator

def split_text(text, chunk_size):
    """将文本分割成指定大小的块"""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
def encrypt_long_text(public_key, text, chunk_size= 10):
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
alice_public, alice_private = ElGamal.create_keypair(1024)

def read_file_content(file_path):
    """读取文件内容"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, 'r', encoding='utf-8') as file:
        return file.read()

# 长文本加密测试
long_text = read_file_content('data.txt')

# 加密并保存结果到文件
encrypted_chunks = encrypt_long_text(alice_public, long_text)
with open('c:/Users/26406/Desktop/discrete math project 2/UFUG2106_Project_2-main/testing/encrypt.txt', 'w', encoding='utf-8') as f:
    for chunk in encrypted_chunks:
        f.write(f"{chunk}\n")

# 解密并保存结果到文件
decrypted_text = decrypt_long_text(alice_private, encrypted_chunks)
with open('c:/Users/26406/Desktop/discrete math project 2/UFUG2106_Project_2-main/testing/decrypt.txt', 'w', encoding='utf-8') as f:
    f.write(decrypted_text)

# 验证解密结果是否与原文一致
assert decrypted_text == long_text, "解密结果与原文不一致"
print("加密解密完成，结果已保存")
