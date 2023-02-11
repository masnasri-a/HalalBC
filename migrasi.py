from random import randint
import pymongo

from dotenv import dotenv_values

conf = dotenv_values('.env')
client = pymongo.MongoClient(conf.get('MONGO_URI'))
database = client["HalalBC"]
col = database['DocumentDetails']
col_product = database['Product']

def id_generator(param):
    """ id generator """
    return str(param + ":" + str(randint(111111111111, 999999999999)))

data = col.find()
for detail in data:
    if 'jawaban_audit' in detail:
        if detail['jawaban_audit'] is not None and detail['jawaban_audit'] is not False:
            print(detail['_id'])
            mapping = {
                "_id": id_generator('AI'),
                "doc_id": detail['_id'],
                "type_data": "audit",
                "data":detail['jawaban_audit']
            }
            col_product.insert_one(mapping)
        
            
        
