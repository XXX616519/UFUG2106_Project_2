import os
import mimetypes

def get_file_type(file_path):
    """自动识别文件类型"""
    # 首先通过扩展名识别
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ('.txt', '.mp3', '.png', '.mp4'):
        return ext[1:]  # 去掉点号
    
    # 如果扩展名不在支持列表中，尝试mimetype识别
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type.startswith('text/'):
            return 'txt'
        elif mime_type == 'audio/mpeg':
            return 'mp3'
        elif mime_type == 'image/png':
            return 'png'
        elif mime_type == 'video/mp4':
            return 'mp4'
    
    raise ValueError(f"不支持的文件类型: {file_path}")

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

def show_as_text(file_path):
    """尝试以文本形式显示文件内容"""
    with open(file_path, 'rb') as f:
        data = f.read()
    
    print("\n字节数据预览:")
    print(f"长度: {len(data)} 字节")
    
    # 尝试多种编码解码
    encodings = ['utf-8', 'gbk', 'iso-8859-1', 'ascii']
    for enc in encodings:
        try:
            text = data.decode(enc)
            print(f"\n使用 {enc} 解码成功:")
            print(text[:200] + ('...' if len(text) > 200 else ''))
            return
        except UnicodeDecodeError:
            continue
    
    print("无法解码为文本，可能是二进制文件")

if __name__ == "__main__":
    input_dir = os.path.join('main', 'data_file', 'input_file')
    output_file = os.path.join('main', 'data_file', 'data.txt')
    
    # 获取input_dir下的第一个文件
    files = os.listdir(input_dir)
    if not files:
        raise FileNotFoundError("input_file目录中没有文件")
    
    input_file = os.path.join(input_dir, files[0])
    file_to_bytes(input_file, output_file)
    
    print(f"成功将 {input_file} 转换为字节串并保存到 {output_file}")
    
    # 显示文本预览
    if input_file.endswith('.txt'):
        show_as_text(output_file)
