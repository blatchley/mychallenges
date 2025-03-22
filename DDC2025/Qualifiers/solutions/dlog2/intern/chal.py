from Crypto.Util.number import isPrime
import random
import signal


p = int(input("give me a safe prime!: "))
assert isPrime(p)
assert isPrime((p-1)//2)

for i in range(5):
    # chop chop buddy, no time to waste here
    signal.alarm(40)
    g = 4
    v = random.randint(2,2**295)
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
