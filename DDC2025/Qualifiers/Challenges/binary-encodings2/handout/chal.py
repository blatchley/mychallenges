from Crypto.Util.number import getPrime
import os

def binarify(m):
    return int.from_bytes(bin(int.from_bytes(m, "big")).encode(), "big")

with open("flag.txt", "rb") as f:
    flag = f.read()

assert flag.startswith(b'DDC{') and flag.endswith(b'}')
assert len(flag) == 18

with open("output.txt", "w") as f:
    for i in range(2):
        p = getPrime(64)
        f.write(f'p_{i} = {p}\n')
        f.write(f'f_{i} = {binarify(flag) % p}\n')


