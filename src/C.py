# Codigo utilizado para alinea C (RSA)

from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization,hashes

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



#generate the pair of RSA keys
private_key = generate_private_key()
public_key = private_key.public_key()

#message (the prefix b, indicates that the string is a sequence of bytes
#instead of a sequence of characters. If we didn't do this we would get an error)
message = b" mensagem aleatoria"

# Encripting the message 
encrypted_message = encrypt(public_key,message)
print("Mensagem encriptada: ",encrypted_message)

# Decripting the message 
decrypted_message = decrypt(private_key,encrypted_message)
print("Mensagem desencriptada",decrypted_message)

