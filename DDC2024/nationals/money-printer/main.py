import secrets
import hashlib
from sage.all import *

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
r = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
K = GF(p)
a = K(0x0000000000000000000000000000000000000000000000000000000000000000)
b = K(0x0000000000000000000000000000000000000000000000000000000000000007)
E = EllipticCurve(K, (a, b))
G = E(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
E.set_order(r)

x = secrets.randbelow(r)

# Generate private key for Bitcoin transactions
P = x * G

print("I have received several Bitcoin transactions under this key pair I generated yesterday.")
print("You can prove you also know this private key by signing a message with the corresponding private key.")
print("If you manage to do this, not only you will have all my Bitcoin, but I will give you the flag as well.\n")

print("I built my own custom signature based on Schnorr from a textbook, so it must be secure.\n")

print("Here is the public key P:")
print(P)

print("\nThe signature should be such that [s]G = R + h*P, where s in an integer, R = (x, y) is a point in the curve and h is Hash(M, P). ")
print("Now you can give me the message M and a valid signature ((x,y), s) to prove you know the secret too: ")

try:
	M = input()
	x = K(input())
	y = K(input())
	s = int(input())
	R = E(x, y)
except:
	print("You do not know what you're doing, this point is not in the curve.")
	exit(0)

h = int(hashlib.sha256((M + str(G)).encode()).hexdigest(), 16)

# Now let us verify what you gave us
vCheck = R + h*P

if (s*G == vCheck and s != 0):
    flag = open('flag.txt', 'r')
    print("\n" + flag.read())
else:
	print("You do not know what you're doing. Come back after you do your homework!")
