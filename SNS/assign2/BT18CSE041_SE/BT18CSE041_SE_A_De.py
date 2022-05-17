from base64 import b64decode
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad


def DES_CBC_decrypt(cipher_txt, key, iv):
    iv = b64decode(iv)
    cipher_txt = b64decode(cipher_txt)
    key = b64decode(key)

    decrypter = DES.new(key, DES.MODE_CBC, iv)
    plain_txt = unpad(decrypter.decrypt(cipher_txt), DES.block_size)

    return plain_txt