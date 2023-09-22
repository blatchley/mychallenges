import random

# 256 bit prime
p = 97953958723054470944201407781333999671402425802271290596631886639255617548503

# Encrypt a plaintext using a password
def encrypt(plaintext, pw):
    random.seed(pw)
    encryption = plaintext
    for i in range(128):
        a = random.randint(2,2**255)
        b = random.randint(2,2**255)
        c = random.randint(2,2**255)
        if c%2 == 0:
            c -= 1
        encryption = pow((a*encryption + b)%p,c,p)
    return encryption

# Decrypt ciphertext using a password
def decrypt(ciphertext, pw):
    # TODO: Implement decryption
    return ciphertext


if __name__ == '__main__':
    # Read the flag from a file
    with open("flag.txt", "rb") as f:
        flagbytes = f.read().strip()

    # flag starts with the flag prefix, `DDC{`
    assert flagbytes.startswith(b'DDC{')

    # convert bytes to integer
    flag = int.from_bytes(flagbytes, 'big')

    # How to convert the integer back to bytestring
    assert flagbytes == int.to_bytes(flag, (flag.bit_length() + 7) // 8, 'big')

    # Generates a password containing a 4 digit password between 0000 and 9999
    pw = str(random.randint(0,9999)).zfill(4)

    print(pw)

    # Write the encrypted flag to the output.txt file!
    with open('output.txt', 'w') as f:
        f.write(f'p = {p}\n')
        f.write(f'ciphertext = {encrypt(flag, pw)}')