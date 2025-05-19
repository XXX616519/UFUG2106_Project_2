import os

def detect_file_type(data):
    """增强版文件类型检测"""
    # 常见文件类型签名
    signatures = {
        'png': b'\x89PNG\r\n\x1a\n',
        'jpg': b'\xFF\xD8\xFF',
        'gif': b'GIF89a',
        'mp3': b'ID3',
        'mp4': b'ftypmp42',
        'zip': b'PK\x03\x04',
        'pdf': b'%PDF-'
    }
    
    # 检查已知文件类型
    for ext, sig in signatures.items():
        if len(data) >= len(sig) and data.startswith(sig):
            return ext
    
    # 检查是否为文本文件
    try:
        if data.decode('utf-8').isprintable():
            return 'txt'
    except UnicodeDecodeError:
        pass
    
    # 检查是否为Windows可执行文件
    if len(data) > 2 and data[:2] == b'MZ':
        return 'exe'
        
    return None

def compare_files(file1, file2):
    """比较两个文件内容是否相同"""
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            content1 = f1.read()
            content2 = f2.read()
            
            if content1 == content2:
                print("验证通过: 解密文件与原始文件内容完全一致")
                return True
            else:
                print("验证失败: 解密文件与原始文件内容不一致")
                print(f"原始文件大小: {len(content1)} 字节")
                print(f"解密文件大小: {len(content2)} 字节")
                
                # 找出第一个不一致的位置
                for i, (b1, b2) in enumerate(zip(content1, content2)):
                    if b1 != b2:
                        print(f"第一个差异在字节位置 {i}: 原始={hex(b1)}, 解密={hex(b2)}")
                        break
                return False
    except FileNotFoundError as e:
        print(f"文件比较失败: {str(e)}")
        return False

def restore_file():
    """将解密后的字节串还原为原始文件"""
    decrypt_file = 'main/data/decrypt.txt'
    original_file = 'main/data/data.txt'
    output_dir = 'main/data/output_file'
    
    # 验证解密是否正确但仍继续恢复
    compare_files(original_file, decrypt_file)
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 读取解密后的二进制数据
        with open(decrypt_file, 'rb') as f:
            data = f.read()
        
        # 自动检测文件类型
        file_type = detect_file_type(data)
        if file_type is None:
            print("无法自动识别文件类型，请检查文件格式")
            return
        
        # 生成输出文件名
        output_path = os.path.join(output_dir, f'restored.{file_type}')
        
        # 写入文件
        if file_type == 'txt':
            # 尝试多种编码解码
            encodings = ['utf-8', 'gbk', 'iso-8859-1']
            for enc in encodings:
                try:
                    text = data.decode(enc)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"成功还原文本文件: {output_path}")
                    print(f"内容预览:\n{text[:200]}{'...' if len(text)>200 else ''}")
                    return
                except UnicodeDecodeError:
                    continue
            
            # 解码失败保存原始二进制
            with open(output_path, 'wb') as f:
                f.write(data)
            print(f"无法解码文本，已保存原始数据到: {output_path}")
        else:
            with open(output_path, 'wb') as f:
                f.write(data)
            print(f"成功还原二进制文件: {output_path}")
            
    except FileNotFoundError:
        print(f"解密文件不存在: {decrypt_file}")
    except Exception as e:
        print(f"文件还原失败: {str(e)}")
    finally:
        print("文件恢复操作已完成")

if __name__ == "__main__":
    restore_file()
