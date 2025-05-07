# 短文本测试和参数，准备做填充

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
from RSA.rsa import RSAKeyGenerator
from RSA.rsa import RSA
# 参数
TEST_ROUNDS = 10
KEY_LENGTH = 2048

# 时间
keygen_start = time.time()
public_key, private_key = RSAKeyGenerator.generate_keypair(bit_length=KEY_LENGTH)
keygen_time = time.time() - keygen_start

# RSA实例
encryptor = RSA(public_key=public_key)
decryptor = RSA(public_key=public_key, private_key=private_key)

# 测试数据
test_data = "I love you".encode('utf-8')

# 执行加密测试
encrypt_times = []
for _ in range(TEST_ROUNDS):
    start = time.time()
    ciphertext = encryptor.encrypt(test_data)
    encrypt_times.append(time.time() - start)

# 解密
decrypt_times = []
for _ in range(TEST_ROUNDS):
    start = time.time()
    decrypted_text = decryptor.decrypt(ciphertext)
    decrypt_times.append(time.time() - start)

# 计算结果指标
avg_encrypt = sum(encrypt_times)/TEST_ROUNDS
avg_decrypt = sum(decrypt_times)/TEST_ROUNDS

# 输出性能报告
print("\nRSA 性能测试报告")
print("="*40)
print(f"密钥长度: {KEY_LENGTH} bits")
print(f"测试轮次: {TEST_ROUNDS}")
print(f"密钥生成时间: {keygen_time:.4f}s")
print(f"单次加密平均时间: {avg_encrypt:.6f}s (±{max(encrypt_times)-min(encrypt_times):.6f}s)")
print(f"单次解密平均时间: {avg_decrypt:.6f}s (±{max(decrypt_times)-min(decrypt_times):.6f}s)")
print("="*40)
