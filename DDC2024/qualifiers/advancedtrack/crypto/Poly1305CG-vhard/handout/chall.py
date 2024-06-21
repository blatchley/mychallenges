from Crypto.Hash import Poly1305
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
import os

with open("flag.txt", "rb") as f:
    flag = f.read()
assert len(flag) == 48

# "Poly1305 is a universal hash family designed by Daniel J. Bernstein for use in cryptography." - wikipedia
def poly1305_hash(data, Key, Nonce):
    hsh = Poly1305.new(key=Key, cipher=AES, nonce=Nonce)
    hsh.update(data=data)
    return hsh.digest()

# If i just use a hash function instead of a linear function in my LCG, then it should be super secure right?
class PolyCG:
    def __init__(self):
        self.Key = b'DDC_2024!-Lets_get_weird_with_it'
        self.Nonce = b'NonceNonceyNonce'
        self.State = os.urandom(16)

    def next(self):
        self.State = poly1305_hash(self.State, self.Key, self.Nonce)
        return self.State[-4:]


pcg = PolyCG()
for i in range(10):
    print(f'v_{i} = {pcg.next().hex()}')

otp = b"".join

flagenc = strxor(flag, b"".join([pcg.next() for _ in range(48//4)]))
print(f"flag = {flagenc.hex()}")