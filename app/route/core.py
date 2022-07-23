import http
from fastapi import APIRouter, Response
from model import core_model
from config import mongo
from utils import util
from utils import response
from logic import core
app = APIRouter()

@app.post('/registration_sjh')
def registration(model:core_model.Registration, resp:Response):
    """ Registration SJH by UMKM """
    try:
        if util.id_checker(model.creator_id):
            if not util.check_regitration(model.creator_id):
                ingest = core.Core()
                ingest.inset_register(model.creator_id)
                return response.response_detail(200, "Registration Insert Success", resp)
        else:
            return response.response_detail(400, "Already Registration", resp)
    except:
        return response.response_detail(400, "Registration Failed", resp)

@app.get('/umkm_registration_data')
def registration_data(umkm_id, resp:Response):
    """ UMKM data will be checking by BPJPH """
    try:
        if not util.check_regitration(umkm_id):
            client, coll = mongo.mongodb_config('Accounts')
            profile_umkm = coll.find_one(umkm_id)
            client.close()
            return response.response_detail(200, profile_umkm, resp)
        else:
            return response.response_detail(400, "UMKM not registered", resp)
    except:
        return response.response_detail(400, "Failed getting umkm data", resp)
        


@app.post('/BPJPH_checking_data')
def bpjph_checker(model:core_model.BPJPH_Check,resp:Response):
    """ BPJPH checking umkm data """
    try:
        client, coll = mongo.mongodb_config('Accounts')
        client_data, coll_data = mongo.mongodb_config('Core')
        if coll.find_one({'_id':model.BPJPH_id}):
            client.close()
            find_id = {'_id':model.umkm_id}
            update_status = { "$set": { "status_check_by_BPJPH": True } }
            coll_data.update_one(find_id,update_status)
            update_desc = {'desc_check_by_BPJPH':model.description}
            coll_data.update_one(find_id,update_desc)
            update_result = {'desc_result':model.result}
            coll_data.update_one(find_id,update_result)
            client_data.close()
            return response.response_detail(200, "Checking data success", resp)
        else:
            return response.response_detail(400, "BPJPH is not found", resp)
    except:
        return response.response_detail(400, "Checking data failed", resp)
        

@app.post('/LPH_appointment')
def LPH_Appointment():
    pass