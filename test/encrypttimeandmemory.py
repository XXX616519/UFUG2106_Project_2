import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ElGamal.ElGamal import ElGamalKeyGenerator, ElGamal

# Generate 512-bit ElGamal keys
ELG_public_key = (11936966245886666310355597323468895655388895234025558571267960693264548662380542246089231939171623902721066455718445462299544950000439465893723685135296959, 11499825327589751345662729089808977934486585081590504608618955325081184140789034122870410506967384387048332706469724117339704785834768792055352263627902522, 2703982250158194427441560695163390911009446668861957312868532114059975088512964928565678379359482645322522579819261315928979284437240480724648460907085880)
ELG_private_key = 8164016195568216788392026341181978242313002272846305206316993751909298472582201585403731230072151332698517788491442990089266455287443400535168658271699231
elgamal = ElGamal(public_key=ELG_public_key, private_key=ELG_private_key)
def read_file_content(file_path):
    """Read raw binary file content"""
    with open(file_path, 'rb') as f:
        return f.read()

def write_encrypted(encrypted, output_path):
    """Write encrypted data to file"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        for chunk in encrypted:
            f.write(f"{chunk}\n")

def process_data(data, elgamal):
    """Process data using ElGamal encryption"""
    chunk_size = 50  # ElGamal chunk size
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    return [elgamal.encrypt(chunk) for chunk in chunks]


if __name__ == "__main__":
    # File paths
    start_time = time.time()
    data_path = os.path.join('test', 'data.txt')
    encrypt_path = os.path.join('test', 'encyption.txt')
    
    # Read and encrypt data
    data = read_file_content(data_path)
    encrypted = process_data(data, elgamal)
    
    # Write encrypted data
    write_encrypted(encrypted, encrypt_path)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Encryption time: {elapsed_time:.2f} seconds")
    print(f"Encryption completed. Results saved to {encrypt_path}")
