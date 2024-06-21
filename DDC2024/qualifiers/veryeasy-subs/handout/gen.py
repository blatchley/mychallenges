#!/usr/bin/env python
"""
Shuffle an alphabet to generate a key for monoalphabetic substitution cipher.
"""
import random

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def shuffled_alphabet():
    alpha_list = list(alphabet)
    random.shuffle(alpha_list) # sort the alphabet into a random order
    s = ''.join(alpha_list)  # funny way to turn list of chars into string
    return s

def monoalphabetic_substitution(text, key):
    alpha_list = list(alphabet)
    result = ""
    for letter in text:
        if letter in alphabet:
            result += key[alphabet.find(letter.lower())] # replace each letter by the same index in the shuffled alphabet
        else:
            result += letter
    return result

if __name__ == '__main__':
    # english wordlist from https://github.com/first20hours/google-10000-english/tree/master
    with open("google-10000-english-no-swears.txt", "r") as f:
        words = f.readlines()
    words = [x.strip() for x in words]

    plaintext = [random.choice(words) for _ in range(400)] # sample 400 random words
    plaintext = " ".join(plaintext) # join list of words together, with spaces in between

    with open("flag.txt", "r") as f:
        flag = f.read()
    plaintext = plaintext + " " + flag # Add flag to plaintext

    key = shuffled_alphabet();
    ciphertext = monoalphabetic_substitution(plaintext, key)
    with open("ciphertext.txt", "w") as f:
        f.write(ciphertext)
