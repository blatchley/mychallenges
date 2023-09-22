
from Crypto.Util.number import getPrime
from random import randrange

with open("flag.txt", "r") as f:
    flag = f.read()

for i in range(1,25):
    P = getPrime(10 * i)
    A = randrange(0, P)
    B = randrange(0, P)
    x = randrange(0, P)
    C = (A*(x**2) + B*x) % P
    print(f'P = {P}')
    print(f'A = {A}')
    print(f'B = {B}')
    print(f'C = {C}')
    print(f'find "x" such that {A}*x**2 + {B}*x == {C} modulo {P}')
    x_inp = int(input("x: "))
    if not (A*(x_inp**2) + B*x_inp) % P == C:
        print("oh no, that's incorrect.")
        print(f'x = {x_inp} did not give the correct result :(')
        exit()
    else:
        print("Nice!")

print("well done! you've passed the second maths exam!")
print(flag)