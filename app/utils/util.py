import hashlib
from fastapi.exceptions import HTTPException
from datetime import datetime
from random import randint
from config import mongo

def sha256(param):
    param = bytes(param, 'utf-8')
    data = hashlib.sha256()
    data.update(param)
    return data.hexdigest()

def id_generator(param):
    return param+":"+str(randint(111111111111,999999999999))

def get_created_at():
    return int(datetime.timestamp(datetime.now())*1000)

def username_checker(username:str)->bool:
    try:
        client, col = mongo.mongo('Accounts')
        data = col.find_one({'username':username})
        client.close
        if data == None:
            return True
        else:
            return False
    except:
        raise HTTPException(400, "Error Mongo")