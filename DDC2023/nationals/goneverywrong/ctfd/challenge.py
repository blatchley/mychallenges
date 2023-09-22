
from Crypto.Util.number import isPrime, getPrime, getStrongPrime
from secretdata import FLAG


# Generate smooth-order primes for fast encryption even with large e
def gen_smooth_prime(PrimeSize, FactorSize, base = 1):
    factorlist = [getPrime(FactorSize) for _ in range((PrimeSize // FactorSize) + 1)]
    while True:
        P = base
        # print(factorlist)
        for pl in factorlist:
            P *= pl
        P = 2*P + 1
        if isPrime(P):
            return P
        else:
            factorlist = factorlist[1:] + [getPrime(FactorSize)]

# Picking a super large super secure e!
e = getPrime(1337)

# Hopefully you guys learned a lot from the qualifier `baby rsa (gone wrong)` challenge! 
# It's nationals now though, so lets step it up a notch! I hope you studied your factoring and dlog algorithms ;)
important_information = getStrongPrime(640)
print(f'my super important information: {important_information}')

# generate fast exponentiation primes, so my large e doesn't slow me down!
p = important_information * gen_smooth_prime(1048 - important_information.bit_length(),15,important_information)
q = important_information * gen_smooth_prime(1048 - important_information.bit_length(),15,important_information)

n = p*q


m = b"That feeling when you go out of your way to make DDC'22 challenges interesting and original, and the easy path of just making 10 RSA challenges. Then the players complain about there being no RSA challenges!?!! I hope they don't come to regret that :D"
q = "Question: Are you ready for a cookie cutter classic RSA crypto challenge? Here's a plaintext and ciphertext to get us started!"
p = int.from_bytes(m,'big')
e = pow(p,e,n)


print(q)
print(f'Plaintext = {m}')
print(f'Encryption = {e}')
print("and my public key!")
print(f'N = {n}')
print(f'e = ...')
# print(f'e = {e}')
# print("now here's the encrypted flag")
# encflag = pow(int.from_bytes(FLAG.encode(),'big'),e,n)
# print(f'enc_flag = {encflag}')

print("oh wait no!!! I accidentally overwrote my primes and my `e` value and lost them! Now I can't even encrypt things let alone decrypt them!")
print("Get them back for me before they realises I broke the challenge, and i'll give you the flag! Please help!")

# This is urgent! They'll find out in one minute!
psyduck = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣆⢀⣶⡶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⢸⠟⣠⣶⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣀⠀⢀⣠⠴⠴⠶⠚⠿⠿⠾⠭⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠴⢋⡽⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠢⣀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⡔⠁⡰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠚⠛⣖⠀⠀⠀⠀
⠀⢀⡏⠀⡼⢡⠚⡛⠒⣄⠀⠀⠀⠀⣠⠖⠛⠛⠲⡄⠐⢯⠁⠀⠀⠹⡧⠀⠀⠀
⠀⣸⠀⠀⡇⠘⠦⣭⡤⢟⡤⠤⣀⠀⠣⣀⡉⢁⣀⠟⠀⠀⢷⠀⠀⠀⠙⣗⠀⠀
⠁⢻⠀⠀⢷⢀⡔⠉⢻⡅⣀⣤⡈⠙⠒⠺⠯⡍⠁⠀⠀⠀⢸⡆⠀⠀⠀⠘⡶⠄
⠀⣈⣧⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣰⠃⠀⠀⠀⠀⣸⡇⠀⠀⠀⠀⠸⣔
⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⣤⡤⠴⠖⠋⢹⠃⠀⠀⠀⠀⠀⣷
⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣻⠁⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⣼
⠙⠑⣤⣀⠀⠀⠀⠀⠀⢀⠀⠀⢄⣐⠴⠋⠀⠀⠀⠀⠀⠀⠘⢆⠀⠀⠀⠀⣰⠟
⠀⠀⠀⣑⡟⠛⠛⠛⠛⠛⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⡾⠋⠀
⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀
⠀⠀⣰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀
⠀⠀⠸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠃⠀⠃
"""

def panic():
    print(psyduck)
    exit()

import signal
def too_slow(_,__):
    print("oh no, you took too long and they realised I lost all my variables! You needed to be faster :(")
    panic()
signal.signal(signal.SIGALRM, too_slow)
signal.alarm(120)

# Please help me!
e_guess = int(input("e = ").strip())

if pow(p,e_guess,n) == e:
    if e_guess.bit_length() == 1337:
        print("thank you so much, you really saved the challenge! Here's the flag")
        print(FLAG)
        exit()
    else:
        print("That can't be my original e, it's the wrong size :(")
        print("Oh no, I'm in so much trouble!")
        panic()
else:
    print("that wasn't the right e, oh no I'm in so much trouble!")
    panic()
