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


@app.post('/simulasi_sjh')
async def simulasi_sjh(creator_id, resp: Response,registered: Optional[bool] = False):
    """apabila SJH masih belum cukup syarat Sertitikat halal"""
    try:
        valid_id = util.id_checker(creator_id)
        if valid_id:
            return response.response_detail(400, "id not valid", resp)
        detail = simulasi.Simulasi(creator_id, registered)
        model, status = detail.logic()
        models = {
            "message":model['message'],
            "data":None,
            "created_at":util.get_created_at(),
            "creator_id":creator_id
        }
        if status:
            return response.response_detail(200, models,resp)
        else:
            return response.response_detail(400, models,resp)
    except Exception:
        traceback.print_exc()
        return response.response_detail(400, "Error create simulation", resp)

@app.post('/input_bahan')
async def input_bahan(model: umkm_model.InputBahan, resp: Response):
    """ input bahan baru """
    try:
        valid_id = util.id_checker(model.creator_id)
        if valid_id:
            return response.response_detail(400, "id not valid", resp)
        client, col = mongo.mongodb_config('BahanDetail')
        list_bahan = []
        number_id = 1
        for detail in model.detail_bahan:
            model_detail = detail.dict()
            model_detail['id'] = number_id
            list_bahan.append(model_detail)
            number_id += 1
        result_model = {
            "_id": util.id_generator('BHN'),
            "creator_id": model.creator_id,
            "list_bahan": list_bahan
        }
        col.insert_one(result_model)
        client.close()
        return response.response_detail(200, "insert bahan success", resp)
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, "input bahan failed", resp)


@app.get('/get_bahan')
def get_bahan(creator_id: str, resp: Response):
    try:
        valid_id = util.id_checker(creator_id)
        if valid_id:
            return response.response_detail(400, "id not valid", resp)
        client, col = mongo.mongodb_config('BahanDetail')
        data = col.find_one({'creator_id':creator_id})
        client.close()
        return response.response_detail(200, data['list_bahan'], resp)

    except Exception as error:
        return response.response_detail(400, "Failed get data bahan", resp)

@app.post('/update_bahan')
def add_update_bahan(model: umkm_model.UpdateBahan, resp: Response):
    try:
        list_bahan = []
        for detail in model.detail_bahan:
            model_detail = detail.dict()
            list_bahan.append(model_detail)
        client, col = mongo.mongodb_config('BahanDetail')
        creator_id = {'creator_id':model.creator_id}
        value =  { "$set": { "list_bahan":list_bahan } }
        col.update_one(creator_id,value)
        client.close()
        return response.response_detail(200, "update bahan success", resp)
    except Exception as error:
        return response.response_detail(400, "failed update data bahan", resp)
