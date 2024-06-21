from Crypto.Hash import MD5

def bytes_to_int(a):
    return int(a.hex(),16)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

assert len(FLAG) == 69
assert FLAG.startswith("DDC{")
assert FLAG.endswith("}")

for x in FLAG[4:-1]:
    assert x in "LlLlLlL"

hashes = []
for i in range(len(FLAG)):
    c = str(i) + FLAG[i] 
    md5 = MD5.new()
    md5.update(c.encode())
    h = md5.digest()
    hashes.append(h)


hash = bytes_to_int(hashes[0])
for x in hashes[1:]:
    hash += bytes_to_int(x)
    hash %= 2**128

with open("output.txt", "w") as f:
    f.write(hex(hash)[2:])

