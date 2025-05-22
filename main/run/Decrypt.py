import os
import math
import hashlib
import struct

def read_encrypted_file(file_path):
    """Read encrypted file, supports multi-line ELGamal|(num1,num2) format"""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('')  # 创建空文件
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if not lines:
            return None, []
            
        # Parse first line to get encryption method
        first_line = lines[0].strip()
        if '|' not in first_line:
            return None, []
            
        method, first_data = first_line.split('|', 1)
        chunks = [first_data]
        
        # Process remaining lines
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
    """RSA decryption implementation (with OAEP unpadding)"""
    try:
        # RSA decryption formula: m = c^d mod n
        m = pow(cipher_int, d, n)
        # Convert to bytes
        decrypted = m.to_bytes((n.bit_length() + 7) // 8, 'big')
        
        # OAEP unpadding
        def mgf1(seed, mask_len, hash_func=hashlib.sha256):
            """MGF1 mask generation function"""
            counter = 0
            output = bytearray()
            while len(output) < mask_len:
                C = seed + struct.pack(">I", counter)
                output.extend(hash_func(C).digest())
                counter += 1
            return bytes(output[:mask_len])
        
        # OAEP unpadding parameters
        hash_len = 32  # SHA-256 hash length
        k = (n.bit_length() + 7) // 8  # Modulus byte length
        
        if len(decrypted) != k or k < 2 * hash_len + 2:
            raise ValueError(" Invalid OAEP ciphertext format")
        
        # Split data
        masked_seed = decrypted[1:1 + hash_len]
        masked_db = decrypted[1 + hash_len:]
        
        # recover seed
        seed_mask = mgf1(masked_db, hash_len)
        seed = bytes(x ^ y for x, y in zip(masked_seed, seed_mask))
        
        # recover DB
        db_mask = mgf1(seed, len(masked_db))
        db = bytes(x ^ y for x, y in zip(masked_db, db_mask))
        
        # verify lHash
        lhash = hashlib.sha256(b"").digest()  # empty label hash
        if db[:hash_len] != lhash:
            raise ValueError("OAEP label verification failed")
        
        # Find separator
        try:
            sep_pos = db.index(b"\x01", hash_len)
        except ValueError:
            raise ValueError("OAEP format error: separator not found")
        
        return db[sep_pos + 1:]  # Return unpadded plaintext
        
    except Exception as e:
        print(f"RSA decrypt error: {str(e)}")
        raise

def elgamal_decrypt(chunk, x, p):
    """ElGamal decrypt"""
    try:
        # Clean parentheses and spaces in data
        clean_chunk = chunk.strip().replace('(', '').replace(')', '').replace(' ', '')
        #  Split and convert to integers
        if ',' not in clean_chunk:
            raise ValueError("Invalid ElGamal encrypted data format")
        
        c1, c2 = map(int, clean_chunk.split(','))
        #  Compute shared secret s = c1^x mod p
        s = pow(c1, x, p)
        #  Compute modular inverse s_inv = s^(p-2) mod p (Fermat's Little Theorem)
        s_inv = pow(s, p-2, p)
        # plaintext m = c2 * s_inv mod p
        m = (c2 * s_inv) % p
        
        # Convert to 16-byte blocks (consistent with chunk_size during encryption
        return m.to_bytes(16, 'big')
        
    except Exception as e:
        print(f"ElGamal decrypt error : {str(e)}")
        raise

def main():
    # read encrypted file
    method, chunks = read_encrypted_file('main/data/encrypt.txt')
    if not method:
        print("Invalid encrypted file")
        return

    # 获取私钥
    print(f"\nplease input {method} private_keys:")
    while True:
        try:
            key_input = input("Format: parameter1,parameter2").strip()
            # clean input
            key_input = key_input.replace('(', '').replace(')', '').replace(' ', '')
            key_parts = key_input.split(',')
            if len(key_parts) != 2:
                raise ValueError("need exactly two parameters")
            private_key = tuple(map(int, key_parts))
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
            print("Please re-enter, example: 12345,67890 (without parentheses)")

    # Decrypt data
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

    # Write decrypted result
    output_path = 'main/data/decrypt.txt'
    output_dir = os.path.dirname(output_path)
    if output_dir:  #  If path contains directory
        os.makedirs(output_dir, exist_ok=True)
    
    with open(output_path, 'wb') as f:
        f.write(b''.join(decrypted))
    print("Decryption completed, result saved")

if __name__ == "__main__":
    main()
