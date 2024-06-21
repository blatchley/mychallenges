import random
from Crypto.Util.number import getPrime

with open("flag.txt", "rb") as f:
    FLAG = f.read().strip()  

assert len(FLAG) == 64
f0, f1, f2, f3 = FLAG[:16], FLAG[16:32], FLAG[32:48], FLAG[48:]


# "XOR"  512 bit number with a byte string!
# a is a bytestring
# b is a number
# Pads a to 64 bytes, then converts b to bytes, then xor's them together.
def xor(a,b):
    a = a.zfill(64)
    b = b.to_bytes(64, "little")
    result = bytes([x^y for x,y in zip(a,b)])
    return result

# example xor. Note xoring twice with the same number undoes the xor.
# Your goal is to recover the numbers, and use these to "un-xor" the parts of the flag
assert xor(xor(b'ACBDEFGHIJKLNNOP', 1234567898765432123456789),1234567898765432123456789)


# An LCG is a form of random number generator, where we repeatedly add and multiply a value with two constants, modulo a prime.
# This is incredibly cheap to do, so is often used when you need a lot of "psuedo random" data quickly.
# state2 = state1 * m + c modulo p

# Problem 0
p0 = getPrime(512)
m0 = random.randint(0,p0)
c0 = random.randint(0,p0)
state = random.randint(0,p0)

with open("output0.txt", "w") as f:
    f.write("Problem 0 Values\n")
    f.write(f'm0 = {m0}\n')
    f.write(f'c0 = {c0}\n')
    f.write(f'p0 = {p0}\n')
    f.write(f's0 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m0 + c0) % p0
    # compute this state and xor to recover the first part of the flag!
    f.write(f'f0 = {xor(f0,state)}\n')


# Note that it is very simple to compute the next state given the previous one. The next three challenges are about what happens if you try and make the value "unpredictable" by hiding m, c or p from the user.
# If this is new to you, there is a very good resource to follow here! 
# https://tailcall.net/posts/cracking-rngs-lcgs/

# Problem 1
p1 = getPrime(512)
m1 = random.randint(0,p1)
c1 = random.randint(0,p1)
state = random.randint(0,p1)

with open("output1.txt", "w") as f:
    f.write("Problem 1 Values, unknown c\n")
    f.write(f'm1 = {m1}\n')
    f.write(f'c1 = ????? \n')
    f.write(f'p1 = {p1}\n')
    f.write(f's10 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m1 + c1) % p1
    f.write(f's11 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m1 + c1) % p1
    # compute this state and xor to recover the next part of the flag!
    f.write(f'f1 = {xor(f1,state)}\n')
    

# Problem 2
p2 = getPrime(512)
m2 = random.randint(0,p2)
c2 = random.randint(0,p2)
state = random.randint(0,p2)

with open("output2.txt", "w") as f:
    f.write("Problem 2 Values, unknown c,m\n")
    f.write(f'm2 = ?????\n')
    f.write(f'c2 = ????? \n')
    f.write(f'p2 = {p2}\n')
    f.write(f's20 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m2 + c2) % p2
    f.write(f's21 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m2 + c2) % p2
    f.write(f's22 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m2 + c2) % p2
    # compute this state and xor to recover the next part of the flag!
    f.write(f'f2 = {xor(f2,state)}\n')
    


# Problem 3
p3 = getPrime(512)
m3 = random.randint(0,p3)
c3 = random.randint(0,p3)
state = random.randint(0,p3)

with open("output3.txt", "w") as f:
    f.write("Problem 3 Values, unknown c,m,p\n")
    f.write(f'm3 = ?????\n')
    f.write(f'c3 = ?????\n')
    f.write(f'p3 = ?????\n')
    f.write(f's30 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m3 + c3) % p3
    f.write(f's31 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m3 + c3) % p3
    f.write(f's32 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m3 + c3) % p3
    f.write(f's33 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m3 + c3) % p3
    f.write(f's34 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m3 + c3) % p3
    f.write(f's35 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m3 + c3) % p3
    f.write(f's36 = {state}\n')
    # we "tick" the LCG to the next state
    state = (state * m3 + c3) % p3
    # compute this state and xor to recover the next part of the flag!
    f.write(f'f3 = {xor(f3,state)}\n')
    

