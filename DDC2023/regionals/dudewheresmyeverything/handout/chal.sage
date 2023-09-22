from Crypto.Util.number import long_to_bytes, getStrongPrime, isPrime, getRandomRange # pip3 install pycryptodome
import os

def xor(a,b):
    return bytes([x^^y for x,y in zip(a,b)])

with open("flag.txt", "rb") as f:
    flag = f.read()
# pad flag
flag = flag + os.urandom((64 - len(flag)))

def challenge():
    # gen curve
    p = getStrongPrime(768)
    A = getRandomRange(1, p)
    B = getRandomRange(1, p)
    assert (4*A**3+27*B**2) % p != 0
    E = EllipticCurve(GF(p), [A, B])
    

    print(f'p = ¯\(ツ)/¯')
    print(f'A = ¯\(ツ)/¯')
    print(f'B = ¯\(ツ)/¯')
    g = E.random_element()
    secret = E.random_element()


    for i in range(9):
        g = g + secret
        if i < 5:
            print(f'g{i} = ({g[0]}, ¯\(ツ)/¯)')
        else:
            print(f'g{i} = ¯\(ツ)/¯')

    mask = int(secret[0])
    print(f"flag = {xor(long_to_bytes(mask), flag).hex()}")

    n = p
    for i in range(6):
        q = getStrongPrime(768)
        n *= q
    # ¯\(ツ)/¯ because we're nice ¯\(ツ)/¯
    print(f'n = {hex(n)}')



challenge()