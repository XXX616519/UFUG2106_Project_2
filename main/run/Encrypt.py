import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.RSA.rsa import RSA, RSAKeyGenerator
from src.ElGamal.ElGamal import ElGamal, ElGamalKeyGenerator

def read_file_content(file_path):
    """Read raw binary file content"""
    with open(file_path, 'rb') as f:
        return f.read()

def write_encrypted(method, encrypted, output_path):
    """Write encrypted data with method prefix"""
    with open(output_path, 'wb') as f:
        if method == 'RSA':
            for chunk in encrypted:
                f.write(f"RSA|{chunk}\n".encode())
        else:  # ElGamal
            for chunk in encrypted:
                f.write(f"ElGamal|{chunk}\n".encode())

def process_data(method, data, public_key):
    """Process data according to encryption method"""
    if method == '1':  # RSA
        chunk_size = 117  # RSA 2048 chunk size
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        # 确保最后一个块补齐到chunk_size
        if len(chunks[-1]) < chunk_size:
            chunks[-1] = chunks[-1] + b'\x00' * (chunk_size - len(chunks[-1]))
        encrypted = []
        for chunk in chunks:
            encrypted_int = public_key.encrypt(chunk)
            encrypted.append(f"0x{encrypted_int:x}")
        return encrypted
    else:  # ElGamal
        chunk_size = 16  # ElGamal chunk size
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        # 确保最后一个块补齐到chunk_size
        if len(chunks[-1]) < chunk_size:
            chunks[-1] = chunks[-1] + b'\x00' * (chunk_size - len(chunks[-1]))
        encrypted = []
        for chunk in chunks:
            c1, c2 = public_key.encrypt(chunk)
            encrypted.append(f"({c1},{c2})")
        return encrypted

import time

def main():
    method = input("Choose encryption method (1 for RSA, 2 for ElGamal): ").strip()
    start_time = time.time()
    
    data_path = os.path.join('main', 'data_file', 'data.txt')
    encrypt_path = os.path.join('main', 'data_file', 'encrpt.txt')
    
    # Read and process input
    data = read_file_content(data_path)
    
    if method == '1':  # RSA
        private_key, public_key = RSAKeyGenerator.generate_keypair(2048)
        rsa = RSA(public_key)
        encrypted = process_data(method, data, rsa)
    elif method == '2':  # ElGamal
        public_key, private_key = ElGamal.create_keypair(512)
        encrypted = process_data(method, data, public_key)
    else:
        print("Invalid choice")
        return
    
    # Write output
    write_encrypted('RSA' if method == '1' else 'ElGamal', encrypted, encrypt_path)
    
    # Output private key in format needed for decryption
    print("\nPrivate Key (save this for decryption):")
    if method == '1':  # RSA
        d, n = private_key
        print(f"RSA私钥格式: d,n")
        print(f"示例: {d},{n}")
    else:  # ElGamal
        print(f"ElGamal私钥对象:")
        print(f"x: {private_key.x}")
        print(f"p: {private_key.p}")
    
    end_time = time.time()
    print(f"\n加密完成，耗时: {end_time - start_time:.2f}秒")

if __name__ == "__main__":
    main()
