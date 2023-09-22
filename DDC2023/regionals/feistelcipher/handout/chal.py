from hashlib import sha256, md5

# Takes 16 bytes from right hand side, and hashes them, for xoring into left hand side
def Fsha(right):
    hsh = sha256()
    hsh.update(right)
    # take first 16 bytes of hash output
    xor_to_left = hsh.digest()[:16]
    return xor_to_left

# Takes 16 bytes from right hand side, and hashes them, for xoring into left hand side
def Fmd5(right):
    hsh = md5()
    hsh.update(right)
    # take first 16 bytes of hash output
    xor_to_left = hsh.digest()[:16]
    return xor_to_left


# xor the output of F(right) onto left
def xor(left, Fright):
    result = [0]*16
    for i in range(16):
        # xor bytes one by one
        result[i] = left[i] ^ Fright[i]
    # convert result back to bytes
    return bytes(result)


# run a feistel cipher! https://en.wikipedia.org/wiki/Feistel_cipher
def keyless_feistel(left_half, right_half):
    # round 1
    F_right = Fsha(right_half)
    left_half = xor(left_half,F_right)
    left_half, right_half = right_half, left_half

    # round 2
    F_right = Fmd5(right_half)
    left_half = xor(left_half,F_right)
    left_half, right_half = right_half, left_half

    # round 3
    F_right = Fsha(right_half)
    left_half = xor(left_half,F_right)
    left_half, right_half = right_half, left_half

    # round 4
    F_right = Fmd5(right_half)
    left_half = xor(left_half,F_right)
    left_half, right_half = right_half, left_half

    # round 5
    F_right = Fsha(right_half)
    left_half = xor(left_half,F_right)
    left_half, right_half = right_half, left_half

    # round 6
    F_right = Fmd5(right_half)
    left_half = xor(left_half,F_right)
    
    return left_half, right_half




# read flag in as bytes
with open("flag.txt", "rb") as f:
    flag = f.read()

assert len(flag) == 32

left_half, right_half = flag[:16], flag[16:]

# encrypt flag using a no-key feistel cipher!
encrypted_left, encrypted_right = keyless_feistel(left_half, right_half)

encrypted_flag = encrypted_left + encrypted_right
encrypted_flag_hex = encrypted_flag.hex()

# saving encryption in hex, can convert back to bytes with fromhex
assert bytes.fromhex(encrypted_flag_hex) == encrypted_flag

with open("output.txt", "w") as f:
    f.write(encrypted_flag_hex)
