import os
# 没问题
def file_to_bytes(input_path, output_path):
    """将文件转换为纯字节串并保存"""
    # 验证输入文件存在
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"输入文件不存在: {input_path}")
    
    # 读取文件内容为字节
    with open(input_path, 'rb') as f:
        file_bytes = f.read()
    
    # 直接写入原始字节
    with open(output_path, 'wb') as f:
        f.write(file_bytes)

if __name__ == "__main__":
    input_dir = os.path.join('main', 'data', 'input_file')
    output_file = os.path.join('main', 'data', 'data.txt')
    
    # 获取input_dir下的第一个文件
    files = os.listdir(input_dir)
    if not files:
        raise FileNotFoundError("input_file目录中没有文件")
    
    input_file = os.path.join(input_dir, files[0])
    file_to_bytes(input_file, output_file)
    
    print(f"成功将 {input_file} 转换为字节串并保存到 {output_file}")
