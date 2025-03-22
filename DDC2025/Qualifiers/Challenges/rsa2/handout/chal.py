import random


with open("flag.txt", "r") as f:
    flag = f.read()

assert len(flag) == 53


FLAG = f"So in normal RSA challenges it all comes down to factorising. To get the flag, {flag}, you would take n = p*q, and if you factor into p and q you can compute phi(n) as (p-1)*(q-1), and then compute d as pow(e,-1,phi(n)) and then get {flag} by doing pow(ct,d,n). But wait is this even RSA? I'm kinda confused tbh... The flag says {flag} but still... Lets encrypt the flag, {flag}, and see what happens. Think you can recover {flag}?  Why not, it's really easy, it's just {flag} {flag} {flag} {flag}"


f = open("output.txt", "w")

for i in range(64):
    e = random.randint(2,2**512)
    n = random.randint(2,2**256)*random.randint(2,2**256)
    ct = pow(int.from_bytes(FLAG.encode(),"big"), e, n)

    f.write(f'e{i} = {e}\n')
    f.write(f'n{i} = {n}\n')
    f.write(f'c{i} = {ct}\n')
    f.write("\n")