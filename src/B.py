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
def alinea_b(text_to_cypher,n):
    

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
    x_val =[None]*len(encryption_times)
    for i in range(len(encryption_times)):
        x_val[i] = i

    # decryption graphic plot
    y_val = [x for x in encryption_times]
    plt.plot(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    plt.show()
    # decryption graphic plot
    y_val = [x for x in decryption_times]
    plt.plot(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    plt.show()
    return
def scatter_plot(encryption_times,n):
    plt.figure(figsize=(10,5))
    # n is the file size
    plt.xlabel(n)
    plt.ylabel('Time')
    #plot with all the test for a file size
    sns.scatterplot(encryption_times)
    plt.show()
import random
import string

def generate_random_text(target_size):
    text = ''
    while len(text.encode('utf-8')) < target_size:
        text += ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation + ' ') for _ in range(target_size))
    return text[:target_size]




#specify the file and number of times to measure encrypt and decrypt
# Note: we consider that 100 measurements are statistically sufficient to have 
# statistically significant results.   
def do_test_for_AES(): 
    current_directory = os.getcwd()
    i = 8
    # contem as medias da encriptação/desincriptação para cada ficheiro
    encryption_measurements = []
    decryption_measurements = []
    while (i <= 2097152):
        # current test file name 
        test_file = str(i) + ".txt"
        #path tp text file for encription
        file_path = os.path.join(current_directory,"test-files",test_file)
        #path to text file to save results
        text_to_cypher = read(file_path)
        if text_to_cypher is None:
            return

        #adição dos tempos de encriptção/desicriptção 
        encryption_time,decryption_time =alinea_b(text_to_cypher,1000)
        encryption_measurements.append((encryption_time))
        decryption_measurements.append((decryption_time))
        i *= 8
    plots(encryption_measurements,decryption_measurements)

def random_AES():
    i = 8
    encryption_measurements = []
    decryption_measurements = []
    mean_encryption_time = 0
    mean_decryption_time = 0
    while (i <= 262144):
        for _ in range(100):
            #randomly generated file of size i
            file = generate_random_text(i)
            plaintext = file.encode('utf-8')

            #calcula os tempos de encriptção/desicriptção medios do ficheiro file 
            encryption_time,decryption_time =alinea_b(plaintext,100)
            #esse tempo é adicionada ao sumatorio dos tempos de todos os ficheiros de tamenho i
            mean_encryption_time += encryption_time
            mean_decryption_time += decryption_time
        # calculo das medias
        mean_encryption_time /= 10
        mean_decryption_time /= 10
        # contem as medias da encriptação/desincriptação para cada tamenho de ficheiro
        encryption_measurements.append((mean_encryption_time))
        decryption_measurements.append((mean_decryption_time))
        i *= 8 
    plots(encryption_measurements,decryption_measurements)    
def time_distribution():
    i = 8
    
    while (i <= 262144):
        encryption_measurements = []
        decryption_measurements = []
        for _ in range(100):
            #randomly generated file of size i
            file = generate_random_text(i)
            plaintext = file.encode('utf-8')
            #calcula os tempos de encriptção/desicriptção medios do ficheiro file 
            encryption_time,decryption_time =alinea_b(plaintext,1)
            # contem os tamenhos encriptação/desincriptação para tameho atual
            encryption_measurements.append((encryption_time))
            decryption_measurements.append((decryption_time))
        scatter_plot(encryption_measurements,i)
        i *= 8 

do_test_for_AES()