# definir tudo aqui

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
        return 0
    return data



# receive file with data to encrypt (encrypt using AES)
# saves it with a form ciphertext_i_AES.bin 
# where i is an int 
def alinea_b(input_file):
    text_to_cypher = read(input_file)
    if (text_to_cypher == 0):
        return
    print(text_to_cypher)

    key = urandom(32) # 256-bit key 
    nonce = urandom(16) 

    # we use CTR mode , transforms a block cipher into a stream cipher
    cipher = Cipher(algorithms.AES(key),modes.CTR(nonce))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update (text_to_cypher) + encryptor.finalize()
    print(hexlify(key))
    save(ciphertext,"AES","Seguranca-trabalho-1\out",os.path.basename(input_file).split(".")[0])


    # decrypt:
    decryptor = cipher.decryptor()
    pt = decryptor.update(ciphertext) + decryptor.finalize()
    print(pt)

alinea_b("Seguranca-trabalho-1\\test-files\\2.txt")