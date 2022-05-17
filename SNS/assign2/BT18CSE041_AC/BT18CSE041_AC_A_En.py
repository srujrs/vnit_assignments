import random

import BT18CSE041_AC_A_Kg as Kg


RSA_modulus_length = 1024

keys = Kg.get_keys(RSA_modulus_length)

RSA_modulus = keys[0]
RSA_public_key = keys[1]
RSA_private_key = keys[2]


def xor(L_txt, R_txt):
    output = ""

    for i in range(len(L_txt)):
        if L_txt[i] == R_txt[i]:
            output += "0"
        else:
            output += "1"

    return output


def mgf1(input_str, length):
    output = ""
    if len(input_str) < length:
        while len(output) < length:
            output += input_str
        output = output[:length]
    else:
        output = input_str[:length]

    return output


def RSA_encrypt(plain_txt_num):
    return pow(plain_txt_num, RSA_public_key, RSA_modulus)


def RSA_decrypt(cipher_txt_num):
    return pow(cipher_txt_num, RSA_private_key, RSA_modulus)


def RSA_OAEP_encrypt(plain_txt):
    plain_txt_ascii = [ord(x) for x in plain_txt]
    plain_txt_bin = [format(y, '08b') for y in plain_txt_ascii]
    plain_txt_bin = "".join(plain_txt_bin)

    plain_txt_len = len(plain_txt_bin)

    k0_and_k1 = RSA_modulus_length - plain_txt_len

    k0 = random.randint(1, k0_and_k1 - 2)
    k1 = k0_and_k1 - k0

    r = random.getrandbits(k0)
    r_bin = format(r, '08b')

    plain_txt_padded = plain_txt_bin

    for i in range(k1):
        plain_txt_padded += "0"

    r_bin_hashed = mgf1(r_bin, RSA_modulus_length - k0)

    X = xor(plain_txt_padded, r_bin_hashed)

    Y = xor(r_bin, mgf1(X, k0))

    cipher_txt_num = RSA_encrypt(int(X + Y, 2))

    result = {
        'cipher': cipher_txt_num,
        'k0': k0,
        'k1': k1,
        'RSA modulus': RSA_modulus,
        'RSA private key': RSA_private_key
    }

    return result


def RSA_OAEP_decrypt(cipher_txt_num, k0, k1):
    cipher_txt = RSA_decrypt(cipher_txt_num)
    cipher_txt = format(cipher_txt, "08b")
    
    X = cipher_txt[:RSA_modulus_length - k0]
    Y = cipher_txt[RSA_modulus_length - k0:]

    r = xor(Y, mgf1(X, k0))

    decrypted_txt_bin = xor(X, mgf1(r, RSA_modulus_length - k0))
    decrypted_txt_bin = decrypted_txt_bin[:len(decrypted_txt_bin) - k1]

    decrypted_txt = ""
    
    for i in range(0, len(decrypted_txt_bin), 8):
        char_bin = decrypted_txt_bin[i:i + 8]
        char_ascii = int(char_bin,2)

        decrypted_txt += chr(char_ascii)

    return decrypted_txt
