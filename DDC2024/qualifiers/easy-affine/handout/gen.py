#!/usr/bin/env python
import random
import binascii

def gcd(x, y):
    while(y):
       x, y = y, x % y
    return abs(x)

def affine_encrypt(text, a, b):
    result = 0
    for letter in text.encode("ascii"):
        c = (a*letter + b) % m
        result = (result << 8) + c
    return hex(result)

if __name__ == '__main__':
    with open('flag.txt', 'r') as file:
    	plaintext = file.read().replace('\n', '')

    m = 256
    a = random.randint(1, m)
    while gcd(a, m) != 1:
        a = random.randint(1, m)
    b = random.randint(0, m)

    print("Key = ")
    print((a,b))
    ciphertext = affine_encrypt(plaintext, a, b)

    with open('output.txt', 'w') as file:
        file.write(ciphertext)
