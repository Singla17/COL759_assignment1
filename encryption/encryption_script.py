# -*- coding: utf-8 -*-
"""
COL759 Assigtnment-1
Encryption Script

Somanshu Singla 2018EE10314
Lakshya Tangri 2018EE10222
"""
import pandas as pd
import numpy as np


## Key Reading
K = pd.read_csv('key.csv',header=None)
K = K.to_numpy()
K = K.astype('int')
key_length = np.shape(K)[0]


## Plain Text Processing
plain_text_file = open("Plain_Text.txt",'r')
plain_text = plain_text_file.read() ## reading complete file at once
plain_text = ''.join(filter(str.isalpha,plain_text))  ## removes everything except [A-Z]
plain_text_length = len(plain_text)
remainder = plain_text_length % key_length
plain_text = plain_text.upper()
if remainder != 0 :
    num_chars_to_be_added = key_length - remainder
    for i in range(num_chars_to_be_added):
        plain_text += 'X' 
        
plain_text_length = len(plain_text)       
plain_text_chunks = []
num_chunks = int(plain_text_length/key_length)

for chunk in range(num_chunks):
    plain_text_chunks.append(plain_text[int((chunk*key_length)):int(((chunk+1)*key_length))])

## Encyrption
ciphered_string = ''
for chunk in range(num_chunks):
    text = plain_text_chunks[chunk]
    text_as_array = np.zeros(key_length,dtype=int)
    for i in range(key_length):
        char_of_text = text[i]
        ascii_char = ord(char_of_text)
        ascii_char -= 65
        text_as_array[i]= ascii_char
    
    cipher_text = np.matmul(K,text_as_array)
    cipher_text = cipher_text % 26
    for i in range(key_length):
        char_as_int = cipher_text[i]
        char_as_int += 65
        ciphered_string += chr(char_as_int)
    
plain_text_file.close()
output_file = open("Cipher_Text.txt",'w')
output_file.write(ciphered_string)
output_file.close()