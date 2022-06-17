""" util file pages """

import hashlib
from datetime import datetime
from random import randint
from pymongo.errors import PyMongoError
from config.mongo import mongo
from fastapi.exceptions import HTTPException

def sha256(param):
    """ hasing function """
    param = bytes(param, 'utf-8')
    data = hashlib.sha256()
    data.update(param)
    return data.hexdigest()

def id_generator(param):
    """ id generator """
    return param+":"+str(randint(111111111111,999999999999))

def get_created_at():
    """ created_at generator """
    return int(datetime.timestamp(datetime.now())*1000)

def username_checker(username:str)->bool:
    """ username check into mongodb """
    try:
        client, col = mongo('Accounts')
        data = col.find_one({'username':username})
        client.close()
        if data is None:
            return True
        else:
            return False
    except PyMongoError as error:
        raise HTTPException(400, "Error Mongo") from error
