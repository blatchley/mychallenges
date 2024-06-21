from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import random

bit_len = 1024

p = getPrime(bit_len)
q = getPrime(bit_len)

n = p*q
e = 65537

d = pow(e,-1,(p-1)*(q-1))
assert pow(pow(12345,e,n), d,n) == 12345

with open("flag.txt", "rb") as f:
    flag = f.read().strip()

ct = pow(bytes_to_long(flag), e, n)


# lets make some noisy primes!
p_bin = bin(p)[2:]
q_bin = bin(q)[2:]
p_noisy = ""
q_noisy = ""
for i in range(bit_len):
    x = random.randint(1, 10*bit_len) - 10*i
    if x < bit_len:
        p_noisy += p_bin[i]
    else:
        p_noisy += "?"
    x = random.randint(1, 10*bit_len) - 10*i
    if x < bit_len:
        q_noisy += q_bin[i]
    else:
        q_noisy += "?"



print(f'n = {n}')
print(f'e = {e}')
print(f'ct = {ct}')
print(f'p_noisy = "{p_noisy}"')
print(f'q_noisy = "{q_noisy}"')
print()
print()
print(f'p_real = {bin(p)}')
print(f'q_real = {bin(q)}')