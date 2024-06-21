from random import getrandbits, randint
import hashlib
from sage.all import *

p = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed
K = GF(p)
A = K(0x76d06)
B = K(0x01)
E = EllipticCurve(K, ((3 - A**2)/(3 * B**2), (2 * A**3 - 9 * A)/(27 * B**3)))
r = 0x80000000000000000000000000000000a6f7cef517bce6b2c09318d2e7ae9f68
G = E(21977797803966062166131953070962764749821235838999402741987750576031241997417, 51891000958208793389495271575934815534411235780576220943952563952382004288047)
E.set_order(r)

print("Hi Alice, this is Bob! I want to see if you can run Diffie-Hellman without my public key.")
print("This curve seemed to work fine in the last challenge, so you shouldn't be able to break these dlogs right?")

while True:
	b = getrandbits(128)
	print(f"here's a random dlog {b*G}")
	if input("done?").lower() == "y":
		break

print("I am not really sure, but I hope it is secure!")

def test_noninteractive_dlog(E, K, G, b = randint(1,r-1)):
	B = b*G
	print("I just generated my ephemeral key pair.")
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
	if not k0 == k1:
		print("nope, guessed wrong. Guess non interactive key exchange isn't really a thing after all")
		exit()
	print("oh nice, same!")
	return

for i in range(32):
	test_noninteractive_dlog(E, K, G)

print("NIDH IS HERE!!!! Here's a flag!")

with open("flag.txt", "r") as f:
	print(f.read())
