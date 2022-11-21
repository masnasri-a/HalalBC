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


# @app.post('/simulasi_sjh')
# async def simulasi_sjh(creator_id, resp: Response, registered: Optional[bool] = False):
#     """apabila SJH masih belum cukup syarat Sertitikat halal"""
#     try:
#         valid_id = util.id_checker(creator_id)
#         if not valid_id:
#             return response.response_detail(400, "id not valid", resp)
#         detail = simulasi.Simulasi(creator_id, registered)
#         model, status = detail.logic()  # type: ignore
#         models = {
#             "message": model['message'],
#             "data": None,
#             "created_at": util.get_created_at(),
#             "creator_id": creator_id
#         }
#         client, col = mongo.mongodb_config('DetailSimulasi')
#         check_simulasi = col.find_one({'_id': creator_id})
#         if check_simulasi is None:
#             simulasi_model = {
#                 '_id': creator_id,
#                 'list_simulasi': [
#                     models
#                 ]
#             }
#             insert = col.insert_one(simulasi_model)
#         else:
#             list_simulasi = check_simulasi['list_simulasi']
#             list_simulasi.append(models)
#             find_id = {'_id': creator_id}
#             set_data = {'$set': {'list_simulasi': list_simulasi}}
#             col.update_one(find_id, set_data)
#         if status:
#             return response.response_detail(200, models, resp)
#         else:
#             return response.response_detail(400, models, resp)
#     except Exception:
#         traceback.print_exc()
#         return response.response_detail(400, "Error create simulation", resp)


# @app.post('/input_bahan')
# async def input_bahan(model: umkm_model.InputBahan, resp: Response):
#     """ input bahan baru """
#     try:
#         valid_id = util.id_checker(model.creator_id)
#         if not valid_id:
#             return response.response_detail(400, "id not valid", resp)
#         client, col = mongo.mongodb_config('BahanDetail')

#         list_bahan = []
#         number_id = 1
#         for detail in model.detail_bahan:
#             model_detail = detail.dict()
#             model_detail['id'] = number_id
#             list_bahan.append(model_detail)
#             number_id += 1
#         result_model = {
#             "_id": util.id_generator('BHN'),
#             "creator_id": model.creator_id,
#             "created_at": util.get_created_at(),
#             "list_bahan": list_bahan
#         }
#         col.insert_one(result_model)
#         client.close()
#         return response.response_detail(200, "insert bahan success", resp)
#     except Exception as error:
#         traceback.print_exc()
#         return response.response_detail(400, "input bahan failed", resp)


@app.post('/simulasi')
def get_bahan(creator_id: str, resp: Response):
    try:
        valid_id = util.id_checker(creator_id)
        if not valid_id:
            return response.response_detail(400, "id not valid", resp)
        client, col = mongo.mongodb_config('DocumentDetails')
        client_sim, col_sim = mongo.mongodb_config('BahanSimulasi')
        data = col.find_one({'creator': creator_id})
        pembelian = data['pembelian']
        result = []
        for detail in pembelian:
            if detail['halal'] == 'True':
                if 'no_sertifikat' in detail:
                    if detail['no_sertifikat'] == '':
                        result.append({
                            'name': detail['nama_dan_merk'],
                            'type': 'pembelian',
                            'status': 'Certificate Not Found'
                        })
                else:
                    result.append({
                        'name': detail['nama_dan_merk'],
                        'type': 'pembelian',
                        'status': 'Certificate Not Found'
                    })
        pembelian_import = data['pembelian_import']
        for detail in pembelian_import:
            if detail['halal'] == 'True':
                if 'no_sertifikat' in detail:
                    if detail['no_sertifikat'] == '':
                        result.append({
                            'name': detail['nama_dan_merk'],
                            'type': 'pembelian import',
                            'status': 'Certificate Not Found'
                        })
                else:
                    result.append({
                        'name': detail['nama_dan_merk'],
                        'type': 'pembelian import',
                        'status': 'Certificate Not Found'
                    })
        client.close()
        find_simulasi = col_sim.find_one({'_id': creator_id})
        if find_simulasi is None:
            model = {
                '_id': creator_id,
                'status': 'success' if len(result) == 0 else 'failed',
                'log': [
                    {
                        'created_at': util.get_created_at(),
                        'data': result,
                        'status': 'success' if len(result) == 0 else 'failed'
                    }
                ]
            }
            col_sim.insert_one(model)
        else:
            log: list = find_simulasi['log']
            log.append(
                {
                    'created_at': util.get_created_at(),
                    'data': result,
                    'status': 'success' if len(result) == 0 else 'failed'
                })
            myquery = {'_id': creator_id}
            newvalues = {"$set": {"log": log}}
            col_sim.update_one(myquery, newvalues)
            value = {"$set": {"status": 'success' if len(
                result) == 0 else 'failed'}}
            col_sim.update_one(myquery, value)
        return response.response_detail(200, result, resp)
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, "Failed get data bahan", resp)


@app.get('/get_simulasi')
def add_update_bahan(creator_id: str,resp: Response):
    try:
        client, col = mongo.mongodb_config('BahanSimulasi')
        query = {'_id': creator_id}
        data = col.find_one(query)
        client.close()
        return response.response_detail(200, data, resp)
    except Exception as error:
        return response.response_detail(400, "failed data get", resp)
