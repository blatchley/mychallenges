from Crypto.Cipher import AES
from hashlib import sha256
import os

class AuthenticatedCipher:

    def __init__(self):
        self.key = os.urandom(16)
    
    # encrypt bytestring, and add message authenticated code
    def encrypt_and_mac(self, pt):
        mac = self.make_mac(pt)
        cipher = AES.new(self.key, AES.MODE_CTR)
        ct = cipher.encrypt(pt)
        nonce = cipher.nonce
        return nonce, ct, mac

    # decrypt and verify mac 
    def decrypt_and_verify(self,nonce,ct,mac):
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=nonce)
        pt = cipher.decrypt(ct)
        verified = mac == self.make_mac(pt)
        return pt, verified

    # Merkle-Damgaard style mac
    def make_mac(self, pt):
        msg_len = len(pt)
        paddedpt = pt + b'\x00' * ((16 - len(pt))%16)
        payload = paddedpt + msg_len.to_bytes(16,"big")
        mac = self.prp(self.key)
        while payload:
            r, payload = self.prp(payload[:16]), payload[16:]
            h = sha256()
            h.update(mac + r)
            mac =  h.digest()
        return mac

    def prp(self, pt):
        prp_cipher = AES.new(b'Even_Mansour_key', AES.MODE_ECB)
        return bytes([a^b for a,b in zip(pt, prp_cipher.encrypt(pt))])
    
    # rerandomise key
    def rerandomise_key(self):
        self.key = os.urandom(16)
