""" Account Services """

from typing import Optional
import traceback
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pymongo import errors
from config import mongo
from utils import util
from model import account_model


app = APIRouter()


@app.get("/get_auditor")
def get_auditor(id: str):
    """ A function to get Auditor Account by id """
    try:
        client, col = mongo.mongodb_config('Accounts')
        data = col.find_one({'_id': id, 'role': 'auditor'})
        if data is not None:
            return data
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Get Auditor") from error


@app.get("/get_all_auditor")
def get_all_auditor():
    """ A function to get all Auditor Account """
    try:
        client, col = mongo.mongodb_config('Accounts')
        data = col.find({'role': 'auditor'})
        if data is not None:
            return [d for d in data]
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Get all Auditor") from error


@app.post('/update_auditor')
def update_auditor(data: account_model.DataAuditor):
    """ A function to update Auditor Account """
    try:
        client, col = mongo.mongodb_config('Accounts')
        datas = col.find_one({'_id': data.id})
        if datas is not None:
            model = {
                "no_ktp": data.no_ktp,
                "name": data.name,
                "religion": data.religion if data.religion else datas['religion'],
                "address": data.address if data.address else datas['address'],
                "institution": data.institution if data.institution else datas['institution'],
                "competence": data.competence if data.competence else datas['competence'],
                "experience": data.experience if data.experience else datas['experience'],
                "cert_competence": data.cert_competence if data.cert_competence else datas['cert_competence'],
                "experied_cert": data.experied_cert if data.experied_cert else datas['experied_cert'],
                "auditor_experience": data.auditor_experience if data.auditor_experience else datas['auditor_experience'],
            }
            col.update_one({'_id': data.id}, {"$set": model})
            client.close()
            return data.id
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Update Auditor") from error


@app.get("/get_umkm")
def get_umkm(id: str):
    """ A function to get UMKM Account by id """
    try:
        client, col = mongo.mongodb_config('Accounts')
        data = col.find_one({'_id': id, 'role': 'umkm'})
        if data is not None:
            return data
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Get UMKM") from error


@app.get("/get_all_umkm")
def get_all_umkm(lph_id:Optional[str] = "all" ):
    """ A function to get all UMKM Account """
    try:
        client, col = mongo.mongodb_config('Accounts')
        if lph_id != "all":
            data = col.find({'$and':[{'role': 'umkm'},{'lph_appointment.lph_id':lph_id}]})
            list_id = []
            for detail in data:
                list_id.append(detail['umkm_id'])
            query = {'_id':{'$in':list_id}}
            datas = col.find(query)
            if datas is not None:
                return [detail for detail in datas]
            else:
                client.close()
                raise HTTPException(404, 'Account not found')
        else:
            data = col.find({'role': 'umkm'})
            if data is not None:
                return [detail for detail in data]
            else:
                client.close()
                raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Get all UMKM") from error

@app.get("/get_all_umkm_area")
def get_all_umkm_area(marketing_area: str):
    """ A function to get all UMKM Account by marketing area """
    try:
        client, col = mongo.mongodb_config('Accounts')
        data = col.find({'role': 'umkm', 'marketing_area': marketing_area})
        if data is not None:
            return [d for d in data]
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Get all UMKM") from error


@app.post('/update_umkm')
def update_umkm(data: account_model.DataUMKM):
    """ A function to update UMKM Account """
    try:
        client, col = mongo.mongodb_config('Accounts')
        datas = col.find_one({'_id': data.id})
        if datas is not None:
            model = {
                "company_name": data.company_name,
                "company_address": data.company_address if data.company_address else datas['company_address'],
                "company_number": data.company_number if data.company_number else datas['company_number'],
                "factory_name": data.factory_name,
                "factory_address": data.factory_address if data.factory_address else datas['factory_address'],
                "email": data.email if data.email else datas['email'],
                "product_name": data.product_name,
                "product_type": data.product_type,
                "marketing_area": data.marketing_area if data.marketing_area else datas['marketing_area'],
                "marketing_system": data.marketing_system if data.marketing_system else datas['marketing_system'],
            }
            col.update_one({'_id': data.id}, {"$set": model})
            client.close()
            return data.id
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Update UMKM") from error


@app.get("/get_consumen")
def get_consumen(id: str):
    """ A function to get Consumen Account by id """
    try:
        client, col = mongo.mongodb_config('Accounts')
        data = col.find_one({'_id': id, 'role': 'consumen'})
        if data is not None:
            return data
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Update Auditor") from error


@app.get("/get_all_consumen")
def get_all_consumen():
    """ A function to get all Consumen Account """
    try:
        client, col = mongo.mongodb_config('Accounts')
        data = col.find({'role': 'consumen'})
        if data is not None:
            return [d for d in data]
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Get all Consumen") from error


@app.post('/update_consumen')
def update_consumen(data: account_model.DataKonsumen):
    """ A function to update consumen Account """
    try:
        client, col = mongo.mongodb_config('Accounts')
        datas = col.find_one({'_id': data.id})
        if datas is not None:
            model = {
                "name": data.name,
                "email": data.email if data.email else datas['email'],
                "phone": data.phone if data.phone else datas['phone'],
                "address": data.address if data.address else datas['address'],
            }
            col.update_one({'_id': data.id}, {"$set": model})
            client.close()
            return data.id
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Update Consumen") from error


@app.post("/update_password")
def update_password(data: account_model.DataPassword):
    """ A function to change Account password """
    try:
        client, col = mongo.mongodb_config('Accounts')
        datas = col.find_one({'_id': data.id})
        if datas is not None:
            if util.sha256(data.password) == datas['password']:
                col.update_one({'_id': data.id}, {
                               "$set": {"password": util.sha256(data.new_password)}})
                client.close()
                return data.id
            else:
                client.close()
                raise HTTPException(400, 'Password is invalid')
        else:
            client.close()
            raise HTTPException(404, 'Account not found')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Update Password") from error
