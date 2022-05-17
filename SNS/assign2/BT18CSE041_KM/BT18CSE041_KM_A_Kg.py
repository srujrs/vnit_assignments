from Crypto.Random import get_random_bytes
from base64 import b64encode
import json


def generate_key(file_name):
    key = get_random_bytes(8)
    iv = get_random_bytes(8)

    iv = b64encode(iv).decode('utf-8')
    key = b64encode(key).decode('utf-8')

    result = {'iv': iv, 'key': key}

    with open(file_name + ".json", 'w')  as f:
        json.dump(result, f)

        f.close()