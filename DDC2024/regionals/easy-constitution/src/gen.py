#!/usr/bin/env python
"""
Shuffle an alphabet to generate a key for monoalphabetic substitution cipher.
"""
import random

alphabet = 'abcdefghijklmnopqrstuvwxyzæøå'

def shuffled_alphabet():
    alpha_list = list(alphabet)
    random.shuffle(alpha_list)
    s = ''.join(alpha_list)  # funny way to turn list of chars into string
    return s

def monoalphabetic_substitution(text, key):
    alpha_list = list(alphabet)
    result = ""
    for letter in text:
        if letter in alphabet:
            result += key[alphabet.find(letter.lower())]
        else:
            result += letter
    return result

if __name__ == '__main__':
    with open('plain.txt', 'r') as file:
    	plaintext = file.read()
    key = shuffled_alphabet();
    #print("Key = " + key)
    print(monoalphabetic_substitution(plaintext, key))
