from hashlib import sha256, md5
from random import randint

p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
A = p - 3
B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
# Nist P256 curve,  y^2 = x^3 + A*x +B over GF(P) 
EE = EllipticCurve(GF(p), [A,B])
G = EE(0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5)
# Curve order
qq = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
EE.set_order(qq)

# Deterministically generate a unique k for ECDSA signature
# Hash function ensures uniqueness, static nonce_key prevents predicting k!
def generate_k(msg, nonce_key):
    # sha256 padded with secret
    # This should definitely prevent any way of predicting any relation between msg and k!
    temp = sha256(msg + str(nonce_key).encode()).digest() 
    k = int(md5(temp).digest().hex(),16)   
    k = k ^^ nonce_key
    return k

# ECDSA sign
def sign(msg,nonce_key, sk):
    # Hash message
    h = int(sha256(msg).digest().hex(),16)
    # generate per-message unique nonce
    k = generate_k(msg,nonce_key) 
    # generate signature
    xn, _ = (k*G).xy()
    r = Integer(xn)
    s = Integer((h + r*sk)*inverse_mod(k, qq) % qq)
    return r, s

# ECDSA verify
def verify(h, r, s, P):
    a = h * inverse_mod(s, qq) % qq
    b = r * inverse_mod(s, qq) % qq
    x, y = (a*G + b*P).xy()
    return x == r

# Receive data from user to sign
def sign_message(sk, nonce_key):
    # Read message to sign
    try:
        msg = bytes.fromhex(input("Message (hex): "))
    except:
        print("invalid hex input")
        exit()

    # Asking for flag is not allowed!
    if b'Flag Please' in msg:
        print(f"I'm not signing {msg}, go away no flag for you!")
        exit()
    
    # sign message
    r,s = sign(msg, nonce_key, sk)
    print(f'Here is your signature on message: {msg}')
    print(f'r: {hex(r)}')
    print(f's: {hex(s)}')

# receive signature from user to verify
def verify_message(P):
    # read in data to verify
    try:
        msg = bytes.fromhex(input("Message (hex): "))
        r = int(input("sig.r (hex): "), 16)
        s = int(input("sig.s (hex): "), 16)
    except:
        print("invalid hex input")
        exit()

    # Verify signature
    h = int(sha256(msg).digest().hex(),16)
    valid = verify(h,r,s,P)
    if not valid:
        print("Signature was invalid")
        exit()
    else:
        # Sign the message b'Flag Pls' to win
        if msg == b'Flag Please':
            print("A valid signature asking for my flag! Here you go!")
            with open("flag.txt", "rb") as f:
                print(f.read())
            exit()
        else:
            print(f"The signature on {msg} was valid!")
    
def options():
    print("")
    print("1- Sign message")
    print("2- Verify signature")
    print("3- Close")
    try:
        request = int(input())
    except:
        print("invalid input")
        return 3
    return request


def main():
    # Generate secret signing key
    sk = randint(2,qq)
    # public verification key
    P = sk*G
    # secret padding to avoid short nonces
    nonce_key = randint(2,qq)
    
    print("Welcome to my signing service, using only the greatest elliptic curve digital signature algorithms!")
    print("You are permitted to sign everything except requests for the flag!")
    print("Now featuring new and improved Nonce generation!")
    print(f'The public verification point is {P}')
    while True:
        choice = options()
        if choice == 1:
            sign_message(sk,nonce_key)
        elif choice == 2:
            verify_message(P)
        else:
            exit()


if __name__ == "__main__":
    main()