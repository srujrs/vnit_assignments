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

def decrypt(encrypt_txt, R1_key, R2_key):
    encrypt_txt_ascii = [ord(x) for x in encrypt_txt]
    encrypt_txt_bin = [format(y,'08b') for y in encrypt_txt_ascii]
    encrypt_txt_bin = "".join(encrypt_txt_bin)

    size = len(encrypt_txt_bin)
    mid_pt = size//2

    R4_left = encrypt_txt_bin[0:mid_pt]
    R4_right = encrypt_txt_bin[mid_pt::]

    R3_rounded = round_func(R4_left,R2_key)
    R5_left = xor(R4_right, R3_rounded)
    R5_right = R4_left

    R4_rounded = round_func(R5_left,R1_key)
    R6_left = xor(R5_right, R4_rounded)
    R6_right = R5_left

    cipher_txt = R6_left + R6_right
    decrypted_txt = ""

    for i in range(0, size, 8):
        char_bin = cipher_txt[i:i + 8]
        char_ascii = int(char_bin,2)

        decrypted_txt += chr(char_ascii)

    return decrypted_txt