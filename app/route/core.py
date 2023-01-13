import http
from http import client
import json
import re, io
import traceback
from typing import Optional
from fastapi import APIRouter, Response
from model import core_model
from config import mongo
from utils import util
from utils import response
from logic import core, certificate
from client import blockchain
from starlette.responses import FileResponse
from fastapi import Response, BackgroundTasks

app = APIRouter()

@app.get('/check_registration_sjh')
def check_regis(umkm_id:str, resp:Response):
    try:
        status =  util.check_regitration(umkm_id)
        if status:
            return response.response_detail(200, {"registered":status, "detail":"Account has been registered"}, resp)
        else:
            return response.response_detail(404, {"registered":status, "detail":"Account not registered"}, resp)
    except:
        traceback.print_exc()
        return response.response_detail(500, "Database has down", resp)

@app.post('/registration_sjh')
def registration(model: core_model.Registration, resp: Response):
    """ Registration SJH by UMKM """
    try:
        client_simulasi, col_simulasi = mongo.mongodb_config("BahanSimulasi")
        if util.id_checker(model.creator_id): 
            client, coll = mongo.mongodb_config('Core')
            if col_simulasi.find_one({"_id":model.creator_id}):
                
                if not util.check_regitration(model.creator_id):
                    core.inset_register(model.creator_id,"")
                    find_id = {'umkm_id': model.creator_id}
                    update_status = {"$set": {"registration.status": True}}
                    coll.update_one(find_id, update_status)
                    update_date = {"$set": {"registration.date": util.get_created_at()}}
                    coll.update_one(find_id, update_date)
                    blockchain.add_transaction("TX",model.creator_id,bytes("register SJH",'utf-8'))
                    return response.response_detail(200, "Registration Insert Success", resp)
                elif not util.check_regitration(model.creator_id) and model.prev_id != "":
                    core.inset_register(model.creator_id,model.prev_id)
                    find_id = {'umkm_id': model.creator_id}
                    update_status = {"$set": {"registration.status": True}}
                    coll.update_one(find_id, update_status)
                    update_date = {"$set": {"registration.date": util.get_created_at()}}
                    coll.update_one(find_id, update_date)
                    blockchain.add_transaction("TX",model.creator_id,bytes("register SJH",'utf-8'))
                    return response.response_detail(200, "Renew Registration Insert Success", resp)
                else:
                    datas = coll.find_one({"umkm_id":model.creator_id})
                    dates = datas['registration']['date']
                    if dates >= dates + (31536000000 * 3):
                        core.inset_register(model.creator_id,datas['_id'])
                        find_id = {'umkm_id': model.creator_id}
                        update_status = {"$set": {"registration.status": True}}
                        coll.update_one(find_id, update_status)
                        update_date = {"$set": {"registration.date": util.get_created_at()}}
                        coll.update_one(find_id, update_date)
                        blockchain.add_transaction("TX",model.creator_id,bytes("register SJH",'utf-8'))
                        return response.response_detail(200, "Renew Registration Insert Success", resp)
                    else:
                        return response.response_detail(400, "Account already registered", resp)
            else:
                traceback.print_exc()
                return response.response_detail(401, "Please Simulasi first before registration", resp)
        else:
            traceback.print_exc()
            return response.response_detail(404, "Please check your creator id", resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "Registration Failed", resp)


@app.get('/tracing')
def tracing(umkm_id, resp: Response):
    """ UMKM data will be Tracing """
    try:
        client, coll = mongo.mongodb_config('Core')
        data = coll.find_one({'umkm_id':umkm_id})
        client.close()
        return response.response_detail(200, data, resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "Tracing Failed", resp)


