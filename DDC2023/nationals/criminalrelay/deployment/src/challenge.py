
from Crypto.Cipher import AES
import zlib
import os

with open("flag.txt","r") as f:
    flag = f.read()

charset = 'abcdefghijklmnopqrstuvwxyz_'

assert len(flag) == 23
assert flag.startswith('DDC{')
assert flag.endswith('}')
for ch in flag[4:-1]:
    assert ch in charset

key = os.urandom(16)

def encrypt_and_send(msg):
    msg_struct = f'MSG: {msg} TO: ____{flag}____ '
    encoded_message = zlib.compress(msg_struct.encode())
    cipher = AES.new(key, AES.MODE_CTR)
    ct = cipher.nonce + cipher.encrypt(encoded_message)
    # send through super tor mixnet jump server darkweb thingy TOR process xd
    print(f'We intercepted the following message leaving the relay node: {ct.hex()}')

print("Welcome to the anonymous message forwarding service!")
print("Just send your message here, and this server will securely forward it into the dark web mixnet, for delivery to the redacted target!")

while True:
    msg = input("Whats your msg?: ")
    encrypt_and_send(msg)

