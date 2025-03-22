
from Crypto.Cipher import AES
from hashlib import md5
import random 
import time
import ast

with open("output.txt", "r") as f:
    ct = ast.literal_eval(f.readline().strip().split("=")[1])
    flag_enc = bytes.fromhex(f.readline().strip().split("=")[1])
    iv = bytes.fromhex(f.readline().strip().split("=")[1])


def gen_mat(q, seed, m,N):
    random.seed(seed)
    return [[random.randint(0,q-1) for _ in range(N)] for _ in range(m)]


# https://en.wikipedia.org/wiki/Learning_with_errors
N = 110
m = 192
q = next_prime(1337)
F = GF(q)
A = Matrix(F,gen_mat(q, "DDC2025", m, N))

ct = vector(F,ct)


enc2 = vector([x - 2 for x in ct])

# matrix: Will subtract/add the rows of A from c to find the shortest solution (modulo q). The remainder after this is then the error term.
# A A A A 0
# A A A A 0
# A A A A 0
# A A A A 0
# c c c c 1
# q 0 0 0 0
# 0 q 0 0 0
# 0 0 q 0 0
# 0 0 0 q 0
mat = Matrix(ZZ, N + 1 + m, m + 1)
mat[:N, :m] = A.T 
mat[N, :m] = enc2
mat[N, m] = 1
mat[N + 1 : N + 1 + m, :m] = diagonal_matrix([q] * m)

for l in mat:
    print(l)
print("BKZ")
start_time = time.time()
L = mat.BKZ(block_size=20)
print(f" took --- {(time.time() - start_time)} seconds ---")


rows = list(L)
for row in rows:
    # skip past the all 0 rows
    if -1 in row and 1 in row:
        sol = row
        break
print(sol)

err = sol / sol[-1]
err = [x + 2 for x in err[:-1]]
ct2 = ct - vector(F,err)

s_test = A.solve_right(ct2)

print(f'recovered error {err}')
key_string = "".join([str(x) for x in s_test])
# for x in "123":
key_string2 = key_string 
print(f'key_string = {key_string2}')
key = md5(key_string2.encode()).digest()
aes = AES.new(key, mode=AES.MODE_CBC, iv=iv)
flag = aes.decrypt(flag_enc)
print(flag)