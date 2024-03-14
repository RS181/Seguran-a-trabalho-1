# Codigo utilizado para alinea B (AES)

from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from os import urandom
from binascii import hexlify
import timeit

#reads the contens of file an returns the string
# or 0 if error ocurred 
def read(input_file):
    try:
        with open(input_file,"rb") as f:
            data = f.read()
    except FileNotFoundError:
        print("Ficheiro " + input_file + " não encontrado")
        return None
    return data

#encrypts data (AES algorithm CTR mode)
def encrypt(key,nonce,plaintext):
    cipher = Cipher(algorithms.AES(key),modes.CTR(nonce))
    encryptor = cipher.encryptor()
    cyphertext = encryptor.update (plaintext) + encryptor.finalize()
    return cyphertext

#decrypts data (AES algorithm CTR mode)
def decrypt(key,nonce,ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext



# receives input_file and n which is the number of times
# we should measure encrypt and decrypt
def alinea_b(input_file,n):
    text_to_cypher = read(input_file)
    if text_to_cypher is None:
        return

    key = urandom(32) # 256-bit key 
    nonce = urandom(16) 

    #Arrays that hold encription and decription times 
    encryption_times = []
    decryption_times = []

    #repeat n times
    for _ in range(n):
        #measure the time for encryption
        encryption_time = timeit.timeit(lambda:encrypt(key,nonce,text_to_cypher),number=1)
        encryption_times.append(encryption_time)

        #encrypt the text 
        ciphertext = encrypt(key,nonce,text_to_cypher)
        
        #measure thte time for decryption
        decryption_time = timeit.timeit(lambda:encrypt(key,nonce,ciphertext),number=1)
        decryption_times.append(decryption_time)

        #decrypt the text 
        plaintext = decrypt(key, nonce, ciphertext)

    #show the results (with an f-string)
    print(f"Encryption times: {encryption_times}")
    print(f"Decryption times: {decryption_times}")
   


#specify the file and number of times to measure encrypt and decrypt
# Note: we consider that 100 measurements are statistically sufficient to have 
# statistically significant results.
alinea_b("Seguranca-trabalho-1\\test-files\\64.txt",100)
        