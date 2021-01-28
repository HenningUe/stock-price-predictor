
import hashlib


def make_hash(val_in):
    result = hashlib.sha1(val_in.encode())
    result = result.hexdigest()[:10]
    return int(result, 16)
