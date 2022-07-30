""" util file pages """

import errno
import hashlib
from datetime import datetime, date
from random import randint
from pymongo.errors import PyMongoError
from config import mongo
from fastapi.exceptions import HTTPException


def sha256(param):
    """ hasing function """
    param = bytes(param, 'utf-8')
    data = hashlib.sha256()
    data.update(param)
    return data.hexdigest()


def id_generator(param):
    """ id generator """
    return str(param + ":" + str(randint(111111111111, 999999999999)))


def get_created_at():
    """ created_at generator """
    return int(datetime.timestamp(datetime.now()) * 1000)


def username_checker(username: str) -> bool:
    """ username check into mongodb """
    try:
        client, col = mongo.mongodb_config('Accounts')
        data = col.find_one({'username': username})
        client.close()
        if data is None:
            return True
        else:
            return False
    except PyMongoError as error:
        raise HTTPException(400, "Error Mongo") from error

def id_checker(_id: str) -> bool:
    """ username check into mongodb """
    try:
        client, col = mongo.mongodb_config('Accounts')
        data = col.find_one({'_id': _id})
        client.close()
        if data is not None:
            return True
        else:
            return False
    except PyMongoError as error:
        raise HTTPException(400, "Error Mongo") from error


def get_time_parse():
    today = date.today()
    return today.strftime("%d %B %Y")

def check_regitration(_id:str) -> bool:
    try:
        client, col = mongo.mongodb_config('Core')
        data = col.find_one({'_id': _id})
        client.close()
        if data != None and data['status_registration']:
            return True
        else:
            return False
        return False
    except Exception as error:
        raise HTTPException(400, "Failed") from error