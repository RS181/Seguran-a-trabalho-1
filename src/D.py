# Codigo utilizado para alinea D (SHA-256)
# TODO verificar se tempo esta a ser medido de forma correta
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
# we should measure encrypt and decrypt .Stores the results 
# in output_result
def alinea_d(input_file,n,output_result):
    #do decode to turn into a string (because e read the file in binary form , rb)
    text_to_cypher = read(input_file).decode() 
    if text_to_cypher is None:
        return
    
    # generation measurements
    generation_measurements = 0
    #repeat n times 
    for _ in range (n):
        # measure the genaration time 
        generation_time = timeit.timeit(lambda:sha256(text_to_cypher),number=1)
        generation_measurements += generation_time
    generation_measurements /= n
    return(generation_measurements)
    plots(generation_measurements)
    save_data_to_file(output_result,generation_measurements)
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
    plt.figure(figsize=(10,5))
    sns.scatterplot(generation_times)
    plt.show()


#saves the measurments made to a file 
def save_data_to_file (filename,generation_times):
    try: 
        with open(filename,"w") as f:
            f.write(f"Generation times:{generation_times}\n")
        print (f"Data saved successfuly to {filename}")
    except Exception as e:
        print(f"Error saving data to {filename}:{e}")

#specify the file and number of times to measure encrypt and decrypt
# Note: we consider that 100 measurements are statistically sufficient to have 
# statistically significant results.
def do_test_for_SHA256():
    current_directory = os.getcwd()
    i = 8
    generation_measurements =[]
    while (i <= 2097152):
        # current test file name 
        test_file = str(i) + ".txt"
        #path tp text file for encription
        file_path = os.path.join(current_directory,"test-files",test_file)
        #path to text file to save results
        output_result = os.path.join(current_directory,"out","SHA",test_file)
        generation_time =alinea_d(file_path,1000,output_result)
        generation_measurements.append((i, generation_time))
        
        #do measurements and save the results 
        i *= 8
    plots(generation_measurements)


do_test_for_SHA256()