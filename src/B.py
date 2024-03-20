# Codigo utilizado para alinea B (AES)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from os import urandom
from binascii import hexlify
import timeit
import os

#reads the contens of file an returns the string
# or None if error ocurred 
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

    # Variables that will hold the Sum of all encryption and decription measurements 
    encryption_measurements = 0
    decryption_measurements = 0

    #repeat n times
    for _ in range(n):

        #measure the time for encryption
        encryption_time = timeit.timeit(lambda:encrypt(key,nonce,text_to_cypher),number=1)
        
        #add encryption time 
        encryption_measurements += encryption_time

        #encrypt the text 
        ciphertext = encrypt(key,nonce,text_to_cypher)
        
        #measure the time for decryption
        decryption_time = timeit.timeit(lambda:decrypt(key,nonce,ciphertext),number=1)
        
        #add decryption time 
        decryption_measurements += decryption_time

        #decrypt the text 
        #plaintext = decrypt(key, nonce, ciphertext)

    # Calculate the average time for encryption and decription 
    encryption_measurements /= n
    decryption_measurements /= n
    
    return(encryption_measurements,decryption_measurements)

##TODO ADICIONAR DESCRIÇÃO
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


# Note: we consider that 1000 measurements are statistically sufficient to have 
# statistically significant results.   
def do_test_for_AES(): 
    current_directory = os.getcwd()
    i = 8
    
    #Arrays that save the Average time ,for each test file, to encrypt and decrypt respectively 
    encryption_measurements = []
    decryption_measurements = []

    while (i <= 2097152):
        # current test file name 
        test_file = str(i) + ".txt"

        #path to text file with i bytes 
        file_path = os.path.join(current_directory,"test-files",test_file)

        #do measurements of current test file and save the results to respectiv variables
        encryption_time,decryption_time =alinea_b(file_path,1000)
        
        #append the results to the respectiv array
        encryption_measurements.append((i,encryption_time))
        decryption_measurements.append((i,decryption_time))
        
        #move on to next test file
        i *= 8
    
    # makes the plot with obtained measurements 
    plots(encryption_measurements,decryption_measurements)
        

#Starts the test for AES
do_test_for_AES()