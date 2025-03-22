#!/usr/bin/env python3
from flask import Flask,request,Response,render_template,abort,make_response
import json,random,os,base64
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256, md5
import time
import random
### Global variables
app = Flask(__name__)

secret_key = os.urandom(16)
super_admin_secret = os.urandom(16)


# Encrypt data using AES_GCM
def encryption(data, context):

    # super securely hash a payload into a unique nonce with some hacky length encoding stuff
    payload = data["username"] + f'::{len(data["username"])}::' + data["role"] + f'::{len(data["role"])}::' + str(data["expirytime"])
    nonce = sha256(payload.encode()).digest()
    
    # Encrypt cookie
    pt = json.dumps(data).encode()
    cipher = AES.new(secret_key, AES.MODE_GCM, nonce = nonce)
    cipher.update(context)
    ct, tag = cipher.encrypt_and_digest(pt)
    cookie = nonce.hex() + "." + ct.hex() + "." + tag.hex()
    return cookie


# create secure AES_GCM authenticated user cookie!
def gen_cookie(data, context = b'basicusercontext'):
    # Set expiry time for cookie (default 1 hour)
    expirytime = int(time.time()) + 3600
    data["expirytime"] = expirytime
    
    # Default user identification
    if "username" not in data:
        data["username"] = "user"
    if "role" not in data:
        data["role"] = "user"

    # Generate encrypted cookie
    cookie = encryption(data, context)
    return cookie


# decode cookie!
def decode_cookie(cookie, context = b'basicusercontext'):
    cookie = cookie.split(".")
    nonce, ct, tag = [bytes.fromhex(x) for x in cookie]
    cipher = AES.new(secret_key, AES.MODE_GCM, nonce = nonce)
    cipher.update(context)
    pt = cipher.decrypt_and_verify(ct,tag).decode()
    cookie_dict = json.loads(pt)

    # Check expiry time
    assert cookie_dict["expirytime"] > int(time.time()), 'expired cookie'

    return cookie_dict


# Authorisation for viewing user psyducks!
@app.route('/viewuser')
def viewBasic():
    user_cookie = request.cookies.get('permissions')

    if user_cookie == None:
        return Response("No cookie set")
    try:
        cookie_dict = decode_cookie(user_cookie)
    except:
        return Response("Something went wrong with your cookie, maybe it expired?")
    
    username = cookie_dict["username"]
    role = cookie_dict["role"]

    if not role in ["user", "admin"]:
        return Response(f'You need a valid role to view user psyducks, your role is: {role}')
    
    requested_duck = random.choice(["fast.png", "party.png", "strong.png", "panic.png"])

    with open(f'./images/{requested_duck}', 'rb') as f:
        return Response(f.read(), mimetype='image/png')

# Authorisation for viewing Admin psyducks!
@app.route('/viewadmin')
def viewAdmin():
    user_cookie = request.cookies.get('permissions')

    if user_cookie == None:
        return Response("No cookie set")
    try:
        cookie_dict = decode_cookie(user_cookie)
    except:
        return Response("Something went wrong with your cookie, maybe it expired?")
    
    username = cookie_dict["username"]
    role = cookie_dict["role"]
    if not username == "admin":
        return Response(f'you need admin username to view admin psyducks. Your username is: {username}')
    if not role == "admin":
        return Response(f'you need admin role to view admin psyducks. Your role is: {role}')
    

    with open(f'./images/adminduck.png', 'rb') as f:
        return Response(f.read(), mimetype='image/png')


# Authorisation for viewing super admin psyducks!
@app.route('/viewsuperadmin')
def viewSuperAdmin():
    user_cookie = request.cookies.get('permissions')

    if user_cookie == None:
        return Response("No cookie set")
    # try:
    cookie_dict = decode_cookie(user_cookie, context=super_admin_secret)
    # except:
    #     return Response("Something went wrong with your super admin cookie, maybe it expired or something?")
    
    username = cookie_dict["username"]
    role = cookie_dict["role"]
    if not username == "admin":
        return Response(f'you need admin username to view super admin psyducks. Your username is: {username}')
    if not role == "admin":
        return Response(f'you need the admin role to view super admin psyducks. Your role is: {role}')
    
    

    # super admin can read any psyduck!
    try:
        psyduck = bytes.fromhex(request.args.get('psyduck'))
        print(psyduck)
        requested_duck = AES.new(super_admin_secret, AES.MODE_CTR, nonce=psyduck[:12]).decrypt(psyduck[12:])
        with open(f'./images/{requested_duck.decode()}', 'rb') as f:
            return Response(f.read(), mimetype='image/png')
    except:
        # Not sure what went wrong, but have an admin psyduck :)
        with open(f'./images/adminduck.png', 'rb') as f:
            return Response(f.read(), mimetype='image/png')




# Browse psyduck menus
def browsePsy():
    user_cookie = request.cookies.get('permissions')
    if user_cookie == None:
        return Response("No cookie set")
    try:
        cookie_dict = decode_cookie(user_cookie)
    except:
        return Response("Something went wrong with your cookie")

    username = cookie_dict["username"]
    role = cookie_dict["role"]

    res = make_response()
    with open('./templates/view.html', 'r') as f:
        data = f.read()
    
    data = data.replace("ZZuserZZ", username)
    data = data.replace("ZZroleZZ", role)

    res.set_data(data)
    return res


# Register for an account
@app.route('/register')
def register():

    registration_data = {}

    username = request.args.get('username')
    if username:
        # No registering as admin user
        if username == "admin":
            return Response("Attempted to register as an illegal user: admin")
        registration_data["username"] = username
    
    role = request.args.get('role')
    if role:
        # No registering as admin role
        if role == "admin":
            return Response("Attempted to register with an illegal role: admin")
        registration_data["role"] = role

    cookie = gen_cookie(registration_data)

    res = make_response()
    res.set_cookie('permissions', cookie)
    with open('./templates/view.html', 'r') as f:
        data = f.read()

    data = data.replace("ZZuserZZ", username if username else "user")
    data = data.replace("ZZroleZZ", role if role else "user")

    res.set_data(data)
    return res

# Register for a super admin account
### NOTE: Due to security concerns we have temporarily disabled configuring accounts through this endpoint
@app.route('/registerSuperAdmin')
def registerSuperAdmin():

    registration_data = {}

    ### NOTE: Due to security concerns we have temporarily disabled configuring accounts through this endpoint

    # username = request.args.get('username')
    # if username:
    #     registration_data["username"] = username
    
    # role = request.args.get('role')
    # if role:
    #     registration_data["role"] = role

    cookie = gen_cookie(registration_data, context=super_admin_secret)

    res = make_response()
    res.set_cookie('permissions', cookie)
    
    with open('./templates/view.html', 'r') as f:
        data = f.read()

    # Registration is temporarily disabled
    data = data.replace("ZZuserZZ", "SuperAdmin (disabled)")
    data = data.replace("ZZroleZZ", "SuperAdmin (disabled)")
    
    res.set_data(data)
    return res


@app.route("/")
def index():
    user_cookie = request.cookies.get('permissions')
    # if no cookie send to register page, otherwise send to browsing page
    if user_cookie == None:
        res = make_response()
        with open('./templates/register.html', 'r') as f:
            res.set_data(f.read())
        return res
    else:
        return browsePsy()



if(__name__ == '__main__'):
    app.run(host='0.0.0.0')
