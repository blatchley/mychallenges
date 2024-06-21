from cmath import e
from re import L
from aesfastest import AES
import os
import ast

with open("flag.txt", "rb") as f:
    flag = f.read()

assert len(flag) == 48

key = os.urandom(16)
aes = AES(key)

flag_enc = aes.encrypt_block(flag[:16]) + aes.encrypt_block(flag[16:32]) + aes.encrypt_block(flag[32:48])

print("welcome to my re-re-improved AES system! Given up changing anything major. I'll just tweak xor slightly and use all my energy making input handling super fancy :)")
print("what would you like me to decrypt?")
while True:
    try:
        # new advanced input handling ¯\_(ツ)_/¯
        pt = ast.literal_eval(input("ct:"))

        # valid plaintexts only pls ¯\_(ツ)_/¯
        assert len(pt) == 16
        for x in pt:
            assert x in range(256)
        
        decrypted = aes.decrypt_block(pt)
        print(f'decrypted = {decrypted.hex()}')
    except Exception as  e:
        if pt == "finished":
            break
        else:
            print('did you mean "finished"? If not, you probably messed up your input ¯\_(ツ)_/¯')

print("hope you had fun decrypting stuff ¯\_(ツ)_/¯")
print("here's the flag!")
print(f'flag = {flag_enc.hex()}')