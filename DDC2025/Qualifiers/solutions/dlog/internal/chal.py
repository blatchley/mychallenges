from Crypto.Util.number import isPrime
import random

p = int(input("give me a prime!: "))
assert isPrime(p)

for i in range(5):
    g = 4
    v = random.randint(2,2**312)
    print(f'{g}^x mod {p} = {pow(g,v,p)}')
    x = input("what was x?: ")
    if int(x) == v:
        print("correct!")
    else:
        print(f"wrong! v = {v}")
        exit()

print(f'well done!')

with open("flag.txt", "r") as f:
    flag = f.read()
    print(flag)
