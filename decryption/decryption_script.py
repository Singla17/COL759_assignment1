# -*- coding: utf-8 -*-
"""
COL759 Assigtnment-1
Decryption Script

Somanshu Singla 2018EE10314
Lakshya Tangri 2018EE10222
"""
import numpy as np
import pandas as pd
from numpy.linalg import inv


## Key and Key inverse processing
K = pd.read_csv('key.csv',header=None)
K = K.to_numpy()
K = K.astype('int')
try:
    K_inv = inv(K)
except:
    print(" The Key is non invertible, please correct the key")

det_key = np.linalg.det(K)
K_inv = K_inv * det_key
K_inv = np.round_(K_inv)             ## getting modulo inverse of key
K_inv = K_inv.astype(int)
det_key = round(det_key)
inv_det = pow(det_key,-1,26)
K_inv = K_inv * inv_det
K_inv = K_inv % 26

key_length = np.shape(K)[0]


## Reading and Processing cipher text file
cipher_text_file = open("Cipher_Text.txt",'r')
cipher_text = cipher_text_file.read()
cipher_text = ''.join(filter(str.isalpha,cipher_text))  ## Just a check[should be redundant]
cipher_text_length = len(cipher_text)
if cipher_text_length % key_length !=0:
    print('Please input complete cipher text for decryption')
cipher_text = cipher_text.upper()

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
    
    
cipher_text_file.close()
output_file = open("Plain_Text.txt",'w')
output_file.write(plain_text)
output_file.close()