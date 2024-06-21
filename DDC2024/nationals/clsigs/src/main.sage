import secrets
import hashlib
from sage.all import *

def keygen():
	x = secrets.randbelow(r)
	y = secrets.randbelow(r)
	sk = (x, y)
	pk = x*Q, y*Q
	return (sk, pk)

def sign(m, sk):
	(x, y) = sk
	A = c * E.random_element()
	return (A, y*A, (x + m*x*y)*A)

def verify(s, m, pk):
	(A, B, C) = s
	(X, Y) = pk
	r0 = Ep12(A).tate_pairing(Y, r, 12) == Ep12(B).tate_pairing(Q, r, 12)
	r1 = Ep12(A).tate_pairing(X, r, 12) * Ep12(m*B).tate_pairing(X, r, 12) == Ep12(C).tate_pairing(Q, r, 12)
	return r0 and r1

load("params.sage")
params()

print("The CL signature scheme, due to Camenisch and Lysyanskaya, can be used to construct anonymous credential systems.")

print("Let me compute a signature over the message 1337 so you can see how it looks like.")

(sk, pk) = keygen()
sig = sign(1337, sk)

print("\nPublic Key = ", pk)
print("\nSignature = ", sig)

m = secrets.randbelow(100000000)
print("\nI implemented the scheme just like the 2004 paper. Can you compute a valid CL signature over the following integer message?", m)

print("Give me the projective coordinates (x,y,z) of the three points (A, B, C) and I will give you the flag if the signature is valid:")

xA = Fp(input())
yA = Fp(input())
zA = Fp(input())
xB = Fp(input())
yB = Fp(input())
zB = Fp(input())
xC = Fp(input())
yC = Fp(input())
zC = Fp(input())

try:
	A = E(xA, yA, zA)
	B = E(xB, yB, zB)
	C = E(xC, yC, zC)
except:
	print("One of the points is not in the curve, try again!")
	exit()

if (m != 1337 and verify((A, B, C), m, pk)):
    flag = open('flag.txt', 'r')
    print("\n" + flag.read())
else:
	print("Incorrect, try again!")
