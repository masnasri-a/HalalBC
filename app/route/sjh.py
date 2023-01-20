
import traceback
from fastapi import APIRouter, Response
from config import mongo
from utils import response


app = APIRouter()


@app.get("/detail_umkm")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    acc = col_acc.find_one({"_id": creator_id})
    raw_data = col.find({"creator": creator_id}, {'detail_umkm': 1})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)


@app.get("/penetapan_tim")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    acc = col_acc.find_one({"_id": creator_id})
    raw_data = col.find({"creator": creator_id}, {'penetapan_tim': 1})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)


@app.get("/bukti_pelaksanaan")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'bukti_pelaksanaan': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)


@app.get("/jawaban_evaluasi")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'jawaban_evaluasi': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)
    

@app.get("/jawaban_audit")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'jawaban_audit': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)
    

@app.get("/daftar_hasil_kaji")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'daftar_hasil_kaji': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)
    
    
@app.get("/pembelian")
def detail_umkm(creator_id: str, resp: Response):
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'pembelian': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)
    

@app.get("/pembelian_import")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'pembelian_import': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)
    

@app.get("/stok_barang")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'stok_barang': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)


@app.get("/form_produksi")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'form_produksi': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)


@app.get("/form_pemusnahan")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'form_pemusnahan': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)


@app.get("/form_pengecekan_kebersihan")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'form_pengecekan_kebersihan': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)


@app.get("/daftar_bahan_halal")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'daftar_bahan_halal': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)


@app.get("/matriks_produk")
def detail_umkm(creator_id: str, resp: Response):
    
    client, col = mongo.mongodb_config('DocumentDetails')
    client_acc, col_acc = mongo.mongodb_config('Accounts')
    raw_data = col.find({"creator": creator_id}, {'matriks_produk': 1})
    acc = col_acc.find_one({"_id": creator_id})
    document_detail = list(raw_data)[-1]
    payload = {
        **document_detail,
        "creator_detail": acc
    }
    client.close()
    client_acc.close()
    return response.response_detail(200, payload, resp)