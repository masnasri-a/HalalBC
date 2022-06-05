import hashlib
from datetime import datetime
from random import randint


def sha256(param):
    param = bytes(param, 'utf-8')
    data = hashlib.sha256()
    data.update(param)
    return data.hexdigest()

def id_generator():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    return randint(1000,9193)*ts[3:-1]