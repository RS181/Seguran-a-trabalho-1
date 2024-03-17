# Codigo utilizado para alinea B (AES)
# TODO verificar se tempo esta a ser medido de forma correta
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from os import urandom
from binascii import hexlify
import timeit
import os

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
# we should measure encrypt and decrypt .Stores the results 
# in output_result
def alinea_b(input_file,n,output_result):
    text_to_cypher = read(input_file)
    if text_to_cypher is None:
        return

    key = urandom(32) # 256-bit key 
    nonce = urandom(16) 

    #Arrays that hold encryption and decryption times measurements
    encryption_measurements = 0
    decryption_measurements = 0

    #repeat n times
    for _ in range(n):
        #measure the time for encryption
        encryption_time = timeit.timeit(lambda:encrypt(key,nonce,text_to_cypher),number=1)
        encryption_measurements += encryption_time

        #encrypt the text 
        ciphertext = encrypt(key,nonce,text_to_cypher)
        
        #measure the time for decryption
        decryption_time = timeit.timeit(lambda:decrypt(key,nonce,ciphertext),number=1)
        decryption_measurements += decryption_time

        #decrypt the text 
        plaintext = decrypt(key, nonce, ciphertext)
    encryption_measurements /= n
    decryption_measurements /= n
    return(encryption_measurements,decryption_measurements)
    plots(encryption_measurements,decryption_measurements)
    #save the result to output_result
    save_data_to_file(output_result,encryption_measurements,decryption_measurements)
   
def plots(encryption_times,decryption_times):
    x_val =[None]*7
    for i in range(7):
        x_val[i] = i

    #x_val = [x[0]/8 for x in encryption_times]
    y_val = [x[1] for x in encryption_times]

    plt.plot(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    plt.show()
    #x_val = [x[0]/8 for x in decryption_times]
    y_val = [x[1] for x in decryption_times]
    plt.plot(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    plt.show()
    return
    plt.figure(figsize=(10,5))
    sns.scatterplot(encryption_times)
    plt.show()
    plt.figure(figsize=(10,5))
    sns.scatterplot(decryption_times)
    plt.show()
#saves the measurments made to a file 
def save_data_to_file (filename,encryption_times,decryption_times):
    try: 
        with open(filename,"w") as f:
            f.write(f"Encryption times:{encryption_times}\n")
            f.write(f"Decryption times:{decryption_times}\n")
        print (f"Data saved successfuly to {filename}")
    except Exception as e:
        print(f"Error saving data to {filename}:{e}")




#specify the file and number of times to measure encrypt and decrypt
# Note: we consider that 100 measurements are statistically sufficient to have 
# statistically significant results.   
def do_test_for_AES(): 
    current_directory = os.getcwd()
    i = 8
    encryption_measurements = []
    decryption_measurements = []
    while (i <= 2097152):
        # current test file name 
        test_file = str(i) + ".txt"
        #path tp text file for encription
        file_path = os.path.join(current_directory,"test-files",test_file)
        #path to text file to save results
        output_result = os.path.join(current_directory,"out","AES",test_file)

        #do measurements and save the results 
        encryption_time,decryption_time =alinea_b(file_path,1000,output_result)
        encryption_measurements.append((i,encryption_time))
        decryption_measurements.append((i,decryption_time))
        i *= 8
    plots(encryption_measurements,decryption_measurements)
        

do_test_for_AES()