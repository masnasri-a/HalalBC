""" umkm  routing pages """

from fastapi import APIRouter, Response
# from utils import word
from model import umkm_model
from utils import response, util
from config import mongo


app = APIRouter()

# @app.post('/submission_criteria')
# def submission_criteria():
# @app.get('/test_create_docx')
# def create_docx():
#     """ function for create docs """
#     word.word_generator()


@app.post('/create_init', status_code=200)
def create_init(model: umkm_model.InitUMKM, resp: Response):
    """ function init docs """
    try:
        data = {
            "_id": util.id_generator('DOC'),
            "type": "init",
            "creator": model.creator_id
        }
        client, col = mongo.mongo('UMKM')
        col.insert_one(data)
        client.close()
        return response.response_detail(200, {'doc_id': data}, resp)
    except Exception as error:
        print(error)
        return response.response_detail(400, error, resp)


@app.post('/insert_detail_umkm', status_code=200)
def detail_umkm(data_model: umkm_model.UmkmDetail, resp: Response):
    """ function  """
    try:
        data = {
            '_id': data_model.id,
            "type": "detail_umkm",
            "nama_ketua": data_model.nama_ketua,
            "nama_penanggungjawab": data_model.nama_penanggungjawab,
            "logo_perusahaan": data_model.logo_perusahaan,
            "ttd_penanggungjawab": data_model.ttd_penanggungjawab,
            "ttd_ketua": data_model.ttd_ketua
        }
        client, col = mongo.mongo('UMKM')
        datas = col.insert_one(data)
        client.close()
        res = response.response_detail(200, str(datas.inserted_id), resp)
        return res
    except Exception as error:
        print(error)
        return response.response_detail(400, error, resp)


@app.post('/insert_penetapan_tim', status_code=200)
def penetapan_tim(data_model: dict, resp: Response):
    """{"id":"",data:
    [{
        "nama":"names1",
        "jabata":"job1",
        "posisiton":"posisi1"
    },{
        "nama":"names1",
        "jabata":"job1",
        "posisiton":"posisi1"
    },{
        "nama":"names1",
        "jabata":"job1",
        "posisiton":"posisi1"
    }]}
    """
    try:
        client, col = mongo.mongo('UMKM')
        datas = col.insert_one(data_model)
        client.close()
        res = response.response_detail(200, str(datas.inserted_id), resp)
        return res
    except Exception as error:
        print(error)
        return response.response_detail(400, error, resp)


@app.post('/insert_bukti_pelaksanaan', status_code=200)
def bukti_pelaksanaan(data_model: umkm_model.Pelaksanaan, resp: Response):
    """{
  "id": "UKMa12312312321",
  "tanggal_pelaksanaan": 123123123123,
  "pemateri": "pemateri",
  "data": [
    {
      "nama": "",
      "posisi": "",
      "ttd": "",
      "nilai": 100
    },
    {
      "nama": "",
      "posisi": "",
      "ttd": "",
      "nilai": 100
    },
    {
      "nama": "",
      "posisi": "",
      "ttd": "",
      "nilai": 100
    }
  ]
}
    """
    try:
        model = {
            "id": data_model.id,
            "tanggal_pelaksanaan": data_model.tanggal_pelaksanaan,
            "pemateri": data_model.pemateri,
            "data": data_model.data
        }
        client, col = mongo.mongo('UMKM')
        datas = col.insert_one(model)
        client.close()
        res = response.response_detail(200, str(datas.inserted_id), resp)
        return res
    except Exception as error:
        print(error)
        return response.response_detail(400, error, resp)

@app.get('/get_soal_evaluasi')
def soal_evaluasi(resp:Response):
    data = [
        {
            "id":1,
            "soal":"Allah SWT memerintahkan Manusia untuk konsumsi makanan yang….",
            "jawaban":{
                "a":"Halal",
                "b":"Thoyib",
                "c":"Kotor",
                "d":"a dan b"
            }
        },{
            "id":2,
            "soal":"Berikut makanan dan minuman yang halal adalah",
            "jawaban":{
                "a":"Klepon",
                "b":"Anjing",
                "c":"Babi",
                "d":"Bangkai Ayam"
            }
        },{
            "id":3,
            "soal":"Daging Babi dan turunannya merupakan najis",
            "jawaban":{
                "a":"Ringan (mukhaffafah)",
                "b":"Berat (mughallazhah)",
                "c":"Sedang (mutawassithah)",
                "d":"Tidak Najis"
            }
        },{
            "id":4,
            "soal":"Cara Mengghilangkan Najis Sedang (mutawassithah) yaitu",
            "jawaban":{
                "a":"Dengan mengucurinya dengan air atau mencucinya di dalam air yang banyak (direndam) hingga hilang rasa, bau dan warna dari bahan najisnya",
                "b":"Di Diamkan Saja",
                "c":"Di Bakar",
                "d":"Dicuci tujuh kali dengan air dan salah satunya dengan tanah atau bahan lain yang mempunyai kemampuan menghilangkan rasa, bau dan warna"
            }
        },{
            "id":5,
            "soal":"Cara Mengghilangkan Najis Berat (mughallazhah) yaitu",
            "jawaban":{
                "a":"Dengan mengucurinya dengan air atau mencucinya di dalam air yang banyak (direndam) hingga hilang rasa, bau dan warna dari bahan najisnya.",
                "b":"Di Diamkan Saja",
                "c":"Di Bakar",
                "d":"Dicuci tujuh kali dengan air dan salah satunya dengan tanah atau bahan lain yang mempunyai kemampuan menghilangkan rasa, bau dan warna."
            }
        },{
            "id":6,
            "soal":"Cara menjaga Konsistensi dalam memproduksi Produk dan bahan yang halal perusahaan harus menerapkan",
            "jawaban":{
                "a":"Sistem Keamanan Pangan",
                "b":"Sistem Keselamatan Kerja",
                "c":"Sistem Jaminan Halal",
                "d":"Sistem Informasi"
            }
        },{
            "id":7,
            "soal":"Kriteria Sistem Jaminan Halal Terdiri dari …. Kriteria",
            "jawaban":{
                "a":"11",
                "b":"20",
                "c":"12",
                "d":"14"
            }
        },{
            "id":8,
            "soal":"Aktifitas manakah dibawah ini yang merupakan aktifitas kritis dalam Sistem Jaminan Halal",
            "jawaban":{
                "a":"Seleksi Bahan Baru",
                "b":"Pembelian",
                "c":"Formulasi Produk baru",
                "d":"Semua Benar"
            }
        },{
            "id":9,
            "soal":"Setiap ada Bahan Baru perusahaan tidak wajib melaporkan kepada LPPOM MUI",
            "jawaban":{
                "a":"benar",
                "b":"salah"
            }
        },{
            "id":10,
            "soal":"Audit Internal dilakukan 6 Bulan Sekali dan dilaporkan kepada LPPOM MUI",
            "jawaban":{
                "a":"benar",
                "b":"salah"
            }
        }
    ]
    return response.response_detail(200, data, resp)
    