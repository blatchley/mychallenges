# pip3 install pycryptodome
from Crypto.Util.number import getStrongPrime, bytes_to_long, long_to_bytes
import json
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

        # init and store CRT variables for faster signing.
        self.dp = self.d % (self.p - 1)
        self.dq = self.d % (self.q - 1)
        self.u = pow(self.q,-1,self.p)


    # simple key storage format
    def store_key(self, filename):
        try:
            key = {}
            key["n"]  = hex(self.n)[2:]
            key["e"]  = hex(self.e)[2:]
            key["p"]  = hex(self.p)[2:]
            key["q"]  = hex(self.q)[2:]
            key["d"]  = hex(self.d)[2:]
            key["dp"] = hex(self.dp)[2:]
            key["dq"] = hex(self.dq)[2:]
            key["u"]  = hex(self.u)[2:]
            with open(filename, "w") as f:
                f.write(json.dumps(key))
        except:
            print("something went wrong")
            exit()

    # simple key storage format
    def load_key(self,filename):
        try:
            with open(filename, "r") as f:
                key = json.loads(f.read())
            self.n  = int(key["n"] ,16)  
            self.e  = int(key["e"] ,16)  
            self.p  = int(key["p"] ,16)  
            self.q  = int(key["q"] ,16)  
            self.d  = int(key["d"] ,16)  
            self.dp = int(key["dp"],16)  
            self.dq = int(key["dq"],16)  
            self.u  = int(key["u"],16)  
        except:
            print("something went wrong")
            exit()



def rsa_verify(msg_int,sig,e,n):
    return pow(sig,e,n) == msg_int

# CRT accelerated signing!
# see https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Using_the_Chinese_remainder_algorithm
def rsa_sign(msg_int, key):
    m1 = pow(msg_int, key.dp, key.p)
    m2 = pow(msg_int, key.dq, key.q)
    h = (key.u * (m1-m2)) % key.p
    sig = (m2 + h*key.q) % key.n
    return sig


# fire your laser at the device
def fire_laser():
    idx = int(input("which part of the disk do you want to aim your laser at? :"))

    # laser hits the disk
    with open("rsa_key.pem", "rb") as f:
        key = list(f.read())
    try:
        key[idx // 8] ^= 1 << (idx % 8)
    except IndexError:
        print("your laser missed the disk :(")
        exit()
    with open('rsa_key.pem', 'wb') as f:
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


    # get some signatures!
    for i in range(10):
        # input msg in hex
        msg_to_sign = int(input("message to sign (hex):"),16)
        assert msg_to_sign > 0

        # system loads signing key
        signing_key = RSA_key()
        signing_key.load_key("rsa_key.pem")
        # signs message
        sig = rsa_sign(msg_to_sign, signing_key)
        print(f'signature (hex): {hex(sig)}')
        
        # stability check
        if not rsa_verify(msg_to_sign,sig,signing_key.e,signing_key.n):
            close_connection(enc_flag)


    # shoot laser at the device!
    fire_laser()
    print("your laser is shining at the device, i wonder if that did anything 0.0")


    # get some more signatures!
    for i in range(10):
        # input msg in hex
        msg_to_sign = int(input("message to sign (hex):"),16)
        assert msg_to_sign > 0

        # system loads signing key
        signing_key = RSA_key()
        signing_key.load_key("rsa_key.pem")
        # signs message
        sig = rsa_sign(msg_to_sign, signing_key)
        print(f'signature (hex): {hex(sig)}')
        
        # stability check
        if not rsa_verify(msg_to_sign,sig,signing_key.e,signing_key.n):
            close_connection(enc_flag)
    
