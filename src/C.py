# Codigo utilizado para alinea C (RSA)

from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization,hashes
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



def alinea_c(input_file):
    text_to_cypher = read(input_file)
    if text_to_cypher is None:
        return
    encrypted_message = encrypt(public_key,text_to_cypher)
    print("Mensagem encriptada: ",encrypted_message)

    # Decripting the message 
    decrypted_message = decrypt(private_key,encrypted_message)
    print("Mensagem desencriptada",decrypted_message)
    

#generate the pair of RSA keys
private_key = generate_private_key()
public_key = private_key.public_key()

current_directory = os.getcwd()
filepath = os.path.join(current_directory,"test-files","64.txt")
print(filepath)
alinea_c(filepath)
alinea_c(filepath)