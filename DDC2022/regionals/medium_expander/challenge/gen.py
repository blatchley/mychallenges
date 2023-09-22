from Crypto.Cipher import AES

K = 4
W = 22
P = [AES.new(bytes([i]*16), mode=AES.MODE_ECB) for i in range(K)]

def move(node, n):
    return P[n].encrypt(node)

with open('flag.txt', 'r') as f:
    flag = int(f.read().strip().encode('utf-8').hex(), 16)

with open('walk.txt', 'w') as f:
    node = b'\x00'*16

    while flag:
        f.write(node.hex() + '\n')
        for i in range(W):
            node = move(node, flag % K)
            flag //= K

    f.write(node.hex() + '\n')
