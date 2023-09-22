import hashlib
    
def bls_keygen():
    sk = randrange(r)
    return (sk, sk*Q)
    
def bls_hash(M):    
    # Hash the message by hashing to scalar and multiplying generator
    k = Integer(hashlib.sha512(M).hexdigest(), 16) % r
    return k * P
    
def bls_sign(M, sk):
    H = bls_hash(M.encode())
    return (sk * H)
    
def bls_verify(M, S, PK):
    if PK == 0 * Q:
        return false
    H = bls_hash(M.encode())
    return (S.ate_pairing(Q, r, 12, t, p) == H.ate_pairing(PK, r, 12, t, p))

def challenge():
    M = "This is such a lame message to sign."
    (sk, PK) = bls_keygen()
    sig = bls_sign(M, sk)
    assert(bls_verify(M, sig, PK))

    _M = "Hold my beer while I sign all the things!"

    print("This is a BLS signature over a boring message:", M)

    print("\nPublic Key = ", PK)
    print("Signature = ", sig)

    print("\nI challenge you to compute a valid BLS signature over the following message:", _M)
    print("Give me the x and y coordinates and I will give you the flag if the signature is valid!")

    x = int(input())
    y = int(input())
    try:
        new_sig = E(x, y)
    except:
        print("Your BLS signature is not blessed!")
    else:
        new_sig = Ep12(new_sig)

        if (bls_verify(_M, new_sig, PK)):
            flag = open('flag.txt', 'r').read().strip()
            print(flag)
        else:
            print("Your BLS signature is not blessed!")

load("params.sage")

params()
challenge()
