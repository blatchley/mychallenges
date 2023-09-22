#!/usr/bin/env python3
from flask import Flask,request,Response,render_template,abort,make_response
import json,random,os,base64

### Global variables
app = Flask(__name__)
allowedPsyducks   = ['normal','king','tea','cold','strong','shy','gentleman','sick','brick','sus','swole','scream','party','cool','panic','fast','happy','irl','oddish','onix','rain','sad','serene','smol','super','triple']
forbiddenPsyducks = ['princess']
allPsyducks = allowedPsyducks + forbiddenPsyducks


### Internal functions
def forbidden_psy(requested_psyduck:str,ip:str):
    if requested_psyduck.lower() in forbiddenPsyducks:
        # Localhost is allowed to view the magnificent psyducks
        if ip == "127.0.0.1":
            return
        # Outsiders are not!
        else:
            return abort(401)
    else:
        return

def check_favorite_requested(requested_psyduck:str,favourite_psyducks:list):
    return requested_psyduck in favourite_psyducks

def check_favorite_forbidden(favourite_psyducks:list):
    for favourite_psyduck in favourite_psyducks:
        if favourite_psyduck in forbiddenPsyducks:
            return False
    return True


### Flask functions
@app.route('/supersecretbackup/backup.zip')
def backup():
    return Response(backup_zip, mimetype='application/zip')

@app.route('/browse')
def dir_listing():
    # Show directory contents
    return render_template('browse.html')

@app.route('/content')
def retPsyduck():
    user_request = request.args.get('psyduck')
    user_ip = request.environ['REMOTE_ADDR']
    user_cookie = json.loads(base64.b64decode(request.cookies.get('MyFavoritePsyducks')).decode())['psy']

    # Ensure the requested psyducks is a favorite!
    if not check_favorite_requested(user_request,user_cookie):
        return Response('You can only request your favorite psyducks!')

    # Ensure user doesn't covet any forbidden psyducks!
    if not check_favorite_forbidden(user_cookie):
        return Response('You are not allowed to like that psyduck!')

    # Check the requested psyduck is not forbidden!
    forbidden_psy(user_request,user_ip)

    if user_request.casefold() in allPsyducks:
        if not check_favorite_requested(user_request.casefold(), user_cookie):
            return Response('You can only request your truly most favourite of psyducks!')
        with open('psyducks/'+user_request.casefold()+'.png','rb') as f:
            return Response(f.read(), mimetype='image/png')
    else:
        return Response('No Psyduck requested!')

@app.route("/")
def index():
    n = random.randint(0, len(allowedPsyducks)-1)
    res = make_response()
    cookie = base64.b64encode(json.dumps({'psy':allowedPsyducks}).encode())
    res.set_cookie('MyFavoritePsyducks', cookie)
    res.set_data(indexTemplate.replace('ZZZ',allowedPsyducks[n]))
    return res


### Main
with open('./templates/index.html') as f:
    indexTemplate = f.read()

with open('./supersecretbackup/backup.zip','rb') as f:
    backup_zip = f.read()

if(__name__ == '__main__'):
    app.run(host='0.0.0.0')
