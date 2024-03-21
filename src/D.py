# Codigo utilizado para alinea D (SHA-256)
import matplotlib.pyplot as plt
import seaborn as sns
from cryptography.hazmat.primitives import hashes
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


# genarates de hash with SHA-256
def sha256(plaintext):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(bytes(plaintext,"utf-8")) #changed to utf-8 to accept more characters than ascii
    hashed_value = digest.finalize()
    # print(hashed_value.hex)
    return hashed_value.hex()

# receives input_file and n which is the number of times
# we should measure the generation
def alinea_d(input_file,n):
    #do decode to turn into a string (because e read the file in binary form , rb)
    text_to_cypher = read(input_file).decode() 
    if text_to_cypher is None:
        return
    
    # generation measurements
    generation_measurements = 0
    generation_time = timeit.timeit(lambda:sha256(text_to_cypher),number=1)
    #repeat n times 
    for _ in range (n):
        # measure the generation time 
        generation_time = timeit.timeit(lambda:sha256(text_to_cypher),number=1)

        #add generation time 
        generation_measurements += generation_time

    # Calculate the average time for generation 
    generation_measurements /= n

    return(generation_measurements)


##TODO ADICIONAR DESCRIÇÃO
def plots(generation_times,):
    x_val =[None]*7
    for i in range(7):
        x_val[i] = i

    #x_val = [x[0]/8 for x in encryption_times]
    y_val = [x[1] for x in generation_times]

    plt.plot(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    plt.show()
    return

# Note: we consider that 1000 measurements are statistically sufficient to have 
# statistically significant results.   
def do_test_for_SHA256():
    current_directory = os.getcwd()
    i = 8

    #Array that save the Average time of generation ,for each test file,  
    generation_measurements =[]

    while (i <= 2097152):

        # current test file name 
        test_file = str(i) + ".txt"

        # path to text file with i bytes 
        file_path = os.path.join(current_directory,"test-files",test_file)

        #do measurements of current test file and save the results to respectiv variables
        generation_time =alinea_d(file_path,1000)

        #append the result generation array
        generation_measurements.append((i, generation_time))
        
        #move on to next test file       
        i *= 8

    # makes the plot with obtained measurements 
    plots(generation_measurements)

#Starts the test for SHA256
do_test_for_SHA256()