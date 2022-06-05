import traceback
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from config import mongo
from utils import util
from model import auth_model

app = APIRouter()

@app.post('/register_umkm')
def register_umkm(data: auth_model.DataUMKM):
    try:
        model = {
            "id":util.id_generator(),
            "company_name":data.company_name,
            "company_address":data.company_address,
            "company_number":data.company_number,
            "factory_name":data.factory_name,
            "factory_address":data.factory_address,
            "email":data.email,
            "product_name":data.product_name,
            "product_type":data.product_type,
            "marketing_area":data.marketing_area,
            "marketing_system":data.marketing_system
        }
        client, col = mongo.mongo('Accounts')
        datas = col.insert_one(model)
        client.close
        return datas.inserted_id
    except:
        raise HTTPException(400, "Failed Register")

@app.post('/register_auditor')
def register_auditor(data: auth_model.DataAuditor):
    try:
        model = {
            "_id": util.id_generator(),
            "no_ktp":data.no_ktp,
            "name":data.name,
            "religion":data.religion,
            "address":data.address,
            "isntitution":data.isntitution,
            "competence":data.competence,
            "experience":data.experience,
            "cert_competence":data.cert_competence,
            "experied_cert":data.experied_cert,
            "auditor_experience":data.auditor_experience
        }
        client, col = mongo.mongo('Accounts')
        datas = col.insert_one(model)
        client.close
        return datas.inserted_id
    except:
        raise HTTPException(400, "Failed Register")

@app.post('/login')
def login(login_data : auth_model.Login):
    try:
        client, col = mongo.mongo('Accounts')
        datas = col.find_one({'$and':[{'name':login_data.username},{'password':util.sha256(login_data.password)}]})
        client.close
        if datas != None:
            del datas['password']
            return {
                "status":"success",
                "data":datas
            }
        else:
            raise HTTPException(401, "Please check your username and password")
    except:
        raise HTTPException(401, "Please check your username and password")