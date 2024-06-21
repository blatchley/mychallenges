import random
import Crypto.Util.number

from datetime import datetime
from Crypto.Util.number import getPrime, GCD, inverse

def keygen(bits, randfunc):

    # key generation
    while True:
        # sample two different primes
        p = getPrime(bits // 2, randfunc)
        q = getPrime(bits // 2, randfunc)
        if p == q:
            continue
        N = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        # e needs to be invertible modulo phi(N)
        if GCD(e, phi) > 1:
            continue
        d = inverse(e,phi)
        break
    return (d, e, N)

def encrypt(message, e, N):
    m = message % N
    return pow(m, e, N)

def decrypt(ciphertext, d, N):
    c = ciphertext % N
    return pow(c, d, N)

s = int(datetime.now().timestamp())
print(s)
random.seed(s)

(d, e, N) = keygen(1024, random.randbytes)
with open('flag.txt', 'r') as file:
    message = file.read().replace('\n', '')

message = int.from_bytes(str.encode(message, "utf-8"), "little")

ciphertext = encrypt(message, e, N)
decryption = decrypt(ciphertext, d, N)

assert decryption == message

with open('challenge.txt', 'w') as file:
    file.write(str(ciphertext))
