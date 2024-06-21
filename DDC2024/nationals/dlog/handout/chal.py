from Crypto.Util.number import getStrongPrime, bytes_to_long

with open("flag.txt", "rb") as f:
    flag = f.read()
assert len(flag) == 1024//8

p = getStrongPrime(1024)

print(f'p = {p}')
print(f'2^flag mod p = {pow(2,bytes_to_long(flag), p)}')