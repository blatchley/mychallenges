import base64
from hashlib import md5

# converts bytes to hex, may fail if called on non bytestring
def make_hex(msg):
    try:
        return True, msg.hex()
    except:
        return False, "something broke trying to hex your message"

# converts hex to bytes, may fail if non hex characters in input
def make_bytes(msg):
    try:
        return True, bytes.fromhex(msg)
    except:
        return False, "something broke trying to bytes from hex your message"

# base64 encodes a bytestring into base64
def make_b64enc(msg):
    # Real encoding crypto challenges don't care about padding, so neither should we
    try:
        return True, base64.b64encode(msg).rstrip(b"=")
    except:
        return False, "Something broke trying to base64 encode your message"

# base64 decodes a base64 encoded string or bytestring, might fail if illegal characters are present
def make_b64dec(msg):
    # Real encoding crypto challenges don't care about padding, so neither should we
    if isinstance(msg, bytes):
        padding = b'='
    else:
        padding = '='

    for padding_len in range(4):
        try:    
            return True, base64.b64decode(msg + padding * padding_len)
        except Exception:
            pass
    return False, "Something broke trying to base64 decode your message"

# encodes an ascii string as a bytestring
def make_encode(msg):
    try:
        return True, msg.encode()
    except:
        return False, "Something broke trying to encode your message"

# decodes a byte string to ascii representation, might fail if non ascii characters are in string
def make_decode(msg):
    try:
        return True, msg.decode()
    except:
        return False, "Something broke trying to decode your message"

# xor two bytestrings together. May fail if an input isn't a bytestring
def xor(a,b):
    res = b''
    for i in range(len(a)):
        res += bytes([a[i] ^ b[i % len(b)]])
    return res

# takes bytestring and lets you xor a (short) crib onto it!
def make_xor(msg, xorval):
    try:
        return True, xor(msg, xorval)
    except:
        return False, "Something broke trying to xor your message"
    
# A good old ECSC hashing step \0/
def make_md5(msg):
    try:
        return True, md5(msg).hexdigest()
    except:
        return False, "Something broke trying to md5 your message"

    