from base64 import b64encode, b64decode
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import json


def DES_CBC_encrypt(plain_txt, file_name):
    iv, key = -1, -1 
    with open(file_name + ".json", 'r') as f:
        data = json.load(f)
        iv = data['iv']
        key = data['key']

    iv = b64decode(iv)
    key = b64decode(key)

    plain_txt = bytes(plain_txt, 'utf-8')
    encrypter = DES.new(key, DES.MODE_CBC, iv)
    cipher_txt = encrypter.encrypt(pad(plain_txt, DES.block_size))

    cipher_txt = b64encode(cipher_txt).decode('utf-8')

    return cipher_txt
