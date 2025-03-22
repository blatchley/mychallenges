# Writeup
WIP

Multiple possible solutions. 
The "simplest" one mathematically is to recognise that the order things are added to the dictionary messes with the json.dumps. so
```
nonce, ct, tag = registerfullurl(remoteURL + "/register?username=user&?role=user")
nonce1, ct1, tag1 = registerfullurl(remoteURL + "/register?role=user")
nonce2, ct2, tag2 = registerfullurl(remoteURL + "/register?username=user")
```

Will all have different cipher texts but the same nonce.
From here use standard gcm attacks to recover H and C.
Then you can take a ct for the superadmin and isolate the AAD and recover that, and then create a valid signature.


It is also possible to solve without noticing this json behaviour, by taking user and superadmin tokens, and subtracting them from each other, to get relations in the AAD and H. Enough of these let you solve directly with groebner/some smart polynomial manipulation.

Proper writeup coming soon(tm)