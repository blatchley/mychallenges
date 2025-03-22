from pwn import *
from Crypto.Util.number import getPrime, isPrime

ip = "127.0.0.1"
port = 1337

# Generate smooth-order primes for fast encryption even with large e
def gen_smooth_prime(PrimeSize, FactorSize, base = 1):
    factorlist = [getPrime(FactorSize) for _ in range((PrimeSize // FactorSize) + 1)]
    while True:
        P = base
        # print(factorlist)
        for pl in factorlist:
            P *= pl
        P = 2*P + 1
        if isPrime(P):
            return P
        else:
            factorlist = factorlist[1:] + [getPrime(FactorSize)]

P = gen_smooth_prime(500,15)
F = GF(P)


# with process(["python3 chal.py"], shell=True, level="Debug") as rem:
with remote(ip, port, level="Debug") as rem:
    rem.recvuntil(b'give me a prime!: ')
    rem.sendline(str(P))

    for i in range(5):
        rem.recvuntil(b'= ')
        c = int(rem.readline().strip())
        print("discrete log starting")
        l = F(c).log(F(4))
        print(l)
        rem.sendline(str(l))
    
    rem.interactive()
    