import utils

with open("flag.txt", "rb") as f:
    Flag = f.read()

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!?_{}0123456789"
for x in Flag.decode():
    assert x in alphabet


# list of cyberchef approved encryption methods
TRANSFORMS = {}
TRANSFORMS["b64encode"] = utils.make_b64enc
TRANSFORMS["b64decode"] = utils.make_b64dec
TRANSFORMS["hex"] = utils.make_hex
TRANSFORMS["bytes"] = utils.make_bytes
TRANSFORMS["encode"] = utils.make_encode
TRANSFORMS["decode"] = utils.make_decode
TRANSFORMS["xor"] = utils.make_xor
TRANSFORMS["md5"] = utils.make_md5


if __name__ == '__main__':
    print("Welcome to the DDC Crypto Challenge Creation Tool!")
    print("Lets make a high quality challenge!")

    # bytestring of the flag
    flag = Flag
    
    for _ in range(200):
        print(flag)
        action = input("What should we do to the flag?")

        # finished!
        if action == "done":
            break
        
        # Transform should exist
        if action not in TRANSFORMS:
            print('Invalid transform! Try again.')
            continue

        # Apply the Transform
        if action == "xor":
            xorval = input("what would you like to xor the message with? (hex):")
            # cyberchef kinda chugs for cribs longer than 3
            xorval = bytes.fromhex(xorval)[:3]
            succ, msg = TRANSFORMS[action](flag, xorval)
        else:
            succ, msg = TRANSFORMS[action](flag)


        # your transform should succeed
        if not succ:
            print(msg)
            exit()

        # pls no cheesey unsolveable challenges
        if len(msg) < len(Flag):
            print('How are the players meant to solve it if the ciphertext is shorter than the flag???')
            print(f'Your challenge has a ciphertext which is {len(msg)} bytes long, but the flag was {len(Flag)}')
            exit()

        # LETS GOOOOOO
        flag = msg
        print(f"you successfully applied {action} to the flag! This challenge is looking great so far!")
        

    # Nicely done! Just some formalities left.
    print("Well done, you've created a crypto challenge!!!")
    flag_guess = input("Lets just confirm that you ended with the same ciphertext I did: ")
    
    if len(flag_guess) != len(flag):
        print(f"Oh no, thats not even the right length... By my math the encryption should be {len(flag)} characters.")
        exit()

    if flag_guess != flag:
        print("Wait that's not right, lets try again")
        exit()

    print(f"Nice! Lets deploy the challenge now, i wonder if they'll ever be able to recover {Flag} from {flag} :monkahmm:")
