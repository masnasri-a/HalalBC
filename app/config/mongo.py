"""mongo config"""
import traceback
import pymongo
from dotenv import dotenv_values
from fastapi.exceptions import HTTPException

conf = dotenv_values('.env')
def mongo(column):
    """ mongo config"""
    try:
        client = pymongo.MongoClient(conf.get('MONGO_URI'))
        database = client["HalalBC"]
        col = database[column]
        return client, col
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(400, "Error Connect Mongo") from error
