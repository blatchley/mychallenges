from flask import Flask, send_from_directory, jsonify, render_template, request, make_response, g
import os, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)


### Cookie encryption/decryption functions ###
# Cookie Encryption
def encrypt_cookie(auth, key):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    authenc = iv + cipher.encrypt(pad(auth,16))
    cookie = authenc.hex()
    return cookie

# Cookie Decryption
def decrypt_cookie(cookie, key):
    iv, ct = cookie[:32], cookie[32:]
    cipher = AES.new(key, AES.MODE_CBC, iv=bytes.fromhex(iv))
    auth = cipher.decrypt(bytes.fromhex(ct))
    return auth
##############################

@app.route('/')
def home():
   return send_from_directory('.', 'index.html')

# Flag only accessible if you have an encrypted cookie where flag is set to True
@app.route('/flag')
def flag():

    encryptedcookie = request.cookies.get('permissions')
    if encryptedcookie == None:
        return send_from_directory('.', 'nocookie.html')

    try:
        cookie = decrypt_cookie(encryptedcookie, key)
        cookie = unpad(cookie,16)
        auth = json.loads(cookie)
    except Exception as e:
        return "An ERROR has occured while trying to handle your cookie: " + str(e)

    if auth["flag"]:
        return send_from_directory('.', 'flag.html')
    else:
        return send_from_directory('.', 'notflag.html')

# Grants an encrypted cookie, json encoding of flag = False
@app.route('/auth')
def auth():
    auth = json.dumps({"flag":False})
    resp = make_response(send_from_directory('.', 'auth.html'))
    authcookie = encrypt_cookie(auth.encode("utf-8"), key)
    resp.set_cookie('permissions', authcookie)
    return resp

# Decrypts and displays cookie
@app.route('/debug')
def debug():
    encryptedcookie = request.cookies.get('permissions')
    if encryptedcookie == None:
        return send_from_directory('.', 'nocookie.html')
    
    try:
        cookie = decrypt_cookie(encryptedcookie, key)
    except Exception as e:
        return "An ERROR has occured while trying to handle your cookie: " + str(e)

    return render_template('debug.html', cookieval=cookie.decode("utf-8", "replace"), hexcookie = cookie.hex())

# Helper function to reduce web caching black magic :psyduck:
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

if __name__ == "__main__":
    key = os.urandom(16)

    app.run(host='0.0.0.0', port=os.getenv('PORT'))
