import http
from http import client
import json
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
                core.inset_register(model.creator_id,"")
                return response.response_detail(200, "Registration Insert Success", resp)
            else:
                core.inset_register(model.creator_id,model.prev_id)
                return response.response_detail(200, "Renew Registration Insert Success", resp)
        else:
            traceback.print_exc()
            return response.response_detail(400, "Already Registration", resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "Registration Failed", resp)


@app.get('/umkm_registration_data')
def registration_data(umkm_id, resp: Response):
    """ UMKM data will be checking by BPJPH """
    try:
        if not util.check_regitration(umkm_id):
            client, coll = mongo.mongodb_config('Accounts')
            profile_umkm = coll.find_one({'_id':umkm_id})
            client.close()
            return response.response_detail(200, profile_umkm, resp)
        else:
            return response.response_detail(400, "UMKM not registered", resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "Failed getting umkm data", resp)

@app.get('/get_umkm_registered')
def umkm_registered(resp:Response):
    """ ambil data list umkm yang register """
    try:
        client, coll = mongo.mongodb_config('Core')
        client_acc, coll_acc = mongo.mongodb_config('Accounts')
        data = coll.find({})
        list_result = []
        for detail in data:
            name = coll_acc.find_one({'_id':detail['umkm_id']})
            list_result.append({
                "id":detail['_id'],
                "umkm_id":detail['umkm_id'],
                "username":name['username'],
                "status_registration":detail['registration']['status'],
                "lph_id":detail['lph_appointment']['lph_id'],
                "status_check_by_BPJPH":detail['bpjph_checked']['status'],
                "status_LPH_check_field":detail['lph_checked']['status'],
                "status_checked_MUI":detail['mui']['checked_status'],
                "Certificate_status":detail['certificate']['status']
            })
        client.close()
        return response.response_detail(200, list_result, resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "Failed getting umkm data", resp)


@app.post('/BPJPH_checking_data')
def bpjph_checker(model: core_model.BPJPH_Check, resp: Response):
    """ BPJPH checking umkm data """
    try:
        client, coll = mongo.mongodb_config('Accounts')
        client_data, coll_data = mongo.mongodb_config('Core')
        if coll.find_one({'_id': model.BPJPH_id}):
            client.close()
            find_id = {'umkm_id': model.umkm_id}
            update_status = {"$set": {"bpjph_checked.checked": True}}
            coll_data.update_one(find_id, update_status)
            update_desc = {"$set": {'bpjph_checked.desc': model.description}}
            coll_data.update_one(find_id, update_desc)
            update_result = {"$set": {'bpjph_checked.result': model.result}}
            coll_data.update_one(find_id, update_result)
            update_date = {"$set": {'bpjph_checked.date': util.get_created_at()}}
            coll_data.update_one(find_id, update_date)
            client_data.close()
            return response.response_detail(200, "Checking data success", resp)
        else:
            traceback.print_exc()
            return response.response_detail(400, "BPJPH is not found", resp)
    except:
        traceback.print_exc()
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
        find_id = {'umkm_id': model.umkm_id}
        updated = {"$set": {'lph_appointment': {
            "bpjph_id": model.bpjphh_id,
            "lph_id": model.lph_id,
            "date":util.get_created_at()
        }}}
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
        find_id = {'umkm_id': model.umkm_id}
        updated = {'lph_checked.status': model.status}
        coll.update_one(find_id, updated)
        client_desc, coll_desc = mongo.mongodb_config('Core')
        update_value = {"$set": {'lph_checked.desc':model.description}}
        coll_desc.update_one(find_id, update_value)
        client_date, coll_date = mongo.mongodb_config('Core')
        update_date = {"$set": {'lph_checked.date':util.get_created_at()}}
        coll_date.update_one(find_id, update_date)
        client_date.close()
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
        find_id = {'umkm_id': model.umkm_id}
        update_status_LPH_check_field = {"$set": {'lph_checked.survey_location':True}}
        coll.update_one(find_id, update_status_LPH_check_field)
        client.close()
        client_status, coll_status = mongo.mongodb_config('Core')
        update_status = {"$set": {'lph_checked.review_status':model.status}}
        coll_status.update_one(find_id, update_status)
        client_status.close()
        client_desc, coll_desc = mongo.mongodb_config('Core')
        update_desc = {"$set": {'lph_checked.to_mui':model.description}}
        coll_desc.update_one(find_id, update_desc)
        client_desc.close()
        return response.response_detail(200, "Review Bussiness Place Success", resp)
    except:
        return response.response_detail(400, "Review Bussiness Place Failed", resp)

@app.get('/mui_get_data')
def mui_get_data(umkm_id, resp:Response):
    """ Mui Ambil Data Untuk Direview """
    try:
        client, coll = mongo.mongodb_config('Core')
        data = coll.find_one({'umkm_id':umkm_id})
        client.close()
        return response.response_detail(200, data, resp)
    except:
        return response.response_detail(400, "MUI get data failed", resp)

@app.post('/mui_checking_data')
def mui_checking_data(model:core_model.MUICheckingData, resp:Response):
    """ MUI melakukan cek data registrasi """
    try:
        client, col = mongo.mongodb_config('Core')
        find_id = {'umkm_id':model.umkm_id}
        new_value = {"$set": {'mui.checked_status':True}}
        col.update_one(find_id, new_value)
        MUI_decicion_result = {"$set": {'mui.decision_desc':model.description}}
        col.update_one(find_id, MUI_decicion_result)
        MUI_status = {"$set": {'mui.approved':model.status}}
        col.update_one(find_id, MUI_status)
        MUI_date = {"$set": {'mui.date':util.get_created_at()}}
        col.update_one(find_id, MUI_date)
        client.close()
        return response.response_detail(200, "MUI Checking data Success", resp)
    except:
        return response.response_detail(400, "MUI checking data failed", resp)

# @app.post()

@app.post('/bpjph_insert_certificate_data')
def bpjph_insert_certificate_data(model : core_model.UploadCertificate, resp:Response):
    """ BPJPH Upload data certificate """
    try:
        client, col = mongo.mongodb_config('Core')
        find_id = {'umkm_id':model.umkm_id}
        new_value = {"$set": {'certificate.status':True}}
        col.update_one(find_id, new_value)
        data = {"$set": {'certificate.data':model.cert_id}}
        col.update_one(find_id, data)
        create = {"$set": {'certificate.created_date':util.get_created_at()}}
        col.update_one(find_id, create)
        expire = {"$set": {'certificate.expired_date':model.expire}}
        col.update_one(find_id, expire)
        client.close()
        return response.response_detail(200, "Insert Certificate data Success", resp)
    except:
        return response.response_detail(400, "Insert Certificate data failed", resp)


@app.get('/qr_detail')
def qr_detail(umkm_id, resp:Response):
    """ 
        AMBIL DETAIL DARI QR
    """
    try:
        client, col = mongo.mongodb_config('Core')
        client_acc, col_acc = mongo.mongodb_config('Accounts')
        profile_account = col_acc.find_one({'_id':umkm_id})
        result = {}
        if profile_account is not None:
            del profile_account['password']
            result['profile'] = profile_account
        core_data = col.find_one({'umkm_id':umkm_id})
        if core_data is not None:
            result['core'] = core_data
        client.close()
        client_acc.close()
        return response.response_detail(200, result, resp)
    except:
        return response.response_detail(400, "detail qr failed", resp)