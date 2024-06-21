from Crypto.Hash import MD5

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

for x in FLAG:
    assert x in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_"

hashes = []
for c in FLAG:
    md5 = MD5.new()
    md5.update(c.encode())
    h = md5.hexdigest()
    hashes.append(h)

with open("output.txt", "w") as f:
    for i in range(len(hashes)):
        f.write(f'char{i} = {hashes[i]}\n')

