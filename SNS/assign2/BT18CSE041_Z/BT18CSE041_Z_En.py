import binascii
import random

R1_key = ""
R2_key = ""

def generate_key(length):
    global R1_key, R2_key

    temp1_key = []
    temp2_key = []

    for i in range(length):
        temp1_key += ["1"]
        temp2_key += ["1"]

    for i in range(length//2):
        index1 = random.randint(0, length-1)
        index1 = random.randint(0, length-1)

        temp1_key[index1] = str(abs(int(temp1_key[index1]) - 1))
        temp2_key[index1] = str(abs(int(temp2_key[index1]) - 1))

    R1_key = R1_key.join(temp1_key)
    R2_key = R2_key.join(temp2_key)

def xor(L_txt, R_txt):
    output = ""

    for i in range(len(L_txt)):
        if L_txt[i] == R_txt[i]:
            output += "0"
        else:
            output += "1"

    return output

def round_func(L_txt, R_txt):
    inter_val = ""

    roll_num = 41
    roll_num_bin = format(roll_num, '08b')

    j = 0

    for i in range(len(L_txt)):
        if L_txt[i] == roll_num_bin[j]:
            if L_txt[i] == "1":
                inter_val += "1"
            else:
                inter_val += "0"
        else:
            inter_val += "0"

        j += 1

        if j == 8:
            j = 0

    return xor(inter_val, R_txt)

def encrypt(plain_txt):
    if len(plain_txt) % 2 != 0:
        plain_txt += " "

    global R1_key, R2_key

    plain_txt_ascii = [ord(x) for x in plain_txt]
    plain_txt_bin = [format(y,'08b') for y in plain_txt_ascii]
    plain_txt_bin = "".join(plain_txt_bin)

    size = len(plain_txt_bin)
    mid_pt = size//2
    
    R1_left = plain_txt_bin[0:mid_pt]
    R1_right = plain_txt_bin[mid_pt::]

    generate_key(mid_pt)

    R1_rounded = round_func(R1_right,R1_key)
    R2_right = xor(R1_rounded,R1_left)
    R2_left = R1_right

    R2_rounded = round_func(R2_right,R2_key)
    R3_right = xor(R2_rounded,R2_left)
    R3_left = R2_right

    cipher_txt = R3_left + R3_right
    encrypted_txt = ""

    for i in range(0, size, 8):
        char_bin = cipher_txt[i:i + 8]
        char_ascii = int(char_bin,2)

        encrypted_txt += chr(char_ascii)

    result = {'ciphertext': encrypted_txt, 'R1_key': R1_key, 'R2_key': R2_key}

    return result