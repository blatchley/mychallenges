
from Crypto.Cipher import AES
from hashlib import md5
import random 

# Generate the public A matrix
def gen_mat(q, seed, m,N):
    random.seed(seed)
    return [[random.randint(0,q-1) for _ in range(N)] for _ in range(m)]


# Params
N = 110
m = 192 
q = next_prime(1337)
F = GF(q)

# Can you learn the errors?
s = vector(F, [random.SystemRandom().randint(0,q-1) for _ in range(N)])
err = vector(F, [random.SystemRandom().randint(1,3) for _ in range(m)])
A = Matrix(F,gen_mat(q, "DDC2025", m, N))
ct = A * s + err


# encrypt flag using secret
with open("flag.txt", "rb") as f:
    flag = f.read()

key_string = "".join([str(x) for x in s])
key = md5(key_string.encode()).digest()
aes = AES.new(key, mode=AES.MODE_CBC)
flag_enc = aes.encrypt(flag)


with open("output.txt", "w") as f:
    f.write(f'ct = {ct}\n')
    f.write(f'flag_enc = {flag_enc.hex()}\n')
    f.write(f'iv = {aes.iv.hex()}')

# Adding for sanity checks, incase random.seed() is inconsistent for some dumb reason
with open("matrix.txt", "w") as f:
    f.write(f'A = {A}')