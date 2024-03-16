# Codigo utilizado para alinea C (RSA)
# IMPORTANTE: não consideramos para os tempos  a geração da chave privada
# TODO verificar se tempo esta a ser medido de forma correta
import matplotlib.pyplot as plt
import seaborn as sns
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization,hashes
import os
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


#generate a private key 
def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048, #2048 bits 
    )
    return private_key

# Encrypts a certain message with the public key (obtained with the private key) 
def encrypt(public_key,message):
    #This portion was taken from documentation
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
    #This portion was taken from documentation
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
# we should measure encrypt and decrypt .Stores the results 
# in output_result
def alinea_c(input_file,n,output_result):
    text_to_cypher = read(input_file)
    if text_to_cypher is None:
        return
    
    #Arrays that hold encryption and decryption times measurements
    encryption_measurements = []
    decryption_measurements = []


    #repeat n times 
    for _ in range(n):
        #measure the time for encryption
        encryption_time = timeit.timeit(lambda:encrypt(public_key,text_to_cypher),number =1)
        encryption_measurements.append(encryption_time)

        #encrypt the text
        ciphertext = encrypt(public_key,text_to_cypher)

        #measure the time for decryption
        decryption_time = timeit.timeit(lambda:decrypt(private_key,ciphertext),number=1)
        decryption_measurements.append(decryption_time)

        #decrypt the text 
        plaintext = decrypt(private_key,ciphertext)
    plots(encryption_measurements,decryption_measurements)
    #save the result to output_result
    save_data_to_file(output_result,encryption_measurements,decryption_measurements)

def plots(encryption_times,decryption_times):
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
def do_test_for_RSA(): 
    current_directory = os.getcwd()
    i = 2
    while (i <= 128):
        # current test file name 
        test_file = str(i) + ".txt"
        #path tp text file for encription
        file_path = os.path.join(current_directory,"test-files",test_file)
        #path to text file to save results
        output_result = os.path.join(current_directory,"out","RSA",test_file)

        #do measurements and save the results 
        alinea_c(file_path,1000,output_result)
        i *= 2


#generate the pair of RSA keys
private_key = generate_private_key()
public_key = private_key.public_key()


do_test_for_RSA()
