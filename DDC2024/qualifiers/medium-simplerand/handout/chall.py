import random

# How random is random 0.0

with open("flag.txt", "rb") as f:
    Flag = f.read()

with open("output.txt", "w") as f:
    for i in range(624):
        f.write(f'{random.getrandbits(32)}\n')

    while Flag:
        FlagPre, Flag = Flag[:4], Flag[4:]
        otp = random.getrandbits(32)
        res = int.from_bytes(FlagPre,"big")
        f.write(f'{res^otp}\n')
    
