# Codigo utilizado para alinea C (RSA)
# IMPORTANTE: não consideramos para os tempos  a geração da chave privada
import matplotlib.pyplot as plt
import seaborn as sns
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization,hashes
import os
import timeit

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

#generate a private key 
def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048, #2048 bits 
    )
    return private_key

# Encrypts a certain message with the public key (obtained with the private key) 
def encrypt(public_key,message):
    #This portion was taken from documentation cryptography module
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

# Decrypts a ciphered text with the private key (the one that generated the public key used in the 
# encryption)
def decrypt(private_key,ciphertext):
    #This portion was taken from documentation of cryptography module 
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


# receives input_file and n which is the number of times
# we should measure encrypt and decrypt 
def alinea_c(input_file,n):
    text_to_cypher = read(input_file)
    if text_to_cypher is None:
        return
    
    # Variables that will hold the Sum of all encryption and decription measurements 
    encryption_measurements = 0
    decryption_measurements = 0

    encryption_time = timeit.timeit(lambda:encrypt(public_key,text_to_cypher),number =1)

    #repeat n times 
    for _ in range(n):

        #measure the time for encryption
        encryption_time = timeit.timeit(lambda:encrypt(public_key,text_to_cypher),number =1)
        
        #add encryption time 
        encryption_measurements += encryption_time
        
        #encrypt the text
        ciphertext = encrypt(public_key,text_to_cypher)

        #measure the time for decryption
        decryption_time = timeit.timeit(lambda:decrypt(private_key,ciphertext),number=1)
        
        #add decryption time 
        decryption_measurements += decryption_time

        #decrypt the text 
        #plaintext = decrypt(private_key,ciphertext)

    # Calculate the average time for encryption and decription 
    encryption_measurements /= n
    decryption_measurements /= n

    return(encryption_measurements,decryption_measurements)

# Does the plot of encryption and decryption measurements
def plots(encryption_times,decryption_times):
    x_val =[None]*len(encryption_times)
    for i in range(len(encryption_times)):
        x_val[i] = i

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
def do_test_for_RSA(): 
    current_directory = os.getcwd()
    i = 2

    #Arrays that save the Average time ,for each test file, to encrypt and decrypt respectively 
    encryption_measurements = []
    decryption_measurements = []

    while (i <= 128):
        # current test file name 
        test_file = str(i) + ".txt"

        #path to text file with i bytes 
        file_path = os.path.join(current_directory,"test-files",test_file)

        #do measurements of current test file and save the results to respectiv variables
        encryption_time,decryption_time =alinea_c(file_path,1000)

        #append the results to the respectiv array
        encryption_measurements.append((i,encryption_time))
        decryption_measurements.append((i,decryption_time))

        #move on to next test file
        i *= 2
        
    # makes the plot with obtained measurements 
    plots(encryption_measurements,decryption_measurements)


#generate the pair of RSA keys
private_key = generate_private_key()
public_key = private_key.public_key()

#Starts the test for RSA
do_test_for_RSA()
