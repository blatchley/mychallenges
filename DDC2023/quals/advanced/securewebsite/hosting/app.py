#!/usr/bin/env python3
from flask import Flask,request,Response,render_template,abort,make_response
import json,random,os,base64
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import time
### Global variables
app = Flask(__name__)

secret_key = os.urandom(16)

# create valid encryptions for my images!
def encrypt_request(imagename):
    pt = imagename.encode()
    pt = pad(pt,16)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    ct = cipher.encrypt(pt).hex()
    return ct

# create valid encryptions for my images!
def decrypt_request(duck_id):
    ct = bytes.fromhex(duck_id)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    paddedpt = cipher.decrypt(ct)
    pt = unpad(paddedpt,16).decode()
    return pt

# My images!
images = ["fast.png", "gentleman.png", "panic.png", "party.png", "strong.png", "flag.png"]

encrypted_requests = {}
# Create image Identifiers for publicly available images
for image in images[:-1]:
    encrypted_requests[image] = encrypt_request(image)


# create secure AES_GCM authenticated user cookie!
def gen_user_cookie(username, nonce = None):
    if nonce == None:
        nonce = os.urandom(12)
    cookie_dict = {}
    cookie_dict["username"] = username
    cookie_dict["admin_access"] = False
    pt = json.dumps(cookie_dict).encode()
    cipher = AES.new(secret_key, AES.MODE_GCM, nonce = nonce)
    ct, tag = cipher.encrypt_and_digest(pt)
    cookie = nonce.hex() + "." + ct.hex() + "." + tag.hex()
    return cookie

# decode cookie!
def decode_cookie(cookie):
    cookie = cookie.split(".")
    nonce, ct, tag = [bytes.fromhex(x) for x in cookie]
    cipher = AES.new(secret_key, AES.MODE_GCM, nonce = nonce)
    pt = cipher.decrypt_and_verify(ct,tag).decode()
    cookie_dict = json.loads(pt)
    return cookie_dict


@app.route('/view')
def viewPsy():
    user_cookie = request.cookies.get('permissions')
    duck_id = request.args.get('psyduck')

    if user_cookie == None:
        return Response("No cookie set")
    try:
        cookie_dict = decode_cookie(user_cookie)
    except:
        return Response("Something went wrong with your cookie")

    try:
        requested_duck = decrypt_request(duck_id)
    except:
        return Response("something went wrong during decryption of your duck id")
    
    if requested_duck not in images:
        return Response("invalid duck requested")
    username = cookie_dict["username"]
    access_level = cookie_dict["admin_access"]
    if not requested_duck in ["strong.png", "party.png"] and not access_level:
        return Response("Psyducks other than strong duck and party duck require admin access to view.")
    
    with open(f'./images/{requested_duck}', 'rb') as f:
        return Response(f.read(), mimetype='image/png')



@app.route('/register')
def register():
    username = request.args.get('username')

    if username == None:
        return Response("attempted to register without username")
    
    # nonce api for tesing
    nonce = request.args.get('nonce')
    try:
        assert not nonce == None
        nonce = bytes.fromhex(nonce)
        assert len(nonce) == 16
        cookie = gen_user_cookie(username, nonce)
    except:
        cookie = gen_user_cookie(username)

    res = make_response()
    res.set_cookie('permissions', cookie)
    with open('./templates/view.html', 'r') as f:
        data = f.read()

    data = data.replace("ZZuserZZ", username)
    data = data.replace("ZZstrongZZ", encrypted_requests["strong.png"])
    data = data.replace("ZZpartyZZ", encrypted_requests["party.png"])
    data = data.replace("ZZgentlemanZZ", encrypted_requests["gentleman.png"])
    res.set_data(data)
    return res



def browsePsy():
    user_cookie = request.cookies.get('permissions')
    if user_cookie == None:
        return Response("No cookie set")
    try:
        cookie_dict = decode_cookie(user_cookie)
    except:
        return Response("Something went wrong with your cookie")

    username = cookie_dict["username"]


    res = make_response()
    with open('./templates/view.html', 'r') as f:
        data = f.read()
    
    data = data.replace("ZZuserZZ", username)
    data = data.replace("ZZstrongZZ", encrypted_requests["strong.png"])
    data = data.replace("ZZpartyZZ", encrypted_requests["party.png"])
    data = data.replace("ZZgentlemanZZ", encrypted_requests["gentleman.png"])

    res.set_data(data)
    return res




@app.route("/")
def index():
    user_cookie = request.cookies.get('permissions')
    if user_cookie == None:
        res = make_response()
        with open('./templates/register.html', 'r') as f:
            res.set_data(f.read())
        return res
    else:
        return browsePsy()



if(__name__ == '__main__'):
    app.run(host='0.0.0.0')
