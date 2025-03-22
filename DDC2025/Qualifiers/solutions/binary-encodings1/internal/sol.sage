
with open("output.txt", "r") as f:
    data = f.read()


# nasty parsing hack. Don't use on untrusted output.txt xd
exec(data)

mods = [p_0, p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8, p_9, p_10, p_11, p_12, p_13, p_14, p_15, p_16, p_17, p_18, p_19, p_20, p_21, p_22, p_23, p_24, p_25, p_26, p_27, p_28, p_29, p_30, p_31]
vals = [f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16, f_17, f_18, f_19, f_20, f_21, f_22, f_23, f_24, f_25, f_26, f_27, f_28, f_29, f_30, f_31]

fullvalue = crt(vals,mods)
print(int(fullvalue).bit_length())
from Crypto.Util.number import long_to_bytes

v1 = int.to_bytes(int(fullvalue), byteorder='big', length=int(fullvalue).bit_length() // 8 + 1)
print(v1)
v2 = v1.decode()
v3 = v2[2:]
v4 = int(v3,2)
v5 = int.to_bytes(v4, byteorder='big', length=31)
print(v5)