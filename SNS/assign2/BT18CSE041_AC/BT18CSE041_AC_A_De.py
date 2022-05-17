RSA_modulus_length = 1024


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


def RSA_decrypt(cipher_txt_num, RSA_modulus, RSA_private_key):
    return pow(cipher_txt_num, RSA_private_key, RSA_modulus)


def RSA_OAEP_decrypt(cipher_txt_num, k0, k1, RSA_modulus, RSA_private_key):
    cipher_txt = RSA_decrypt(cipher_txt_num, RSA_modulus, RSA_private_key)
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