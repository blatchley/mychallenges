import requests


TargetUrl = "http://127.0.0.1:13337/submitdata"

# Here's the basic script i use when i need to back up data!
def upload_data(encrypted_bytes):
    encrypted_data = encrypted_bytes.hex()
    payload = {}
    payload["submitted_data"] = encrypted_data
    resp = requests.post(TargetUrl, data=payload)
    timetaken = resp.elapsed.total_seconds()
    print(timetaken)
    return resp.text


encrypted_data = bytes.fromhex("aa"*32)

print(upload_data(encrypted_data))