#!/usr/bin/env python
"""
Basic xor cipher
"""
import random

alphabet = 'abcdefghijklmnopqrstuvwxyz -,.'

# english wordlist from https://github.com/first20hours/google-10000-english/tree/master
with open("google-10000-english-no-swears.txt", "r") as f:
    words = f.readlines()
    words = [x.strip() for x in words]

def generate_text(num_words):
    # My super realistic text generator!
    # Sample some words
    sampled = [random.choice(words) for _ in range(num_words)]
    joined = " ".join(sampled)

    # Add some dashes for the meme compound words
    for i in [123,321,234,432,543]:
        space_idx = joined.find(" ", i)
        joined = joined[:space_idx] + "-" + joined[space_idx+1:]
    dashed = ""

    # Add some punctiation
    for x in joined:
        if x == " ":
            # Compound words are super pog
            if random.random() < 0.23:
                dashed += "-"
            # Sometimes you need commas
            elif random.random() < 0.12 :
                dashed += ", "
            # And sentences are cool too. (Lets pretend capital letters don't exist)
            elif random.random() < 0.08:
                dashed += ". "
            else:
                dashed += " "
        else:
            dashed += x
    

    return dashed






def apply_key(text, key):
    result = ""
    for i in range(len(text)):
        letter = text[i]
        key_letter = key[i%(len(key))]
        result += alphabet[(alphabet.find(letter.lower()) + alphabet.find(key_letter.lower())) % len(alphabet)] # replace each letter by the same index in the shuffled alphabet
    return result

if __name__ == '__main__':
    print("welcome to my baby-xor challenge! I'll sample two keyphrases to make it a little more challenging!")

    # Sample a random keyphrase
    key_phrase_1 = random.choice(words)
    while len(key_phrase_1) < 3000:
        key_phrase_1 += " " + random.choice(words)

    key_phrase_2 = [random.choice(words) for _ in range(100)]

    # Apply secondary keyphrase
    for key2 in key_phrase_2:
        key = apply_key(key_phrase_1,key2)

    print("Key generated! Can you crack me?")
    successes = 0
    for _ in range(100):
        plaintext = generate_text(75)
        ct = apply_key(plaintext,key)
        print(f"ct: {ct}")
        guess = input("What is the plaintext?:")
        if len(guess) > 2:
            if guess == plaintext:
                print("Nice!")
                successes += 1
            else:
                print("WRONG WRONG WRONG")
                exit()
        if successes == 10:
            print("Wow you're an XOR MASTER!")
            with open("flag.txt", "r") as f:
                flag = f.read()
            print(flag)
            exit()
    print("Thanks for playing <3")
    exit()