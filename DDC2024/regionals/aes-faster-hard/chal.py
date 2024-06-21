from aesfaster import AES
import os

with open("flag.txt", "rb") as f:
    flag = f.read()

key = os.urandom(16)
aes = AES(key)


print("welcome to my re-improved, SBOX-less, AES system!")
print("what would you like me to encrypt?")

pt = input("pt (hex):")
pt = bytes.fromhex(pt)
encrypted = aes.encrypt_block(pt)
print(f'ct = {encrypted.hex()}')

ct_challenge = os.urandom(16)
print(f'decrypt this: {ct_challenge.hex()}')
pt = input("pt (hex): ").strip()
assert aes.decrypt_block(ct_challenge) == bytes.fromhex(pt), "wrong decryption :("
print("wow you decrypted properly, but can you encrypt?")


pt_challenge = os.urandom(16)
print(f'encrypt this: {pt_challenge.hex()}')
ct = input("ct (hex): ")
assert aes.encrypt_block(pt_challenge) == bytes.fromhex(ct), "wrong encryption :("

print("wow you've really cracked my system 0.0")
print(f'flag = {flag}')