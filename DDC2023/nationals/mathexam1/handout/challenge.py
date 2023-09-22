
from random import randint, randrange

with open("flag.txt", "r") as f:
    flag = f.read()

for i in range(1,12):
    A = randrange(0, 10**i)
    B = randrange(0, 10**i)
    x = randrange(0, 10**i)
    C = A*(x**2) + B*x
    print(f'A = {A}')
    print(f'B = {B}')
    print(f'C = {C}')
    print(f'find "x" such that {A}*x**2 + {B}*x == {C}')
    x_inp = int(input("x: "))
    if not A*(x_inp**2) + B*x_inp == C:
        print("oh no, that's incorrect.")
        print(f'x = {x_inp} did not give the correct result :(')
        exit()
    else:
        print("Nice!")

print("well done! you've passed the first maths exam!")
print(flag)


