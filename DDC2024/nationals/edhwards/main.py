import random
import hashlib
from sage.all import *

p = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed
K = GF(p)
A = K(0x76d06)
B = K(0x01)
E = EllipticCurve(K, ((3 - A**2)/(3 * B**2), (2 * A**3 - 9 * A)/(27 * B**3)))
r = 0x80000000000000000000000000000000a6f7cef517bce6b2c09318d2e7ae9f68
def to_weierstrass(A, B, x, y):
	return (x/B + A/(3*B), y/B)
G = E(*to_weierstrass(A, B, K(0x09), K(0x20ae19a1b8a086b4e01edd2c7748d14c923d4d7e6d7c61b229e9c5a27eced3d9)))
E.set_order(r)

b = random.randint(1,r-1)
B = b*G
print("Hi Alice, this is Bob! Let's run Diffie-Hellman. My ephemeral public key is:")
print(B)

print("Please give me your ephemeral public key as two coordinates (x, y) in the same curve:")
try:
	x = K(input())
	y = K(input())
	A = E(x,y)
except:
	print("The point must be in the curve!")
	exit(0)

K = b*A
k0 = hashlib.sha256(str(K).encode()).hexdigest()

print("Now give me the key you computed to check if we obtained the same.")
k1 = input()

if (k0 == k1):
    flag = open('flag.txt', 'r')
    print("\n" + flag.read())
else:
	print("Incorrect, try again!")
