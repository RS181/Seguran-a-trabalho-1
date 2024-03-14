# Codigo utilizado para alinea B

from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from os import urandom
from binascii import hexlify
import timeit
import os 

#save some data into a specified directory
#(we assume that directory exists)
def save(data,type,directory,i):
    with open(os.path.join(directory,"ciphertext_" + str(i) +"_"+ type + ".bin" ),"wb") as cphFile:
        cphFile.write(data)

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


# receive file with data to encrypt (encrypt using AES)
# saves it with a form ciphertext_i_AES.bin 
# where i is an int 
def alinea_b(input_file):
    text_to_cypher = read(input_file)
    if text_to_cypher is None:
        return
    #print(text_to_cypher)

    key = urandom(32) # 256-bit key 
    nonce = urandom(16) 

    #Encryption
    encryption_time = timeit.timeit(lambda:encrypt(key,nonce,text_to_cypher),number=1)
    print(f"Encription time:{encryption_time} seconds" )

    ciphertext = encrypt(key,nonce,text_to_cypher)
    print(ciphertext)

    #Decryption
    decryption_time = timeit.timeit(lambda:encrypt(key,nonce,ciphertext),number=1)
    print(f"Decryption time: {decryption_time} seconds")

    plaintext = decrypt(key,nonce,ciphertext)
    print(plaintext)
   


# repeat(10,"Seguranca-trabalho-1\\test-files\\4.txt")
alinea_b("Seguranca-trabalho-1\\test-files\\4.txt")
        