@app.get('/umkm_registration_data')
def registration_data(umkm_id, resp: Response):
    """ UMKM data will be checking by BPJPH """
    try:
        if util.check_regitration(umkm_id):
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
def umkm_registered(resp:Response, lph_id:Optional[str] = 'all'):
    """ ambil data list umkm yang register """
    try:
        client, coll = mongo.mongodb_config('Core')
        client_acc, coll_acc = mongo.mongodb_config('Accounts')
        check_lph = coll_acc.find_one({'$and':[{'_id':lph_id},{'type':'lph'}]})
        list_id = []
        query = {}
        if check_lph:
            datas = coll.find({'lph_appointment.lph_id':lph_id})
            for detail in datas:
                list_id.append(detail['umkm_id'])
            if lph_id != 'all':
                query = {'umkm_id':{'$in':list_id}}
            else:
                query = {}
        print(query)
        data = coll.find(query)
        list_result = []
        for detail in data:
            name = coll_acc.find_one({'_id':detail['umkm_id']})
            list_result.append({
                "id":detail['_id'],
                "umkm_id":detail['umkm_id'],
                "username":name['username'] if 'username' in name else 'No Name',
                "status_registration":detail['registration']['status'],
                "lph_id":detail['lph_appointment']['lph_id'],
                "status_check_by_lph":True if detail['lph_checked']['status'] != "" else False,
                "status_check_by_BPJPH":detail['bpjph_checked']['status'],
                "status_LPH_check_field":detail['lph_checked']['review_status'],
                "status_checked_MUI":detail['mui']['checked_status'],
                "fatwa_status":detail['fatwa']['status'] if 'fatwa' in detail else None,
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
            update_status = {"$set": {"bpjph_checked.status": True}}
            coll_data.update_one(find_id, update_status)
            update_checked = {"$set": {"bpjph_checked.checked": True}}
            coll_data.update_one(find_id, update_checked)
            update_desc = {"$set": {'bpjph_checked.desc': model.description}}
            coll_data.update_one(find_id, update_desc)
            update_result = {"$set": {'bpjph_checked.result': model.result}}
            coll_data.update_one(find_id, update_result)
            update_date = {"$set": {'bpjph_checked.date': util.get_created_at()}}
            coll_data.update_one(find_id, update_date)
            client_data.close()
            blockchain.add_transaction(model.BPJPH_id,model.BPJPH_id,bytes('BPJPH checking data','utf-8'))
            return response.response_detail(200, "Checking data success", resp)
        else:
            traceback.print_exc()
            return response.response_detail(400, "BPJPH is not found", resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "Checking data failed", resp)


@app.get('/get_LPH')
def get_lph(resp: Response,location: Optional[str] = ""):
    """ ambil data LPH dari address """
    try:
        client, coll = mongo.mongodb_config('Accounts')
        # if location != "":
        #     rgx = re.compile('.*'+location+'.*', re.IGNORECASE)
        #     query = {'$and': [{'$or':[{'type': 'LPH'},{'type':'lph'}]}, {'address': rgx}]}
        # else:
        query = {'$or':[{'type': 'LPH'},{'type':'lph'}]}
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
        blockchain.add_transaction(model.bpjphh_id,model.bpjphh_id,bytes('appintment lph','utf-8'))
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
        updated = {"$set": {'lph_checked.status': model.status}}
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
        blockchain.add_transaction(model.umkm_id,model.umkm_id,bytes('lph checking data','utf-8'))
        return response.response_detail(200, "Checking Data Success", resp)
    except:
        traceback.print_exc()
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
        blockchain.add_transaction(model.umkm_id,model.umkm_id,bytes('review place','utf-8'))
        return response.response_detail(200, "Review Bussiness Place Success", resp)
    except:
        traceback.print_exc()
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
        blockchain.add_transaction(model.umkm_id,model.umkm_id,bytes('checking data','utf-8'))
        return response.response_detail(200, "MUI Checking data Success", resp)
    except:
        return response.response_detail(400, "MUI checking data failed", resp)

# @app.post()

@app.post('/generate_certificate')
def generate_cert(umkm_id, resp:Response):
    try:
        client_acc, col_acc = mongo.mongodb_config('Accounts')
        account = col_acc.find_one({"_id":umkm_id})
        client, col = mongo.mongodb_config('DocumentDetails')
        product = col.find_one({"creator":umkm_id})
        data = {}
        data['_id'] = umkm_id
        if account:
            lens = len(account['company_address'])
            address = account['company_address']
            if  lens< 60:
                address += 2*"\n"
            elif lens <120:
                address += "\n"
            address += "."
            data['_id'] = umkm_id
            data['name'] = account['company_name']
            data['product_type'] = account['product_type']
            data['product_name'] = account['product_name']
            data['address'] = address
        if product:
            prd:dict = product
            matrix = prd.get('matriks_produk')
            resps = []
            for detail in matrix:
                resps.append(detail['nama_bahan'])
            data['matrix'] = resps
        file_name = certificate.generate(data)
        print(file_name)
        return FileResponse(file_name, media_type='application/octet-stream',filename="certificate.pdf")

    except:
        traceback.print_exc()
        return response.response_detail(400, "Failed Generate Certificate", resp)

@app.get('/load_certificate')
def load_cert(umkm_id:str, resp:Response):
    try:
        resps = FileResponse(f"app/assets/certificate-{umkm_id}.pdf", media_type='application/octet-stream',filename="certificate.pdf")
        if resps:
            return resps
        else:
            response.response_detail(400, "Certificate no available", resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "Certificate no available", resp)
        
        
@app.post('/bpjph_insert_certificate_data')
def bpjph_insert_cetificate_data(model : core_model.UploadCertificate, resp:Response):
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


@app.post('/mui_insert_fatwa_data')
def bpjph_insert_fatwa_data(model : core_model.UploadCertificate, resp:Response):
    """ BPJPH Upload data fatwa """
    try:
        client, col = mongo.mongodb_config('Core')
        find_id = {'umkm_id':model.umkm_id}
        new_value = {"$set": {'fatwa.status':True}}
        col.update_one(find_id, new_value)
        data = {"$set": {'fatwa.data':model.cert_id}}
        col.update_one(find_id, data)
        create = {"$set": {'fatwa.created_date':util.get_created_at()}}
        col.update_one(find_id, create)
        expire = {"$set": {'fatwa.expired_date':model.expire}}
        col.update_one(find_id, expire)
        client.close()
        return response.response_detail(200, "Insert Fatwa data Success", resp)
    except:
        return response.response_detail(400, "Insert Fatwa data failed", resp)


@app.get('/qr_detail')
def qr_detail(umkm_id, resp:Response):
    """ 
        AMBIL DETAIL DARI QR
    """
    try:
        client, col = mongo.mongodb_config('Core')
        client_acc, col_acc = mongo.mongodb_config('Accounts')
        client_bahan, col_bahan = mongo.mongodb_config('DocumentDetails')
        profile_account = col_acc.find_one({'_id':umkm_id})
        result = {}
        if profile_account is not None:
            del profile_account['password']
            result['profile'] = profile_account
        core_data = col.find_one({'umkm_id':umkm_id})
        if core_data is not None:
            result['core'] = core_data
        data_bahan = col_bahan.find_one({'creator':umkm_id})
        if data_bahan is not None:
            result['pembelian'] = data_bahan['pembelian']
            result['pembelian_import'] = data_bahan['pembelian_import']
            result['stok_barang'] = data_bahan['stok_barang']
        client.close()
        client_acc.close()
        return response.response_detail(200, result, resp)
    except:
        return response.response_detail(400, "detail qr failed", resp)


@app.post('/review')
def review(model: core_model.ReviewUMKM, resp:Response):
    """
        CONSUMEN POST A REVIEW ABOUT PRODUCT
    """
    try:
        client, col = mongo.mongodb_config('Review')
        data = {}
        data['_id'] = util.id_generator("REVIEW")
        data.update(model.dict())
        data['created_at'] = util.get_created_at()
        tex = blockchain.add_transaction(data['_id'],data['_id'],bytes(json.dumps(data),'utf-8'))
        data['transaction_id'] = tex
        col.insert_one(data)
        client.close()
        return response.response_detail(200, data, resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "failed post review", resp)



@app.get('/review_by_umkm')
def review_by_umkm(umkm_id, resp:Response):
    """
        GET REVIEW DATA BY UMKM_ID
    """
    try:
        client, col = mongo.mongodb_config('Review')
        data = col.find({'umkm_id._id':umkm_id})
        if data:
            res = []
            for detail in data:
                res.append(detail)
            client.close()
            
            return response.response_detail(200, res, resp)
        else:
            traceback.print_exc()
            return response.response_detail(400, "get review failed", resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "get review failed", resp)

@app.post('/pelaporan')
def pelaporan(model:core_model.Pelaporan, resp:Response):
    try:
        client, col = mongo.mongodb_config('Pelaporan')
        data = {
            '_id':util.id_generator("PELAPORAN"),
            **model.dict()
        }
        col.insert_one(data)
        client.close()
        return response.response_detail(200, "Insert Pelaporan Success", resp)

    except:
        traceback.print_exc()
        return response.response_detail(400, "Pelaporan Failed", resp)

@app.get('/pelaporan')
def g_pelaporan(resp:Response, username:Optional[str]='all'):
    try:
        client, col = mongo.mongodb_config('Pelaporan')
        data = col.find()
        res = list(data)
        client.close()
        return response.response_detail(200, res, resp)
    except:
        traceback.print_exc()
        return response.response_detail(400, "Get Pelaporan Failed", resp)