from Crypto.Util.number import long_to_bytes, getPrime, isPrime, getRandomRange # pip3 install pycryptodome
import os

def xor(a,b):
    return bytes([x^^y for x,y in zip(a,b)])

with open("flag.txt", "rb") as f:
    flag = f.read()
# pad flag
flag = flag + os.urandom((32 - len(flag)))

def challenge():
    # gen curve
    p = getPrime(256)
    A = getRandomRange(1, p)
    B = getRandomRange(1, p)
    assert (4*A**3+27*B**2) % p != 0
    E = EllipticCurve(GF(p), [A, B])
    assert isPrime(E.order())

    print(f'p = {p}')
    print(f'A = {A}')
    print(f'B = {B}')
 
    g = E.random_element()
    secret = E.random_element()
    for i in range(9):
        g = g + secret
        print(f'g{i} = ({g[0]},{g[1]})')

    mask = int(secret[0])
    print(f"flag = {xor(long_to_bytes(mask), flag).hex()}")


challenge()
