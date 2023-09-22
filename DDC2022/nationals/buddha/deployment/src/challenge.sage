from random import randint

r = 0x8000000000000000000000000000000000000000000000000000020000000001
cof = 0x9adddc851c8c5c2f97cc969033d8023f5ed433fd8fbad435a4413547e18f678c
p = 2*cof*r - 1
Fp = GF(p)
assert(p in Primes())
A = -3
B = 0

x = 0x5b618e61cc59c8900a739c4631453583aba8e68e6d9f522630b6870a4b9aba4ec849c4b05c6b6b6544968cf32617da092f8e7a1d916b4ae55d57401de7086646
y = 0x657fd6725a6022fcb1b7a4af93d4bdea677112235d3c89f5fba7e6aabcb8fd0431d52afd560d2fdb771a77404357953c1b86016581676a3428d47a74d1e27fa0

# Curve y^2 = x^3 + A*x + B over GF(P)
E = EllipticCurve(Fp, [A,B])
h = E.order()//r
G = E(x,y)
assert(r*G == E(0))

def encode_msg(M):
    x = Fp(M)
    rhs = x^3 + A*x
    while not(rhs.is_square()):
        x += 1
        rhs = x^3 + A*x
    y = sqrt(rhs)
    return h*E(x, y)

# Encrypt using ElGamal
def encrypt(msg, PK):
    M = encode_msg(msg)
    y = randint(1, r-1)
    c1 = y * G
    c2 = M + y * PK
    return (c1, c2)

def main():
    # Generate secret signing key
    sk = randint(1, r-1)
    # public encryption key
    PK = sk*G

    print("       _=_        This is a direct oracle to BuDDHa.")
    print("     q(-_-)p-     BuDDHa is happy to share some wisdom, but first you need to solve a challenge.")
    print("     '_) (_`      A secret will be revealed if you guess correctly 50 times in a row!")
    print("     /__/  \      For each try, you will receive two messages and one ciphertext encrypted under Elgamal.")
    print("   _(<_   / )_    You have to guess which message is encrypted under a given public key by typing 0 or 1.")
    print(f"  (__\_\_|_/__)   The public key is {PK}\n")

    correct = 0
    while correct < 50:
        m0 = randint(1, p-1)
        m1 = randint(1, p-1)
        ms = [m0, m1]
        print(f'The first message is {m0}')
        print(f'The second message is {m1}')
        b = randint(0, 1)
        (c1, c2) = encrypt(ms[b], PK)
        print(f'\nYou got a new ciphertext! It is:\n c1 = {c1}\n c2 = {c2}\n')
        print("What is your guess (0 or 1)?")
        bit = int(input())
        if (bit == b):
            correct += 1
        else:
            exit()

    flag = open('flag.txt', 'r').read().strip()
    print(flag)

if __name__ == "__main__":
    main()
