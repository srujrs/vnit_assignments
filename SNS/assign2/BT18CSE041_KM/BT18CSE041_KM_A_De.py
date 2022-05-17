from base64 import b64decode
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import json


def DES_CBC_decrypt(cipher_txt, file_name):

    iv, key = -1, -1 
    with open(file_name + ".json", 'r') as f:
        data = json.load(f)
        iv = data['iv']
        key = data['key']

    iv = b64decode(iv)
    cipher_txt = b64decode(cipher_txt)
    key = b64decode(key)

    decrypter = DES.new(key, DES.MODE_CBC, iv)
    plain_txt = unpad(decrypter.decrypt(cipher_txt), DES.block_size)

    return plain_txt