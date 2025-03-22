from pwn import remote

# io = process('python3 chal.py'.split())

io = remote("127.0.0.1", 1337, level="debug")

def send_action(action: str) -> None:
    io.sendlineafter(b'flag?', action.encode())

def send_xor(xor_hex: str) -> None:
    send_action('xor')
    io.sendlineafter(b'xor the message with? (hex):', xor_hex.encode())

actions = (
    'hex',
    'encode',
    'hex',
    'encode',
    'hex',
    'encode',
    'hex',
    'encode',
    'hex',
    'encode',
    'hex',
    'encode',
)
for action in actions:
    send_action(action)

# The 0a will xor a `7` to `=` which will be the terminator of the b64decode
send_xor('000aff')
send_action('b64decode')
send_action('b64encode')

send_action('decode')
send_action('done')

known_text = b'393939393939393939393393939393939393939394939393939393939393939393939393939393939393393939393939393939394939393939393939393939393939393939393939390'
io.sendlineafter(b'Lets just confirm that you ended with the same ciphertext I did: ', known_text)
out = io.recvall(timeout=0.2)
print(out.decode())