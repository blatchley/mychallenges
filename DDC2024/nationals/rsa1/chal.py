from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

bit_len = 768

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
for i in range(6):
    if i % 2:
        p_noisy += p_bin[128*i:128*i+128]
        q_noisy += "?" * 128
    else:
        q_noisy += q_bin[128*i:128*i+128]
        p_noisy += "?" * 128


print(f'n = {n}')
print(f'e = {e}')
print(f'ct = {ct}')
print(f'p_noisy = "{p_noisy}"')
print(f'q_noisy = "{q_noisy}"')