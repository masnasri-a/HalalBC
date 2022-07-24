import http
import re
import traceback
from fastapi import APIRouter, Response
from model import core_model
from config import mongo
from utils import util
from utils import response
from logic import core
app = APIRouter()


@app.post('/registration_sjh')
def registration(model: core_model.Registration, resp: Response):
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
def registration_data(umkm_id, resp: Response):
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

@app.get('/get_umkm_regestered')
def umkm_registered(resp:Response):
    """ ambil data list umkm yang register """
    try:
        client, coll = mongo.mongodb_config('Core')
        data = coll.find({})
        list_result = []
        for detail in data:
            list_result.append(detail['_id'])
        return response.response_detail(200, list_result, resp)
    except:
        return response.response_detail(400, "Failed getting umkm data", resp)


@app.post('/BPJPH_checking_data')
def bpjph_checker(model: core_model.BPJPH_Check, resp: Response):
    """ BPJPH checking umkm data """
    try:
        client, coll = mongo.mongodb_config('Accounts')
        client_data, coll_data = mongo.mongodb_config('Core')
        if coll.find_one({'_id': model.BPJPH_id}):
            client.close()
            find_id = {'_id': model.umkm_id}
            update_status = {"$set": {"status_check_by_BPJPH": True}}
            coll_data.update_one(find_id, update_status)
            update_desc = {'desc_check_by_BPJPH': model.description}
            coll_data.update_one(find_id, update_desc)
            update_result = {'desc_result': model.result}
            coll_data.update_one(find_id, update_result)
            client_data.close()
            return response.response_detail(200, "Checking data success", resp)
        else:
            return response.response_detail(400, "BPJPH is not found", resp)
    except:
        return response.response_detail(400, "Checking data failed", resp)


@app.get('/get_LPH')
def get_lph(location: str, resp: Response):
    """ ambil data LPH dari address """
    try:
        client, coll = mongo.mongodb_config('Accounts')
        rgx = re.compile('.*'+location+'.*', re.IGNORECASE)
        query = {'$and': [{'type': 'LPH'}, {'address': rgx}]}
        data = coll.find(query)
        list_result = []
        for detail in data:
            del detail['password']
            list_result.append(detail)
        client.close()
        return response.response_detail(200, list_result, resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "get data LPH failed", resp)


@app.post('/LPH_appointment')
def LPH_Appointment(model: core_model.Appointment, resp:Response):
    """ Penunjukan LPH okeh BPJPH """
    try:
        client, coll = mongo.mongodb_config('Core')
        find_id = {'_id': model.umkm_id}
        updated = {'LPH_appointment': {
            "BPJPH_id": model.bpjphh_id,
            "LPH_id": model.lph_id
        }}
        coll.update_one(find_id, updated)
        client.close()
        return response.response_detail(200, "Appointment Success", resp)
    except:
        return response.response_detail(400, "LPH appointment Failed", resp)


@app.post('/LPH_Checking_data')
def checking_data(model:core_model.LPHCheckingData, resp:Response):
    """ LPH melakuakan review data dari BPJPH """
    try:
        client, coll = mongo.mongodb_config('Core')
        find_id = {'_id': model.umkm_id}
        updated = {'LPH_Checking_data_status': model.status}
        coll.update_one(find_id, updated)
        client_desc, coll_desc = mongo.mongodb_config('Core')
        update_value = {'LPH_Checking_data_desc':model.description}
        coll_desc.update_one(find_id, update_value)
        client_desc.close()
        client.close()
        return response.response_detail(200, "Checking Data Success", resp)
    except:
        return response.response_detail(400, "Checking Data Failed", resp)


@app.post('/review_bussiness_place')
def review_buss_place(model:core_model.ReviewBussinessPlace, resp:Response):
    """ LPH Melakukan Review Lapangan """
    try:
        client, coll = mongo.mongodb_config('Core')
        find_id = {'_id': model.umkm_id}
        update_status_LPH_check_field = {'status_LPH_check_field':True}
        coll.update_one(find_id, update_status_LPH_check_field)
        client.close()
        client_status, coll_status = mongo.mongodb_config('Core')
        update_status = {'LPH_review_status':model.status}
        coll_status.update_one(find_id, update_status)
        client_status.close()
        client_desc, coll_desc = mongo.mongodb_config('Core')
        update_desc = {'LPH_to_MUI':model.description}
        coll_desc.update_one(find_id, update_desc)
        client_desc.close()
        return response.response_detail(200, "Review Bussiness Place Success", resp)
    except:
        return response.response_detail(400, "Review Bussiness Place Failed", resp)

@app.get('/mui_get_data')
def mui_get_data(model:core_model.MUIGetData, resp:Response):
    """ Mui Ambil Data Untuk Direview """
    try:
        client, coll = mongo.mongodb_config('Core')
        data = coll.find_one({'_id':model.umkm_id})
        client.close()
        return response.response_detail(200, data, resp)
    except:
        return response.response_detail(400, "MUI get data failed", resp)

