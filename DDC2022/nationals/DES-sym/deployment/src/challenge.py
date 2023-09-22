import pyDes  #Pure python DES implementation. Taken unchanged from https://gist.github.com/eigenein/1275094
import os

# some memes about breaking kidz but now hash is UPGRADED TO NSA APPROVED CRYPTO

def rotate(n, d):
    n = int(n.hex(), 16)
    return bytes([((n << d)%256)|(n >> (8 - d))])

def xor(a,b):
    return bytes([x ^ y for x,y in zip(a, b)])

def bytes_to_blocks(a):
    return [a[i:i+8] for i in range(0,len(a), 8)]

# My hash function is too important to be called on boring data!
def test_interestingness(message):
    message_blocks = bytes_to_blocks(message)
    interestingblocks = []
    for block in message_blocks:
        if not block in interestingblocks:
            interestingblocks.append(block)
        else:
            print("one of your blocks was all boring and repetitive!")
            print("Don't worry, i made it more interesting for you :)")
            interestingblocks.append(os.urandom(8))
    return b"".join(interestingblocks)


# Hash data using secret key
def Hash(secret_key, message):
    message_blocks = bytes_to_blocks(message)
    roundkey = secret_key
    keyshift = b'\x55'
    
    hash_stream = b''
    # encrypt data
    for block in message_blocks:
        cipher = pyDes.des(roundkey, pyDes.ECB)
        hash_stream += cipher.encrypt(block)
        roundkey = xor(roundkey, keyshift * 8)
        keyshift = rotate(keyshift,1)
    
    # compress date
    hashed_blocks = bytes_to_blocks(hash_stream)
    for _ in range(3):
        compressed_blocks = []
        for i in range(0,len(hashed_blocks), 2):
            compressed_block = xor(hashed_blocks[i], hashed_blocks[i+1])
            compressed_blocks.append(compressed_block)
        hashed_blocks = compressed_blocks
    
    hashed_message = b''.join(hashed_blocks)
    return hashed_message


if __name__ == "__main__":
    # I've secured my hash using a secret key! Now there's no way you'll break it
    secret_key = os.urandom(8)

    # Send exactly 256 bytes, hex encoded
    request = input("Please give 256 bytes of data in hex!")
    message = bytes.fromhex(request)
    
    if not len(message) == 256:
        print("please give exactly 256 bytes of hex!")
        exit()

    # My new hash function is way too cool for boring data, so i just want to make sure your data is interesing enough to be worth hashing
    interesting_message = test_interestingness(message)

    # Hash your message
    hashed_message = Hash(secret_key, interesting_message)

    #Only comands which has to 0 are allowed to be run on this system!
    if int(hashed_message.hex()) == 0:
        # runs "message" as command in the current folder!
        if message.startswith(b'sudo cat flag.txt'):
            print(f"Well done! Running your command:\n{message}")
            print(open("flag.txt", "r").read().strip())
            # output = stream.read()
        #    print(output)
        else:
            print("congratz! you found something that hashes to 0!")
            print("Try doing it again but where you print the flag!")

    else:
        print(f"No no no no, I needed a 0 hash, but your input:\n{message}\nhashed to: \n{hashed_message.hex()}")