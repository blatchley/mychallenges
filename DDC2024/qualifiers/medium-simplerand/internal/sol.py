with open("output.txt", "r") as f:
    data = f.readlines()


from randcrack import RandCrack


rc = RandCrack()

for i in range(624):
      
	rc.submit(int(data[i].strip()))
	# Could be filled with random.randint(0,4294967294) or random.randrange(0,4294967294)

result = []

data = data[624:]
while data:
    v, data = int(data[0]), data[1:]
    otp = rc.predict_randrange(0, 4294967295)
    l = v ^ otp
    result.append(int.to_bytes(l,4,"big"))

print(b"".join(result))
