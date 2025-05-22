
# key_generation_time 

| method | key_length | average_time / seconds |  
| --- | --- | --- |  
|RSA|2048|2.1136|  
|RSA|3072|12.1465|   
|RSA|4096|24.5214 |   
|ELGamal|512|18.7785 |  
|ELGamal|1024|102.0038|  
|ELGamal|2048| ---- |  


## 复杂度研究和解释



# encrypt and decrypt time and memeory usage  

RSA_keylength = 2048  
ELGamal_keylength = 512   
To control variables, we used fixed public and private keys for encryption and decryption tests.
## short_text   
### RSA 
| method | text length（bytes） | encrypt time（s） | dycrypt time（s） |
|----------|-----------------|---------------|---------------|
| RSA   | 7               | 0.042413      | 0.000362      |
| RSA   | 12              | 0.044600      | 0.000438      |
| RSA   | 18              | 0.045430      | 0.000419      |
| RSA   | 23              | 0.042528      | 0.000387      |
| RSA   | 28              | 0.044264      | 0.000405      |
| RSA   | 43              | 0.043995      | 0.000393      |
| RSA   | 58              | 0.043651      | 0.000391      |
| RSA   | 116             | 0.044062      | 0.000581      |
| RSA   | 174             | 0.044175      | 0.000402      |


In RSA algorithm, plaintext is padded with OAEP for semantic security during encryption. Therefore, in short-text tests, the lengths of the parts involved in encryption calculations are similar, resulting in similar encryption and decryption times.

### ELGamal

| method | bytes | encrypt time（s） | decrypt time（s） |
|----------|--------|--------------|--------------|
|  ELGamal   | 7      | 0.002098     | 0.001164     |
|  ELGamal   | 12     | 0.002163     | 0.001154     |
|  ELGamal   | 18     | 0.002142     | 0.001157     |
|  ELGamal   | 23     | 0.002136     | 0.001165     |
|  ELGamal   | 28     | 0.002749     | 0.001154     |
|  ELGamal   | 43     | 0.002147     | 0.001144     |
|  ELGamal   | 58     | 0.002136     | 0.001145     |


## long_text 

| method | oringinal/ kb | final/ kb | encrypt time | dycrypt time |
| ------ | ------------- | --------- | ---- | ----- | 
| RSA | 6 | 25 | 2.01 seconds | 3.16 |
| RSA | 66 | 288 | 23.83 seconds | 8.91 |
| RSA | 652 | 2875 | 240.74 seconds | 69.03 |
| ELGamal | 60 | 376 | 2.51 seconds | 14.97 |
| ELGamal | 598 | 3754 | 24.63 seconds |  122.23 |
| ELGamal | 5975 | 37539 | 250.96  seconds | 897.35 |  


In this part of the test results, both the time and memory usage are in a positive proportional relationship with the original file size. This is because we performed segmentation processing on the original file to achieve encryption of large amounts of data.

