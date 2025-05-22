import os

def file_to_bytes(input_path, output_path):
    """Convert file to raw bytes and save"""
    # Verify input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Read file content as bytes
    with open(input_path, 'rb') as f:
        file_bytes = f.read()
    
    # Check and create directory if needed before writing
    output_dir = os.path.dirname(output_path)
    if output_dir:  # If path contains directory
        os.makedirs(output_dir, exist_ok=True)
    
    # Write raw bytes (regardless of file existence)
    with open(output_path, 'wb') as f:
        f.write(file_bytes)

if __name__ == "__main__":
    input_dir = os.path.join('main', 'data', 'input_file')
    output_file = os.path.join('main', 'data', 'data.txt')
    
    # Get first file in input_dir
    files = os.listdir(input_dir)
    if not files:
        os.makedirs(input_dir, exist_ok=True)  # Ensure directory exists
        placeholder_file = os.path.join(input_dir, 'placeholder.txt')
        with open(placeholder_file, 'w') as f:
            f.write('')  # Create placeholder file
        files = [placeholder_file]  # Use placeholder file
    
    input_file = os.path.join(input_dir, files[0])
    file_to_bytes(input_file, output_file)
    
    print(f"Successfully converted {input_file} to bytes and saved to {output_file}")
