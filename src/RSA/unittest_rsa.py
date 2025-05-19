import unittest
from rsa import RSAKeyGenerator, RSA
import os
import struct

class TestHighBitRSA(unittest.TestCase):
    """高位数RSA综合测试类（≥2048位）"""
    
    @classmethod
    def setUpClass(cls):
        """生成测试用2048位密钥对"""
        cls.public_key, cls.private_key = RSAKeyGenerator.generate_keypair(bit_length=2048)
        cls.rsa_pub = RSA(cls.public_key)
        cls.rsa_priv = RSA(cls.public_key, cls.private_key)
        
        # 预计算大数测试参数
        cls.max_byte_length = (cls.public_key[1].bit_length() + 7) // 8
        cls.overflow_data = os.urandom(cls.max_byte_length + 1)
        cls.valid_large_data = os.urandom(cls.max_byte_length - 1)

    def test_key_generation_validation(self):
        """测试密钥生成参数验证"""
        # 测试非法位长
        with self.assertRaises(ValueError):
            RSAKeyGenerator.generate_keypair(bit_length=1024)
        
        # 测试非素数输入
        with self.assertRaises(ValueError):
            RSAKeyGenerator.generate_keypair(
                bit_length=2048,
                p=123456,
                q=987654
            )
        
        # 验证自动生成密钥参数
        e, n = self.public_key
        d, _ = self.private_key
        self.assertEqual(e, 65537, "公钥指数应为65537")
        self.assertEqual(n.bit_length(), 2048, "模数位数应为2048位")
        self.assertTrue(0 < d < (n-1), "私钥应在有效范围内")

    def test_encryption_decryption_cycle(self):
        """测试完整加解密流程"""
        test_vectors = [
            b"",                          # 空数据
            b"A",                         # ASCII字符
            os.urandom(50),              # 随机数据（最大支持长度减去填充）
            b"\xFF\x00" * 120,            # 边界字节值组合
            "中文测试".encode('utf-8')     # Unicode数据
        ]
        
        for plaintext in test_vectors:
            with self.subTest(plaintext=plaintext):
                # 将明文转换为整数
                if isinstance(plaintext, str):
                    plaintext = plaintext.encode('utf-8')
                ciphertext = self.rsa_pub.encrypt(plaintext)
                decrypted = self.rsa_priv.decrypt(ciphertext)
                self.assertEqual(plaintext, decrypted, "解密结果应与原始明文一致")

    def test_input_validation(self):
        """测试输入类型及边界验证"""
        # 非法输入类型
        with self.assertRaises(TypeError):
            self.rsa_pub.encrypt(123)  # 整数输入
            
        with self.assertRaises(TypeError):
            self.rsa_pub.encrypt("未编码字符串")

        # 数据长度验证
        with self.assertRaises(ValueError):
            self.rsa_pub.encrypt(self.overflow_data)

        # 密文范围验证
        with self.assertRaises(ValueError):
            self.rsa_priv.decrypt(self.public_key[1] + 1)  # 超过模数

    def test_custom_prime_operation(self):
        """测试自定义素数模式"""
        # 使用已知安全素数生成密钥
        p = 106697219132480173106064317148705638676529121742557567770857687729397446898790451577487723991083173010242416863238099716044775658681981821407922722052778958942891831033512463262741053961681512908218003840408526915629689432111480588966800949428079015682624591636010678691927285321708935076221951173426894836169
        q = 144819424465842307806353672547344125290716753535239658417883828941232509622838692761917211806963011168822281666033695157426515864265527046213326145174398018859056439431422867957079149967592078894410082695714160599647180947207504108618794637872261572262805565517756922288320779308895819726074229154002310375209
   
        pub, priv = RSAKeyGenerator.generate_keypair(
            bit_length=2048,
            p=p,
            q=q
        )
        
        # 验证密钥参数
        self.assertEqual(pub[1], p*q, "模数应为素数乘积")
        self.assertEqual(pub[0], 65537, "公钥指数应为65537")
        
        # 验证加密解密功能
        test_data = b"Custom primes test"
        cipher = RSA(pub).encrypt(test_data)
        decrypted = RSA(pub, priv).decrypt(cipher)
        self.assertEqual(test_data, decrypted.rstrip(b'\x00'))

    def test_partial_decryption(self):
        """测试私钥不可用时的防护"""
        # 未提供私钥时尝试解密
        with self.assertRaises(RuntimeError):
            self.rsa_pub.decrypt(123456)

        # 错误私钥尝试解密
        # 检查结果是否相同
        wrong_priv = (self.private_key[0]+1, self.private_key[1])
        wrong_rsa = RSA(self.public_key, wrong_priv)
        cipher = self.rsa_pub.encrypt(b"test")
        wrong_rsa.decrypt(cipher)
        self.assertNotEqual(cipher, wrong_rsa.decrypt(cipher), "错误私钥解密结果应与原密文不同")

if __name__ == '__main__':
    unittest.main(verbosity=2)