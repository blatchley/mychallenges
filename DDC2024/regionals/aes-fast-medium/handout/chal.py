from aesfast import AES
import os

with open("flag.txt", "rb") as f:
    flag = f.read()

assert len(flag) == 32

key = os.urandom(16)
aes = AES(key)

flag_enc = aes.encrypt_block(flag[:16]) + aes.encrypt_block(flag[16:32])

print("welcome to my improved, mix-collumnless, AES system!")
print(f'flag = {flag_enc.hex()}')

print("what would you like me to encrypt?")
while True:
    pt = input("pt (hex):")
    assert len(pt) == 32
    pt = bytes.fromhex(pt)
    encrypted = aes.encrypt_block(pt)
    print(f'ct = {encrypted.hex()}')
