import hashlib

def sha256(param):
    param = bytes(param, 'utf-8')
    data = hashlib.sha256()
    data.update(param)
    return data.hexdigest()

