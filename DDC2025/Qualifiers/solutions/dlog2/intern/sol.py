from Crypto.Util.number import isPrime, getPrime
from pwn import *
import time

ip = "127.0.0.1"
port = 1337
path_to_cadopy = "/mnt/c/Users/adamb/Downloads/cado/cado-nfs/cado-nfs.py"

bitsize = 296
# power = getPrime(250)
while True:
    a = getPrime(bitsize)
    b = 2*a + 1
    g = 4

    if isPrime(b):
        break

payload = f'{path_to_cadopy} -dlp -ell {a} target={4} {b}'
with process([payload], shell=True) as cadof:
    while True:
        z = cadof.readline().decode("utf-8")
        print("PRECOMPUTATION:" + z, end="")
        if 'Complete Factorization / Discrete logarithm: Total cpu/elapsed time for entire Discrete logarithm:' in z:
            break
    cadof.recvuntil(b'root: If you want to compute one or several new target(s), run')
    preprocessedstring = cadof.recvuntil(b'target=').decode()
    cadof.recvuntil(b'logbase =')
    logbase = int(cadof.readline().strip())
    cadof.recvuntil(b'target =')
    target = int(cadof.readline().strip())
    cadof.recvuntil(b'log(target) = ')
    logtarget = int(cadof.recvuntil(b' ').strip())



def cado_use_preprocess(val, preprocessed, run_idx):
    payload = preprocessed + str(val)
    with process([payload], shell=True) as cadof:
        while True:
            z = cadof.readline().decode("utf-8")
            print(f"online phase {i}:" + z, end="")
            if 'root: target =' in z:
                break
        cadof.recvuntil(b'root: log(target) = ')
        relative_log = int(cadof.recvuntil(b' ').strip())
    return relative_log


print(preprocessedstring)

print(logbase)
print(target)
print(logtarget)

inverse_base = pow(logtarget, -1, a)
print("starting online phase")
start = time.time()
# with process(["python3 chal.py"], shell=True, level="debug") as rem:
with remote(ip,port,level="debug") as rem:
    rem.recvuntil(b'give me a safe prime!: ')
    rem.sendline(str(b))
    rem.recvuntil(b'')
    for i in range(5):
        rem.recvuntil(f"{g}^x mod {b} = ".encode())
        chal = int(rem.readline().strip())
        print(chal)
        res = cado_use_preprocess(chal, preprocessedstring, i)
        exponent = (res * inverse_base) % a
        rem.sendline(str(exponent))
        print(f"time elapsed = {time.time() - start}")
    print(f"time elapsed = {time.time() - start}")
    print(f"time elapsed = {time.time() - start}")
    rem.interactive()
    exit()

exit()