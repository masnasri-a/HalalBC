""" Account Services """

import traceback
from typing import Optional
from fastapi import APIRouter, Response
from fastapi.exceptions import HTTPException
from pydantic import Field
from pymongo import errors
from config import mongo
from utils import util, response
from model import simulasi_model, umkm_model
from logic import simulasi

app = APIRouter()

@app.post('/simulasi')
def get_bahan(creator_id: str, resp: Response):
    try:
        valid_id = util.id_checker(creator_id)
        if not valid_id:
            return response.response_detail(400, "id not valid", resp)
        client, col = mongo.mongodb_config('DocumentDetails')
        # client_sim, col_sim = mongo.mongodb_config('BahanSimulasi')
        client_sim, col_sim = mongo.mongodb_config('LogSimulasi')
        # Cek Akun sudah melakukan pengisian dokumen apa belum?
        document_account = col.find_one({"creator":creator_id})
        if not document_account:        
            return response.response_detail(404, "UMKM Belum melakukan Pengisian data", resp)
        # Cek kalau ada yang belum terisi
        keys_with_none = [key for key, value in document_account.items() if value is None]
        if keys_with_none:
            return response.response_detail(404, "UMKM Belum melakukan keseluruhan Pengisian data", resp)
        
        # Cek akun apakah pernah registrasi apa belum
        
        data = col.find_one({'creator': creator_id})
        pembelian = data['pembelian']
        result = []
        count_status = 0
        total = 0
        not_halal = []
        for detail in pembelian:
            if detail['halal'] == 'True' or detail['halal'] == 'Halal':
                if 'no_sertifikat' in detail:
                    if detail['no_sertifikat'] == '':
                        result.append({
                            'name': detail['nama_dan_merk'],
                            'type': 'pembelian',
                            'detail': 'Halal but Certificate Not Found',
                            'status':True
                        })
                        count_status += 1
                        total += 1
                    else:
                        result.append({
                            'name': detail['nama_dan_merk'],
                            'type': 'pembelian',
                            'detail': 'Halal and Certificate Found',
                            'status':True
                        })
                        count_status += 1
                        total += 1
                else:
                    result.append({
                        'name': detail['nama_dan_merk'],
                        'type': 'pembelian',
                        'detail': 'Halal but Certificate Not Found',
                        'status':True
                    })
                    count_status += 1
                    total += 1
            else:
                result.append({
                        'name': detail['nama_dan_merk'],
                        'type': 'pembelian',
                        'detail': 'Certificate Not Found',
                        'status':False
                    })
                count_status -= 1
                total += 1
                not_halal.append({
                    "product_name":detail['nama_dan_merk'],
                    "type":"pembelian"
                })
        pembelian_import = data['pembelian_import']
        for detail in pembelian_import:
            if detail['halal'] == 'True' or detail['halal'] == 'Halal':
                if 'no_sertifikat' in detail:
                    if detail['no_sertifikat'] == '':
                        result.append({
                        'name': detail['nama_dan_merk'],
                        'type': 'pembelian_import',
                        'detail': 'Halal but Certificate Not Found',
                        'status':True
                    })
                        count_status += 1
                        total += 1


                    else:
                        result.append({
                        'name': detail['nama_dan_merk'],
                        'type': 'pembelian_import',
                        'detail': 'Halal and Certificate Found',
                        'status':True
                    })
                        count_status += 1
                        total += 1


                else:
                    result.append({
                        'name': detail['nama_dan_merk'],
                        'type': 'pembelian_import',
                        'detail': 'Halal but Certificate Not Found',
                        'status':True
                    })
                    count_status += 1
                    total += 1
            else:
                result.append({
                        'name': detail['nama_dan_merk'],
                        'type': 'pembelian_import',
                        'detail': 'Certificate Not Found',
                        'status':False
                    })
                count_status -= 1
                total += 1
                not_halal.append({
                    "product_name":detail['nama_dan_merk'],
                    "type":"pembelian_import"
                })
        client.close()
        
        find_simulasi = col_sim.find_one({'_id': creator_id})
        if find_simulasi is None:
            model = {
                '_id': creator_id,
                'status': 'success' if count_status != total else 'failed',
                'log': [
                    {
                        'created_at': util.get_created_at(),
                        'data': result,
                        'status': 'success' if count_status != total else 'failed'
                    }
                ]
            }
            col_sim.insert_one(model)
            return response.response_detail(200, result, resp)
        else:
            log: list = find_simulasi['log']
            log.append(
                {
                    'created_at': util.get_created_at(),
                    'data': result,
                    'status': 'success' if count_status == total else 'failed'
                })
            myquery = {'_id': creator_id}
            newvalues = {"$set": {"log": log}}
            col_sim.update_one(myquery, newvalues)
            value = {"$set": {"status": 'success' if count_status == total else 'failed'}}
            print(count_status)
            print(total)
            col_sim.update_one(myquery, value)
        return response.response_detail(200, result, resp)
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, "Failed get data bahan", resp)

@app.get('/saran_simulasi')
def saran(creator_id: str,resp: Response):
    try:
        client, col = mongo.mongodb_config('BahanSimulasi')
        data = col.find_one({'_id': creator_id})
        if data:
            if data['status'] == "success":
                return response.response_detail(200, "Please a register SJH", resp)
            else:
                return response.response_detail(200, "Please fix your data and make sure all materials are halal", resp)
        else:
            return response.response_detail(404, "Please Simulation your data first", resp)
    except:
        return response.response_detail(502, "Bad Gateway", resp)

@app.get('/get_simulasi')
def add_update_bahan(creator_id: str,resp: Response):
    try:
        client, col = mongo.mongodb_config('BahanSimulasi')
        query = {'_id': creator_id}
        data = col.find_one(query)
        if data:
            return response.response_detail(200, data, resp)
        else:
            return response.response_detail(404, "Please Simulation your data first", resp)
    except Exception as error:
        traceback.print_exc
        return response.response_detail(500, "Failed Connect Database", resp)
