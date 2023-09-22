import random

with open("plaintext.txt", "r") as f:
    plaintext = f.read()

random.seed("Crypto Gang")

l = [c for c in plaintext]

random.shuffle(l)
random.shuffle(l)
random.shuffle(l)

ciphertext = "".join(l)

with open("encrypted.enc", "w") as f:
    f.write(ciphertext)
