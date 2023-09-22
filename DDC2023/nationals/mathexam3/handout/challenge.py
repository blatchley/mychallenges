
from Crypto.Util.number import getPrime

with open("flag.txt", "r") as f:
    flag = f.read()

for i in range(1,100):
    P = getPrime(8 * i)
    print(f'P = {P}')
    print(f'find "x" such that x**x == 2 modulo {P}')
    x_inp = int(input("x: "))
    if not (x_inp**x_inp) % P == 2:
        print("oh no, that's incorrect.")
        print(f'x = {x_inp} did not give the correct result :(')
        exit()
    else:
        print("Nice!")

print("well done! you've passed the final maths exam!")
print(flag)