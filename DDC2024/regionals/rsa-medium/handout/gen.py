from Crypto.Util.number import getPrime, bytes_to_long

with open("flag.txt", "rb") as f:
    flag = bytes_to_long(f.read())

p,q,r = [getPrime(512) for _ in range(3)]
e = 0x1337

m1 = bytes_to_long(b"Is this really an RSA challenge?")
m2 = bytes_to_long(b"I think so? It is raising stuff mod N after all...")
m3 = bytes_to_long(b"I guess that's close enough.")

with open("output.txt", "w") as f:
    f.write(f'm1 = {pow(m1,e,p*q)}\n')
    f.write(f'm2 = {pow(m2,e,q*r)}\n')
    f.write(f'm3 = {pow(m3,e,r*p)}\n')
    f.write(f'flag = {pow(flag,e,p*q*r)}')