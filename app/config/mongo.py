import traceback
import pymongo
from dotenv import dotenv_values

conf = dotenv_values('.env')
def mongo(column):
    try:
        client = pymongo.MongoClient(conf.get('MONGO_URI'))
        db = client["HalalBC"]
        col = db[column]
        return client, col
    except:
        traceback.print_exc()