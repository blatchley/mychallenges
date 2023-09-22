# SSS code taken from https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing#Python_example
# Code is unedited except for the addition of the `make_set_shares` function
import pySSS


# HUGE prime for HUGE security!
p = 156507240814763934191750445881983197486927480042673140908527922923020905623855903208457994966957179893992207518948656389074363850504420848982191538180311277409495670055255501990571073045635567706126902714421904255206378339714858109337628554748911648298304924127093648075772941710427425343776236743140177012103


userIDs = [ b'coin founder who is a billionare now and hosts yacht parties', 
            b'bitconneeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeect dude', 
            b'bob from accounting', 
            b'billionaire investor who has no idea what blockchain is',
            b'barry who browses WSB and yolod savings into this project',
            b'big banking guy who keeps losing his secret key and asking customer support to send him a new one',
            b'cryptobro who keeps talking about how id based SSS is the FUTURE OF FINANCE',
            b'phd student coasting on blockchain hype to have a fully funded crypto phd he pretends is actually about blockchain',
            b'someone trying to start a DAO',
            b'ctf author who thinks solodity rev counts as "crypto challenges"']

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    
def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

# Generates a "k of n" shamir secret sharing of the flag
def get_shares(flag, k, n, prime, userid):
    ids = [int_from_bytes(userid)] + [int_from_bytes(userIDs[x]) for x in range(n-1)]
    # make_set_shares returns tuples of the form (id, share) where share is the polynomial evaluated at index id 
    shares = pySSS.make_set_shares(flag, k, ids, prime)
    return shares

if __name__ == "__main__":
    flag = open("flag.txt", "rb").read().strip()
    flag_int = int_from_bytes(flag)

    print("please supply parameters for K out of N sharing scheme as integers")
    print(f"where: 2<N<{len(userIDs) + 2}, K <= N")
    n = int(input("N:"))

    assert n > 2 and n <= len(userIDs) + 1

    k = int(input("K:"))
    assert k <= n

    print("please give your id (encoded as a hex string)")
    id = bytes.fromhex(input("ID:"))

    if int_from_bytes(id) == 0:
        print("ERROR: NULL ID")
        exit()
    
    shares = get_shares(flag_int,k,n,p, id)

    # confirm that subsets of k shares can recover key
    assert int_to_bytes(pySSS.recover_secret(shares[:k], p)) == flag
    assert int_to_bytes(pySSS.recover_secret(shares[-k:], p)) == flag

    print(f"here's the first k-1 = {k-1} shares")
    for x in range(k-1):
        print(shares[x])
