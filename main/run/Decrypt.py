import os
import math
import hashlib
import struct

def read_encrypted_file(file_path):
    """读取加密文件，支持多行ELGamal|(数字1,数字2)格式"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if not lines:
            return None, []
            
        # 解析第一行获取加密方法
        first_line = lines[0].strip()
        if '|' not in first_line:
            return None, []
            
        method, first_data = first_line.split('|', 1)
        chunks = [first_data]
        
        # 处理剩余行
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            if '|' in line:
                _, data = line.split('|', 1)
                chunks.append(data)
            else:
                chunks.append(line)
                
        return method, chunks

def rsa_decrypt(cipher_int, d, n):
    """RSA解密实现(带OAEP解填充)"""
    try:
        # RSA解密公式: m = c^d mod n
        m = pow(cipher_int, d, n)
        # 转换为字节
        decrypted = m.to_bytes((n.bit_length() + 7) // 8, 'big')
        
        # OAEP解填充实现
        def mgf1(seed, mask_len, hash_func=hashlib.sha256):
            """MGF1掩码生成函数"""
            counter = 0
            output = bytearray()
            while len(output) < mask_len:
                C = seed + struct.pack(">I", counter)
                output.extend(hash_func(C).digest())
                counter += 1
            return bytes(output[:mask_len])
        
        # OAEP解填充参数
        hash_len = 32  # SHA-256哈希长度
        k = (n.bit_length() + 7) // 8  # 模数字节长度
        
        if len(decrypted) != k or k < 2 * hash_len + 2:
            raise ValueError("无效的OAEP密文格式")
        
        # 分解数据
        masked_seed = decrypted[1:1 + hash_len]
        masked_db = decrypted[1 + hash_len:]
        
        # 恢复seed
        seed_mask = mgf1(masked_db, hash_len)
        seed = bytes(x ^ y for x, y in zip(masked_seed, seed_mask))
        
        # 恢复DB
        db_mask = mgf1(seed, len(masked_db))
        db = bytes(x ^ y for x, y in zip(masked_db, db_mask))
        
        # 验证lHash
        lhash = hashlib.sha256(b"").digest()  # 空标签
        if db[:hash_len] != lhash:
            raise ValueError("OAEP标签验证失败")
        
        # 查找分隔符
        try:
            sep_pos = db.index(b"\x01", hash_len)
        except ValueError:
            raise ValueError("OAEP格式错误：未找到分隔符")
        
        return db[sep_pos + 1:]  # 返回解填充后的明文
        
    except Exception as e:
        print(f"RSA解密错误: {str(e)}")
        raise

def elgamal_decrypt(chunk, x, p):
    """ElGamal解密"""
    try:
        # 清理数据中的括号和空格
        clean_chunk = chunk.strip().replace('(', '').replace(')', '').replace(' ', '')
        # 分割并转换为整数
        if ',' not in clean_chunk:
            raise ValueError("无效的ElGamal加密数据格式")
        
        c1, c2 = map(int, clean_chunk.split(','))
        # 计算共享密钥s = c1^x mod p
        s = pow(c1, x, p)
        # 计算模逆元s_inv = s^(p-2) mod p (费马小定理)
        s_inv = pow(s, p-2, p)
        # 计算明文m = c2 * s_inv mod p
        m = (c2 * s_inv) % p
        
        # 转换为16字节块(与加密时的chunk_size一致)
        return m.to_bytes(16, 'big')
        
    except Exception as e:
        print(f"ElGamal解密错误: {str(e)}")
        raise

def main():
    # 读取加密文件
    method, chunks = read_encrypted_file('main/data/encrypt.txt')
    if not method:
        print("无效的加密文件")
        return

    # 获取私钥
    print(f"\n请输入{method}私钥:")
    while True:
        try:
            key_input = input("格式: 参数1,参数2\n").strip()
            # 清理输入中的括号和空格
            key_input = key_input.replace('(', '').replace(')', '').replace(' ', '')
            key_parts = key_input.split(',')
            if len(key_parts) != 2:
                raise ValueError("需要两个参数")
            private_key = tuple(map(int, key_parts))
            break
        except ValueError as e:
            print(f"输入无效: {e}")
            print("请重新输入，示例: 12345,67890 (不要包含括号)")

    # 解密数据
    decrypted = []
    if method == 'RSA':
        d, n = private_key
        for chunk in chunks:
            hex_str = chunk.split('|')[-1].replace('0x', '')
            cipher_int = int(hex_str, 16)
            decrypted.append(rsa_decrypt(cipher_int, d, n))
    elif method == 'ElGamal':
        x, p = private_key
        for chunk in chunks:
            decrypted.append(elgamal_decrypt(chunk, x, p))

    # 写入解密结果
    with open('main/data/decrypt.txt', 'wb') as f:
        f.write(b''.join(decrypted))
    print("解密完成，结果已保存")

if __name__ == "__main__":
    main()
