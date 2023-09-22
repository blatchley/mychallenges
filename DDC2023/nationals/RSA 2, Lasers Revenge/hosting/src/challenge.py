# pip3 install pycryptodome
from Crypto.Util.number import getStrongPrime, bytes_to_long, long_to_bytes
import tempfile
import os

class RSA_key:

    def initalise(self,p,q,e):
        # init rsa data
        self.p = p
        self.q = q
        self.e = e
        self.n = p*q
        self.phi = (p-1)*(q-1)
        self.d = pow(e,-1,self.phi)

    # simple key storage format
    def store_key(self, filename):
        try:
            with open(filename, "wb") as f:
                f.write(self.n.to_bytes(2048//8, "little"))
                f.write(self.e.to_bytes(3, "little"))
                f.write(self.p.to_bytes(1024//8, "little"))
                f.write(self.q.to_bytes(1024//8, "little"))
                f.write(self.d.to_bytes(2048//8, "little"))
        except:
            print("something went wrong storing key")
            exit()

    # simple key storage format
    def load_key(self,filename):
        try:
            with open(filename, "rb") as f:
                self.n = int.from_bytes(f.read(2048//8), "little")
                self.e = int.from_bytes(f.read(3), "little")
                self.p = int.from_bytes(f.read(1024//8), "little")
                self.q = int.from_bytes(f.read(1024//8), "little")
                self.d = int.from_bytes(f.read(2048//8), "little")
        except:
            print("something went wrong loading key")
            exit()



def rsa_verify(msg_int,sig,e,n):
    return pow(sig,e,n) == msg_int

# fault injection resistant signing
def rsa_sign(msg_int, key):
    sig = pow(msg_int, key.d, key.n)
    return sig


# fire your laser at the device
def fire_laser():
    idx = int(input("which part of the device do you want to aim your laser at? :"))

    # laser hits the disk as it loads the key
    with open("rsa_key.pem", "rb") as f:
        key = list(f.read())
    try:
        key[idx // 8] ^= 1 << (idx % 8)
    except IndexError:
        print("your laser missed the disk :(")
        exit()
    with open('rsa_key_lasered.pem', 'wb') as f:
        f.write(bytes(key))
    


# load and pad flag
with open("flag.txt", "rb") as f:
    flag = f.read()
flag += os.urandom((250 - len(flag)))
flag = bytes_to_long(flag)

# Device stability checks will abort and dump state if integrity is compromised
def close_connection(enc_flag):
    print("critical system error detected")
    print("ABORT!")
    print("ABORT!")
    print("ABORT!")
    print("dumping encrypted data")
    print(f'flag = {enc_flag}')
    exit()



with tempfile.TemporaryDirectory() as direc:
    os.chdir(direc)

    p,q = getStrongPrime(1024), getStrongPrime(1024)
    e = 65537

    # pad and encrypt flag
    enc_flag = hex(pow(flag,e,p*q))

    # System stores it's signing key on disk
    secret_key = RSA_key()
    secret_key.initalise(p,q,e)
    secret_key.store_key("rsa_key.pem")
    print(f'Public key: N = {secret_key.n}')

    # get some signatures!
    for i in range(0x1337):
        # Shine your laser at the device
        fire_laser()

        # input msg to sign in hex
        msg_to_sign = int(input("message to sign (hex):"),16)
        assert msg_to_sign > 0

        # system loads faulted signing key from the modified memory
        signing_key = RSA_key()
        signing_key.load_key("rsa_key_lasered.pem")

        # Inbuilt integrity check
        if not signing_key.p * signing_key.q == signing_key.n:
            close_connection(enc_flag)

        # signs message
        sig = rsa_sign(msg_to_sign, signing_key)
        print(f'signature (hex): {hex(sig)}')
