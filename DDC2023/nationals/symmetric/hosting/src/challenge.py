from symmetric import AuthenticatedCipher

def contains_flag(pt):
    return b'give_me_the_flag' in pt

cipher = AuthenticatedCipher()

print("Welcome to my new secure symmetric cipher suite messaging service!!")

# 10 tries to break it!
for _ in range(10):
    # rerandomise the key
    cipher.rerandomise_key()

    print("give a sender_id and a message")
    uname = bytes.fromhex(input("sender_id (hex): "))
    msg = bytes.fromhex(input("message (hex): "))

    # no asking for the flag allowed!
    assert not contains_flag(uname)
    assert not contains_flag(msg)

    uname_nonce, uname_enc, uname_mac = cipher.encrypt_and_mac(uname)
    msg_nonce, msg_enc, msg_mac = cipher.encrypt_and_mac(msg)

    print(f'enc_user: {uname_nonce.hex() + ":" + uname_enc.hex() + ":" + uname_mac.hex()}')
    print(f'enc_msg: {msg_nonce.hex() + ":" + msg_enc.hex() + ":" + msg_mac.hex()}')


    # user gets one message before we rerandomise keys :)
    user_msg = input("one message (hex):")

    m_nonce, m_enc, m_mac = [bytes.fromhex(x) for x in user_msg.split(":")]
    pt, verified = cipher.decrypt_and_verify(m_nonce, m_enc, m_mac)
    if not verified:
        print("mac was invalid :(")

    elif contains_flag(pt):
        print("Wow, how did you do that??")
        with open("flag.txt", "r") as f:
            print(f.read())
            exit()
    else:
        print("thanks for the message")
    

