#!/usr/bin/env python3
from flask import Flask,request,Response,render_template,abort,make_response
import json,random,os,base64
from Crypto.Cipher import AES
### Global variables
app = Flask(__name__)

secret_key = os.urandom(16)
ctr_nonce = os.urandom(8)

def gen_user_cookie():
    cookie_dict = {}
    cookie_dict["access_level"] = "User"
    pt = json.dumps(cookie_dict).encode()
    cipher = AES.new(secret_key, AES.MODE_CTR, nonce = ctr_nonce)
    ct = cipher.encrypt(pt).hex()
    return ct

def check_admin_cookie(cookie):
    ct = bytes.fromhex(cookie)
    cipher = AES.new(secret_key, AES.MODE_CTR, nonce = ctr_nonce)
    pt = cipher.decrypt(ct).decode()
    cookie_dict = json.loads(pt)
    if cookie_dict["access_level"] == "Admin":
        return True
    else:
        return False


@app.route('/flag')
def retPsyduck():
    user_cookie = request.cookies.get('permissions')
    if user_cookie == None:
        return Response("No cookie set")
    try:
        allowed = check_admin_cookie(user_cookie)
    except:
        return Response("Something went wrong with your cookie")

    if allowed: 
        with open('images/flag.png','rb') as f:
                return Response(f.read(), mimetype='image/png')
    else:
        return Response("This page is for admins only!")


@app.route("/")
def index():
    res = make_response()
    cookie = gen_user_cookie()
    res.set_cookie('permissions', cookie)
    with open('./templates/index.html') as f:
        res.set_data(f.read())
    return res



if(__name__ == '__main__'):
    app.run(host='0.0.0.0')
