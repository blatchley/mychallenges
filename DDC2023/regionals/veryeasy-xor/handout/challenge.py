import os

# read flag in as bytes
with open("flag.txt", "rb") as f:
    flag = f.read()

# XOR's two bytestrings together. 
def xor(a,b):
    xor_result = b''
    for i in range(len(a)):
        xor_result += bytes([a[i]^b[i]])
    return xor_result


# sample a completely random 200 byte one time pad!
one_time_pad = os.urandom(200)


# two similar messages are sent using the same pad.
msg1 = b'was the flag for the challenge ' + flag
msg2 = b'yeah, the flag was definitely ' + flag

enc_msg_1 = xor(msg1,one_time_pad)
enc_msg_2 = xor(msg2,one_time_pad)

# convert bytes to/from hex for easy storage
assert bytes.fromhex(enc_msg_1.hex()) == enc_msg_1

print(f'enc_msg_1 = {enc_msg_1.hex()}')
print(f'enc_msg_2 = {enc_msg_2.hex()}')