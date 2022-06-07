""" Auth Services """

import traceback
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pymongo import errors
from config import mongo
from utils import util
from model import auth_model

app = APIRouter()


@app.post('/register_umkm')
def register_umkm(data: auth_model.DataUMKM):
    """ A function to generate accounts of UMKM """
    try:
        if util.username_checker(data.username):

            model = {
                "_id": util.id_generator('UMKM'),
                "username": data.username,
                "password": util.sha256(data.password),
                "company_name": data.company_name,
                "company_address": data.company_address,
                "company_number": data.company_number,
                "factory_name": data.factory_name,
                "factory_address": data.factory_address,
                "role": "umkm",
                "email": data.email,
                "product_name": data.product_name,
                "product_type": data.product_type,
                "marketing_area": data.marketing_area,
                "marketing_system": data.marketing_system,
                "created_at": util.get_created_at()
            }
            client, col = mongo.mongo('Accounts')
            datas = col.insert_one(model)
            client.close()
            return datas.inserted_id
        else:
            raise HTTPException(400, 'Username Already Used')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, error) from error


@app.post('/register_auditor')
def register_auditor(data: auth_model.DataAuditor):
    """ A Function for register Auditor Account like a 'Fatwa','LBH','BPJPH' """
    try:
        if util.username_checker(data.username):
            model = {
                "_id": util.id_generator('AUDIT'),
                "no_ktp": data.no_ktp,
                "name": data.name,
                "username": data.username,
                "type": data.type,
                "role": "auditor",
                "password": util.sha256(data.password),
                "religion": data.religion,
                "address": data.address,
                "institution": data.institution,
                "competence": data.competence,
                "experience": data.experience,
                "cert_competence": data.cert_competence,
                "experied_cert": data.experied_cert,
                "auditor_experience": data.auditor_experience,
                "created_at": util.get_created_at()
            }
            client, col = mongo.mongo('Accounts')
            datas = col.insert_one(model)
            client.close()
            return datas.inserted_id
        else:
            raise HTTPException(400, 'Username Already Used')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Register") from error


@app.post('/register_consumen')
def register_consumer(data: auth_model.DataKonsumen):
    """ A function for register consumen accounts """
    try:
        if util.username_checker(data.username):
            model = {
                "_id": util.id_generator('CON'),
                "username": data.username,
                "password": util.sha256(data.password),
                "name": data.name,
                "email": data.email,
                "role": "consumen",
                "phone": data.phone,
                "address": data.address,
                "created_at": util.get_created_at()
            }
            client, col = mongo.mongo('Accounts')
            datas = col.insert_one(model)
            client.close()
            return datas.inserted_id
        else:
            raise HTTPException(400, 'Username Already Used')
    except errors.ExecutionTimeout as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Register") from error


@app.post('/login')
def login(login_data: auth_model.Login):
    """ A function for login """
    try:
        client, col = mongo.mongo('Accounts')
        datas = col.find_one({'$and': [{'username': login_data.username}, {
                             'password': util.sha256(login_data.password)}]})
        client.close()
        if datas is not None:
            del datas['password']
            return {
                "status": "success",
                "data": datas
            }
        else:
            traceback.print_exc()
            raise HTTPException(401, "Please check your username and password")
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(
            401, "Please check your username and password") from error
