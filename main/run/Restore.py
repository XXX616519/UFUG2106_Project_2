import os

def detect_file_type(data):
    """Enhanced file type detection"""
    # Common file type signatures
    signatures = {
        'png': b'\x89PNG\r\n\x1a\n',
        'jpg': b'\xFF\xD8\xFF',
        'gif': b'GIF89a',
        'mp3': b'ID3',
        'mp4': b'ftypmp42',
        'zip': b'PK\x03\x04',
        'pdf': b'%PDF-'
    }
    
    # Check for known file types
    for ext, sig in signatures.items():
        if len(data) >= len(sig) and data.startswith(sig):
            return ext
    
    # Check if text file
    try:
        if data.decode('utf-8').isprintable():
            return 'txt'
    except UnicodeDecodeError:
        pass
    
    # Check if Windows executable
    if len(data) > 2 and data[:2] == b'MZ':
        return 'exe'
        
    return None

def compare_files(file1, file2):
    """Compare if two files have identical content"""
    if not os.path.exists(file1):
        with open(file1, 'wb') as f:
            f.write(b'')  # 创建空文件
    if not os.path.exists(file2):
        with open(file2, 'wb') as f:
            f.write(b'')  # 创建空文件
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            content1 = f1.read()
            content2 = f2.read()
            
            if content1 == content2:
                print("Verification passed: Decrypted file matches original file exactly")
                return True
            else:
                print("Verification failed: Decrypted file does not match original file")
                print(f"Original file size: {len(content1)} bytes")
                print(f"Decrypted file size: {len(content2)} bytes")
                
                # Find first position of difference
                for i, (b1, b2) in enumerate(zip(content1, content2)):
                    if b1 != b2:
                        print(f"First difference at byte position {i}: Original={hex(b1)}, Decrypted={hex(b2)}")
                        break
                return False
    except FileNotFoundError as e:
        print(f"File comparison failed: {str(e)}")
        return False

def restore_file():
    """Restore decrypted bytes to original file format"""
    decrypt_file = 'main/data/decrypt.txt'
    original_file = 'main/data/data.txt'
    output_dir = 'main/data/output_file'
    
    # Verify decryption but continue restoration anyway
    compare_files(original_file, decrypt_file)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Read decrypted binary data
        with open(decrypt_file, 'rb') as f:
            data = f.read()
        
        # Auto-detect file type
        file_type = detect_file_type(data)
        if file_type is None:
            print("Could not automatically identify file type. Please check file format.")
            return
        
        # Generate output file name
        output_path = os.path.join(output_dir, f'restored.{file_type}')
        
        # Write file
        if file_type == 'txt':
            # Try multiple encodings
            encodings = ['utf-8', 'gbk', 'iso-8859-1']
            for enc in encodings:
                try:
                    text = data.decode(enc)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"Successfully restored text file: {output_path}")
                    print(f"Content preview:\n{text[:200]}{'...' if len(text)>200 else ''}")
                    return
                except UnicodeDecodeError:
                    continue
            
            # Save as raw binary if decoding fails
            with open(output_path, 'wb') as f:
                f.write(data)
            print(f"Failed to decode text. Saved raw data to: {output_path}")
        else:
            with open(output_path, 'wb') as f:
                f.write(data)
            print(f"Successfully restored binary file: {output_path}")
            
    except FileNotFoundError:
        print(f"Decrypted file not found: {decrypt_file}")
    except Exception as e:
        print(f"File restoration failed: {str(e)}")
    finally:
        print("File restoration operation completed")

if __name__ == "__main__":
    restore_file()