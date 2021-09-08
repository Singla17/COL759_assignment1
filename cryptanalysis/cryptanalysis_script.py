# -*- coding: utf-8 -*-
"""
COL759 Assigtnment-1
Cryptanalysis Script

Somanshu Singla 2018EE10314
Lakshya Tangri 2018EE10222
"""

import numpy as np
from numpy.linalg import inv

def decrypt(K,cipher_text,cipher_text_length):
    try:
        K_inv = inv(K)
        det_key = np.linalg.det(K)
        K_inv = K_inv * det_key
        K_inv = np.round_(K_inv)             ## getting modulo inverse of key
        K_inv = K_inv.astype(int)
        det_key = round(det_key)
        inv_det = pow(det_key,-1,26)
        K_inv = K_inv * inv_det
        K_inv = K_inv % 26
    except:
        return 

    
    key_length = np.shape(K)[0]
    
    
    
    
    cipher_text_chunks = []
    num_chunks = int(cipher_text_length/key_length)
    for chunk in range(num_chunks):
        cipher_text_chunks.append(cipher_text[(chunk*key_length):((chunk+1)*key_length)])
        
    ## Decryption
    plain_text = ''
    for chunk in range(num_chunks):
        text = cipher_text_chunks[chunk]
        text_as_array = np.zeros(key_length,dtype=int)
        for i in range(key_length):
            char_of_text = text[i]
            ascii_char = ord(char_of_text)
            ascii_char -= 65
            text_as_array[i]= ascii_char
        
        plain_text_array = np.matmul(K_inv,text_as_array)
        plain_text_array = plain_text_array.astype('int')
        plain_text_array = plain_text_array % 26
        for i in range(key_length):
            char_as_int = plain_text_array[i]
            char_as_int += 65
            plain_text += chr(char_as_int)
                    
    return plain_text


def getIOC(text):
    text = ''.join(filter(str.isalpha,text))  ## removes everything except [A-Z]
    text_len = len(text)
    text = text.upper()

    freq={}
    for char in text:
        if(freq.get(char)):
            freq[char]+=1
        else:
            freq[char]=1
    ioc=0
    for key in freq.keys():
        ioc+=(freq[key]*(freq[key]-1))
    ioc /= ((text_len)*(text_len-1))
    return ioc




cipher_text_file = open("Cipher_Text.txt",'r')
cipher_text = cipher_text_file.read() ## reading complete file at once
cipher_text = ''.join(filter(str.isalpha,cipher_text))  ## removes everything except [A-Z]
cipher_text_length = len(cipher_text)
cipher_text = cipher_text.upper()


partial_plain_text_file = open("Partial_Plain_Text.txt","r")
partial_plain_text = partial_plain_text_file.read()
partial_plain_text = ''.join(filter(str.isalpha,partial_plain_text)) 
partial_plain_text = partial_plain_text.upper()

partial_cipher_text_file = open("Partial_Cipher_Text.txt",'r')
partial_cipher_text = partial_cipher_text_file.read() ## reading complete file at once
partial_cipher_text = ''.join(filter(str.isalpha,partial_cipher_text))  ## removes everything except [A-Z]
partial_cipher_text = partial_cipher_text.upper()



key_size = np.linspace(2,10,9)
key_size = key_size.astype(int)
ioc_map = {}

for size in key_size:
    plain_ascii = np.zeros(size*size,dtype=int)
    cipher_ascii = np.zeros(size*size,dtype=int)
    
    start_index=0
    inverse_exists = False
    max_iteration = int((len(partial_cipher_text) - (size*size))/size)+1
    number_of_iterations = 0
    
    
    while inverse_exists is False and number_of_iterations<max_iteration:
        for i in range(start_index,(size*size)+start_index):
            plain_ascii[i-start_index]=((ord(partial_plain_text[i])-65))
            cipher_ascii[i-start_index]=((ord(partial_cipher_text[i])-65))
        
        
        
        plain_ascii = plain_ascii.reshape((size,size))
        plain_ascii = plain_ascii.T
        cipher_ascii = cipher_ascii.reshape((size,size))
        cipher_ascii = cipher_ascii.T
        
        
        try:
            plain_inv = inv(plain_ascii)
            det_plain = np.linalg.det(plain_ascii)
            plain_inv = plain_inv * det_plain
            plain_inv = np.round_(plain_inv)             ## getting modulo inverse of plain text matrix
            plain_inv = plain_inv.astype(int)
            det_plain = round(det_plain)
            inv_det = pow(det_plain,-1,26)
            plain_inv = plain_inv * inv_det
            plain_inv = plain_inv % 26
            inverse_exists = True
            
        except:
            inverse_exists = False
            start_index += size
            plain_ascii = np.zeros(size*size,dtype=int)
            cipher_ascii = np.zeros(size*size,dtype=int)
            number_of_iterations +=1 
        
    
    if inverse_exists:
        key = np.matmul(cipher_ascii,plain_inv)
        key = key % 26
        plain_text = decrypt(key,cipher_text,len(cipher_text))
        if plain_text is not None:
            ioc = getIOC(plain_text)
            ioc_map[size]= (ioc,key)
            
minimum_ioc_diff = 1
key_output = None
key_size_output = 10   

for key_size in sorted(list(ioc_map.keys())):
    ioc_val = ioc_map[key_size][0]      
    abs_diff = abs(0.0667-ioc_val)
    if abs_diff < minimum_ioc_diff:
        minimum_ioc_diff = abs_diff
        key_output = ioc_map[key_size][1]
        key_size_output = key_size
        
np.savetxt("Key.csv",key_output,delimiter=',')
    
partial_plain_text_file.close()
partial_cipher_text_file.close()
cipher_text_file.close()