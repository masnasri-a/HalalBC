from fastapi import APIRouter
from config import mongo
from utils import util
from model import auth_model

app = APIRouter()

@app.post('/register')
def register_umkm():
    # Test Insert
    test_insert = {
        "_id":123123123123,
        "name":"nasri",
        "email":"nasriblog12@gmail.com",
        "role":"goverment",
        "password":util.sha256("UtyCantik12")
    }
    client, col = mongo.mongo('Accounts')
    datas = col.insert_one(test_insert)
    client.close
    return datas.inserted_id

@app.post('/login')
def login(login_data : auth_model.Login):
    print(login_data)
