from base64 import b64encode
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

key = get_random_bytes(8)
iv = get_random_bytes(8)

def DES_CBC_encrypt(plain_txt):
    global key, iv

    plain_txt = bytes(plain_txt, 'utf-8')
    encrypter = DES.new(key, DES.MODE_CBC, iv)
    cipher_txt = encrypter.encrypt(pad(plain_txt, DES.block_size))

    iv = b64encode(iv).decode('utf-8')
    key = b64encode(key).decode('utf-8')
    cipher_txt = b64encode(cipher_txt).decode('utf-8')

    result = {'iv':iv, 'ciphertext':cipher_txt, 'key': key}

    return result