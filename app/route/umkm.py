""" umkm  routing pages """

import traceback
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
from app.utils import pdf
from app.model import umkm_model
from app.utils import response, util
from app.config import mongo


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
        _id = util.id_generator('DOC')
        data = {
            "_id": _id,
            "type": "init",
            "creator": model.creator_id
        }
        client, col = mongo.mongodb_config('UMKM')
        col.insert_one(data)
        client.close()
        client, col_log = mongo.mongodb_config('Log')
        model = {
            "_id": _id,
            "creator":model.creator_id,
            "status": "init",
            "detail_umkm": False,
            "penetapan_tim": False,
            "bukti_pelaksanaan": False,
            "jawaban_evaluasi": False,
            "jawaban_audit": False,
            "daftar_hasil_kaji": False,
            "pembelian": False,
            "pembelian_import": False,
            "stok_barang": False,
            "form_produksi": False,
            "form_pemusnahan": False,
            "form_pengecekan_kebersihan": False,
            "daftar_bahan_halal": False,
            "matriks_produk": False
        }
        col_log.insert_one(model)
        return response.response_detail(200, {'doc_id': data}, resp)
    except Exception as error:
        traceback.print_exc()
        print(error)
        return response.response_detail(400, error, resp)


@app.get('/get_ukmk_detail')
def details(creator_id, resp: Response):
    try:
        client, col = mongo.mongodb_config('Log')
        data = col.find_one({"creator": creator_id})
        return response.response_detail(200, data, resp)

    except Exception as error:
        print(error)
        return response.response_detail(400, error, resp)


@app.post('/insert_detail_umkm', status_code=200)
def detail_umkm(data_model: umkm_model.UmkmDetail, resp: Response):
    """ function  """
    try:
        _id = util.id_generator('Detail')
        data = {
            "nama_ketua": data_model.nama_ketua,
            "no_telp_ketua":data_model.no_ktp_ketua,
            "no_ktp_ketua":data_model.no_ktp_ketua,
            "nama_penanggungjawab": data_model.nama_penanggungjawab,
            "logo_perusahaan": data_model.logo_perusahaan,
            "ttd_penanggungjawab": data_model.ttd_penanggungjawab,
            "ttd_ketua": data_model.ttd_ketua
        }
        model = {
            '_id':_id,
            'doc_id': data_model.id,
            "type": "detail_umkm",
            "data": data
        }
        client, col = mongo.mongodb_config('DetailUMKM')
        datas = col.insert_one(model)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data_model.id}
        newvalues = {"$set": {'status': 'detail_umkm'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set": {'detail_umkm': True}}
        log_col.update_one(change, newvalues)
        client.close()
        res = response.response_detail(200, str(datas.inserted_id), resp)
        return res
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, error, resp)


@app.post('/insert_penetapan_tim', status_code=200)
def penetapan_tim(doc_id:str, data_model: dict, resp: Response):
    """[{
        "nama":"names1",
        "jabatan":"job1",
        "position":"posisi1"
    }]
    """
    try:
        model = {
            "_id": util.id_generator('Detail'),
            "type": "penetapan_tim",
            "doc_id":doc_id,
            "data": data_model
        }
        client, col = mongo.mongodb_config('DetailUMKM')
        datas = col.insert_one(model)
        client.close()

        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': doc_id}
        newvalues = {"$set":{'status': 'penetapan_tim'}}
        log_col.update_one(change, newvalues)
        newvalues = { "$set":{'penetapan_tim': True}}
        log_col.update_one(change, newvalues)
        client.close()

        res = response.response_detail(200, str(datas.inserted_id), resp)
        return res
    except Exception as error:
        print(error)
        return response.response_detail(400, error, resp)


@app.post('/insert_bukti_pelaksanaan', status_code=200)
def bukti_pelaksanaan(data_model: umkm_model.Pelaksanaan, resp: Response):
    """{
  "id": "DOC:123123123",
  "tanggal_pelaksanaan": 123123123123,
  "pemateri": "pemateri",
  "data": [
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
            "tanggal_pelaksanaan": data_model.tanggal_pelaksanaan,
            "pemateri": data_model.pemateri,
            "data": data_model.data
        }
        data = {
            "_id": util.id_generator('Detail'),
            "doc_id": data_model.id,
            "type": "bukti_pelaksanaan",
            "model_data": model
        }

        client, col = mongo.mongodb_config('DetailUMKM')
        datas = col.insert_one(data)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data_model.id}
        newvalues = {"$set": {'status': 'bukti_pelaksanaan'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set": {'bukti_pelaksanaan': True}}
        log_col.update_one(change, newvalues)
        client.close()
        res = response.response_detail(200, str(datas.inserted_id), resp)
        return res
    except Exception as error:
        traceback.print_exc()
        print(error)
        return response.response_detail(400, error, resp)


@app.get('/get_soal_evaluasi')
def soal_evaluasi(resp: Response):
    """ soal evaluasi """
    data = [
        {
            "id": 1,
            "soal": "Allah SWT memerintahkan Manusia untuk konsumsi makanan yang….",
            "jawaban": {
                "a": "Halal",
                "b": "Thoyib",
                "c": "Kotor",
                "d": "a dan b"
            }
        }, {
            "id": 2,
            "soal": "Berikut makanan dan minuman yang halal adalah",
            "jawaban": {
                "a": "Klepon",
                "b": "Anjing",
                "c": "Babi",
                "d": "Bangkai Ayam"
            }
        }, {
            "id": 3,
            "soal": "Daging Babi dan turunannya merupakan najis",
            "jawaban": {
                "a": "Ringan (mukhaffafah)",
                "b": "Berat (mughallazhah)",
                "c": "Sedang (mutawassithah)",
                "d": "Tidak Najis"
            }
        }, {
            "id": 4,
            "soal": "Cara Mengghilangkan Najis Sedang (mutawassithah) yaitu",
            "jawaban": {
                "a": "Dengan mengucurinya dengan air atau mencucinya di dalam air yang banyak (direndam) hingga hilang rasa, bau dan warna dari bahan najisnya",
                "b": "Di Diamkan Saja",
                "c": "Di Bakar",
                "d": "Dicuci tujuh kali dengan air dan salah satunya dengan tanah atau bahan lain yang mempunyai kemampuan menghilangkan rasa, bau dan warna"
            }
        }, {
            "id": 5,
            "soal": "Cara Mengghilangkan Najis Berat (mughallazhah) yaitu",
            "jawaban": {
                "a": "Dengan mengucurinya dengan air atau mencucinya di dalam air yang banyak (direndam) hingga hilang rasa, bau dan warna dari bahan najisnya.",
                "b": "Di Diamkan Saja",
                "c": "Di Bakar",
                "d": "Dicuci tujuh kali dengan air dan salah satunya dengan tanah atau bahan lain yang mempunyai kemampuan menghilangkan rasa, bau dan warna."
            }
        }, {
            "id": 6,
            "soal": "Cara menjaga Konsistensi dalam memproduksi Produk dan bahan yang halal perusahaan harus menerapkan",
            "jawaban": {
                "a": "Sistem Keamanan Pangan",
                "b": "Sistem Keselamatan Kerja",
                "c": "Sistem Jaminan Halal",
                "d": "Sistem Informasi"
            }
        }, {
            "id": 7,
            "soal": "Kriteria Sistem Jaminan Halal Terdiri dari …. Kriteria",
            "jawaban": {
                "a": "11",
                "b": "20",
                "c": "12",
                "d": "14"
            }
        }, {
            "id": 8,
            "soal": "Aktifitas manakah dibawah ini yang merupakan aktifitas kritis dalam Sistem Jaminan Halal",
            "jawaban": {
                "a": "Seleksi Bahan Baru",
                "b": "Pembelian",
                "c": "Formulasi Produk baru",
                "d": "Semua Benar"
            }
        }, {
            "id": 9,
            "soal": "Setiap ada Bahan Baru perusahaan tidak wajib melaporkan kepada LPPOM MUI",
            "jawaban": {
                "a": "benar",
                "b": "salah"
            }
        }, {
            "id": 10,
            "soal": "Audit Internal dilakukan 6 Bulan Sekali dan dilaporkan kepada LPPOM MUI",
            "jawaban": {
                "a": "benar",
                "b": "salah"
            }
        }
    ]
    return response.response_detail(200, data, resp)


@app.post('/input_jawaban', status_code=200)
def jawaban(data: umkm_model.InputJawabanEvaluasi, resp: Response) -> bool:
    """
    # example = {"id":asdasdasd,"nama":"Eka Widiawati","Tanggal":"19 Agustus 2021",1:"a",2:"b",3:"a",4:"a",5:"b",6:"a",7:"a",8:"b",9:"a",10:"a"}
    """
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        model = {
            "_id": util.id_generator('Detail'),
            "doc_id": data.id,
            "type": "jawaban_evaluasi",
            "nama": data.nama,
            "data": data.data
        }
        datas = col.insert_one(model)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data.id}
        newvalues = {"$set": {'status': 'jawaban_evaluasi'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set": {'jawaban_evaluasi': True}}
        log_col.update_one(change, newvalues)
        client.close()
        res = response.response_detail(200, str(datas.inserted_id), resp)
        return res
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, error, resp)


@app.get('/get_audit_internal')
def get_audit_internal():
    """ soal audit internal """
    try:
        model = [
            {
                "id": 1,
                "soal": "Apakah kebijakan halal telah dijelaskan pada semua karyawan ?"
            }, {
                "id": 2,
                "soal": "Apakah ada bukti sosialisasi kebijakan halal ? (daftar hadir sosialisasi)"
            }, {
                "id": 3,
                "soal": "Apakah tersedia poster kebijakan halal dan edukasi halal di kantor, area produksi dan  udang?"
            }, {
                "id": 4,
                "soal": "Apakah ketua/anggota Tim Manajemen Halal telah mengikuti pelatihan eksternal setidaknya sekali dalam dua tahun?"
            }, {
                "id": 5,
                "soal": "Apakah ada bukti pelatihan eksternal (sertifikat pelatihan) ?"
            }, {
                "id": 6,
                "soal": "Apakah pelatihan internal kepada semua karyawan, termasuk karyawan baru, dengan materi seperti tercantum dalam Lampiran 3 telah dilaksanakan setidaknya setahun sekali ?"
            }, {
                "id": 7,
                "soal": "Apakah ada bukti pelatihan internal (daftar hadir pelatihan) ?"
            }, {
                "id": 8,
                "soal": "Apakah Daftar Bahan dengan format seperti pada Lampiran 4 telah dibuat ?"
            }, {
                "id": 9,
                "soal": "Apakah nama/merk bahan dan nama produsen bahan yang dibeli sesuai dengan yang tercantum dalam Daftar Bahan Halal ?"
            }, {
                "id": 10,
                "soal": "Apakah bukti pembelian (nota/kuitansi) dan contoh label kemasan (jika ada) selalu disimpan setidaknya selama 6 bulan ?"
            }, {
                "id": 11,
                "soal": "Apakah setiap ada bahan baru selalu dimintakan persetujuan ke LPPOM MUI sebelum digunakan? (kecuali bahan tidak kritis dan bahan bersertifikat halal MUI yang ada di www.halalmui.org)"
            }, {
                "id": 12,
                "soal": "Apakah bukti persetujuan penggunaan bahan baru dari LPPOM MUI selalu disimpan setidaknya selama dua tahun ?"
            }, {
                "id": 13,
                "soal": "Apakah dilakukan pemeriksaan label bahan pada setiap pembelian atau penerimaan bahan ? (kecuali bahan tidak kritis)"
            }, {
                "id": 14,
                "soal": "Apakah hasil pemeriksaan menunjukkan informasi nama bahan dan produsen yang tercantum di label sesuai dengan Daftar Bahan Halal ?"
            }, {
                "id": 15,
                "soal": "Apakah ada formula/resep produk baku (untuk produk yang memiliki formula) ?"
            }, {
                "id": 16,
                "soal": "Apakah bahan yang digunakan dalam produksi hanya bahan yang tercantum dalam Daftar Bahan ?"
            }, {
                "id": 17,
                "soal": "Apakah formula produk yang digunakan pada proses produksi mengacu pada formula baku ?"
            }, {
                "id": 18,
                "soal": "Jika terlanjur ada penggunaan bahan yang tidak tercantum dalam Daftar Bahan Halal, apakah produk yang dihasilkan tidak akan dijual ke konsumen dan dimusnahkan ?"
            }, {
                "id": 19,
                "soal": "Apakah semua fasilitas dan peralatan produksi selalu dalam keadaan bersih (bebas dari najis) sebelum dan sesudah digunakan ?"
            }, {
                "id": 20,
                "soal": "Apakah bahan dan produk selalu disimpan di tempat yang bersih dan terhindar dari najis?"
            }, {
                "id": 21,
                "soal": "Apakah kendaraan yang digunakan untuk mengangkut produk halal dalam kondisi baik dan tidak digunakan untuk mengangkut produk lain yang diragukan kehalalannya ?"
            }, {
                "id": 22,
                "soal": "Apakah setiap ada produk baru dengan merk yang sama selalu disertifikasi halal sebelum dipasarkan?"
            }, {
                "id": 23,
                "soal": "Apakah setiap ada penambahan fasilitas produksi baru selalu didaftarkan untuk disertifikasi ?"
            }, {
                "id": 24,
                "soal": "Apakah telah dilakukan audit internal setiap enam bulan sekali dengan cara memeriksa pelaksanaan seluruh prosedur operasional ? *"
            }, {
                "id": 25,
                "soal": "Apakah audit internal dilakukan oleh ketua/ anggota Tim Manajemen Halal yang sudah mengikuti pelatihan ? *"
            }, {
                "id": 26,
                "soal": "Apakah ada bukti pelaksanaan audit internal? *"
            }, {
                "id": 27,
                "soal": "Apakah hasil audit internal telah dibahas dalam rapat kaji ulang manajemen yang dihadiri oleh ketua dan anggota Tim Manajemen Halal ? *"
            }, {
                "id": 28,
                "soal": "Jika dalam audit internal ditemukan kelemahan, yaitu ada pertanyaan yang dijawab “tidak”, apakah segera dilakukan perbaikan agar kelemahan tersebut tidak terulang ? *"
            }, {
                "id": 29,
                "soal": "Jika dalam audit internal ditemukan kelemahan, apakah ada bukti pelaksanaan perbaikan ? *"
            }, {
                "id": 30,
                "soal": "Apakah ada bukti pelaksanaan rapat kaji ulang manajemen ? *"
            }, {
                "id": 31,
                "soal": "Apakah form hasil audit internal yang telah terisi telah dikirimkan ke LPPOM MUI melalui Cerol? *"
            }
        ]
        return model
    except Exception as error:
        raise HTTPException(400, "error getting data") from error


@app.post('/jawaban_audit_internal')
def jawaban_audit(data: umkm_model.JawabanAuditInternal, resp: Response):
    """ exmaple
    {
  "jawaban": [
    {
      "id": 1,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 2,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 3,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 4,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 5,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 6,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 7,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 8,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 9,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 10,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 11,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 12,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 13,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 14,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 15,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 16,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 17,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 18,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 19,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 20,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 21,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 22,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 23,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 24,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 25,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 26,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 27,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 28,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 29,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 30,
      "jawaban": true,
      "keterangan": ""
    },
    {
      "id": 31,
      "jawaban": true,
      "keterangan": ""
    }
  ]
}
    """
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        model = {
            "_id": util.id_generator('Detail'),
            "doc_id": data.id,
            "type": "jawaban_audit",
            "auditee": data.auditee,
            "nama_auditor": data.nama_auditor,
            "bagian_diaudit": data.bagian_diaudit,
            "data": data.data
        }
        datas = col.insert_one(model)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data.id}
        newvalues = {"$set": {'status': 'jawaban_audit'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set": {'jawaban_audit': True}}
        log_col.update_one(change, newvalues)
        client.close()
        res = response.response_detail(200, str(datas.inserted_id), resp)
        return res
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, error, resp)


@app.post('/daftar_hadir_kaji')
def daftar_hadir_kaji(model: umkm_model.DaftarHadirKaji, resp: Response):
    """ daftar hadir kaji ulang \n  docx hal 18"""
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        data = {
            "_id": util.id_generator('Detail'),
            "doc_id": model.id,
            "tanggal": model.tanggal,
            "list_orang": model.list_orang,
            "pembahasan": model.pembahasan
        }
        datas = {
            "type": "daftar_hasil_kaji",
            "data": data
        }
        datas = col.insert_one(datas)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': model.id}
        newvalues = {"$set":{'status': 'daftar_hasil_kaji'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set":{'daftar_hasil_kaji': True}}
        log_col.update_one(change, newvalues)
        client.close()
        return response.response_detail(200, str(datas.inserted_id), resp)
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, error, resp)


@app.post('/generate_lampiran')
def generate_lampiran(doc_id:str, resp: Response):
    try:
        client, coll = mongo.mongodb_config("DetailUMKM")
        client, coll = mongo.mongodb_config("DetailUMKM")
        data = coll.find_one({'$and':[{'doc_id':doc_id},{'type':'detail_umkm'}]})
        detail = data['data']
        client.close()
        client, coll_umkm = mongo.mongodb_config("UMKM")
        creator = coll_umkm.find_one({'_id':doc_id})
        client.close()
        client, coll_acc = mongo.mongodb_config("Accounts")
        detail_account = coll_acc.find_one({'_id':creator['creator']})
        files = pdf.Lampiran(detail['nama_ketua'],detail['no_ktp_ketua'], detail['no_telp_ketua'],
        "Pemimpin Perusahaan",detail_account['company_name'], detail_account['company_address'],
        detail_account['marketing_area'])
        return FileResponse(files,media_type='application/octet-stream',filename='lampiran.pdf')
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, error, resp)


# BIKIN DOWNLOAD LAMPIRAN 6


@app.post('/form_pembelian_pemeriksaan')
def pembelian_pemeriksaan(pemeriksaan: umkm_model.Pemeriksaan, resp: Response):
    """ form pembelian dan pemeriksaan bahan """
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        data = {
            "_id": util.id_generator('Detail'),
            "doc_id":pemeriksaan.id,
            "type": "pembelian",
            "data": pemeriksaan.data
        }
        datas = col.insert_one(data)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': pemeriksaan.id}
        newvalues = { "$set":{'status': 'pembelian'}}
        log_col.update_one(change, newvalues)
        newvalues = { "$set":{'pembelian': True}}
        log_col.update_one(change, newvalues)
        client.close()
        return response.response_detail(200, str(datas.inserted_id), resp)
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, error, resp)


@app.post('/form_pembelian_pemeriksaan_import')
def pembelian_pemeriksaan(data: umkm_model.Pemeriksaan, resp: Response):
    """ form pembelian dan pemeriksaan bahan import"""
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        datas = {
            "_id": util.id_generator('Detail'),
            "doc_id":data.id,
            "type": "pembelian_import",
            "data": data.data
        }
        datas = col.insert_one(datas)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data.id}
        newvalues = {"$set":{'status': 'pembelian_import'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set":{'pembelian_import': True}}
        log_col.update_one(change, newvalues)
        client.close()
        return response.response_detail(200, str(datas.inserted_id), resp)
    except Exception as error:
        return response.response_detail(400, error, resp)


@app.post('/form_stok_barang')
def form_stok_barang(data: umkm_model.StokBarang, resp: Response):
    """ form pembelian dan pemeriksaan bahan import"""
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        model = {
            "_id": util.id_generator('Detail'),
            "type": "stok_barang",
            "data": data.data
        }
        datas = col.insert_one(model)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data.id}
        newvalues = {"$set":{'status': 'stok_barang'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set":{'stok_barang': True}}
        log_col.update_one(change, newvalues)
        client.close()
        return response.response_detail(200, str(datas.inserted_id), resp)
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, error, resp)


@app.post('/form_produksi')
def form_produksi(data: umkm_model.FormProduksi, resp: Response):
    """ form pembelian dan pemeriksaan bahan import"""
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        model = {
            "_id": util.id_generator('Detail'),
            "type": "form_produksi",
            "data": data.data
        }
        datas = col.insert_one(model)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data.id}
        newvalues = {"$set":{'status': 'form_produksi'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set":{'form_produksi': True}}
        log_col.update_one(change, newvalues)
        client.close()
        return response.response_detail(200, str(datas.inserted_id), resp)
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, error, resp)


@app.post('/form_pemusnahan')
def form_produksi(data: umkm_model.FormPemusnahan, resp: Response):
    """ form pembelian dan pemeriksaan bahan import"""
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        model = {
            "_id": util.id_generator('Detail'),
            "type": "form_pemusnahan",
            "data": data.data
        }
        datas = col.insert_one(model)
        client.close()
        client, col_col = mongo.mongodb_config('Log')
        change = {'_id': data.id}
        newvalues = {"$set":{'status': 'form_pemusnahan'}}
        col_col.update_one(change, newvalues)
        newvalues = {"$set":{'form_pemusnahan': True}}
        col_col.update_one(change, newvalues)
        client.close()
        return response.response_detail(200, str(datas.inserted_id), resp)
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, error, resp)


@app.post('/form_pengecekan_kebersihan')
def form_pengecekan_kebersihan(data: umkm_model.FormPengecekanKebersihan, resp: Response):
    """ form pembelian dan pemeriksaan bahan import"""
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        model = {
            "_id": util.id_generator('Detail'),
            "type": "form_pengecekan_kebersihan",
            "data": data.data
        }
        datas = col.insert_one(model)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data.id}
        newvalues = {"$set":{'status': 'form_pengecekan_kebersihan'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set":{'form_pengecekan_kebersihan': True}}
        log_col.update_one(change, newvalues)
        client.close()
        return response.response_detail(200, str(datas.inserted_id), resp)
    except Exception as error:
        return response.response_detail(400, error, resp)


@app.post('/daftar_barang_halal')
def daftar_bahan_halal(data: umkm_model.DaftarBarangHalal, resp: Response):
    """ form pembelian dan pemeriksaan bahan import"""
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        model = {
            "_id": util.id_generator('Detail'),
            "type": "daftar_bahan_halal",
            "data": data.data
        }
        datas = col.insert_one(model)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data.id}
        newvalues = {"$set": {'status': 'daftar_bahan_halal'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set": {'daftar_bahan_halal': True}}
        log_col.update_one(change, newvalues)
        client.close()
        return response.response_detail(200, str(datas.inserted_id), resp)
    except Exception as error:
        return response.response_detail(400, error, resp)


@app.post('/matriks_produk')
def matriks_produk(data: umkm_model.MatrixProduksi, resp: Response):
    """ form pembelian dan pemeriksaan bahan import"""
    try:
        client, col = mongo.mongodb_config('DetailUMKM')
        model = {
            "_id": util.id_generator('Detail'),
            "type": "matriks_produk",
            "data": data.data
        }
        datas = col.insert_one(model)
        client.close()
        client, log_col = mongo.mongodb_config('Log')
        change = {'_id': data.id}
        newvalues = {"$set":{'status': 'matriks_produk'}}
        log_col.update_one(change, newvalues)
        newvalues = {"$set":{'matriks_produk': True}}
        log_col.update_one(change, newvalues)
        client.close()
        return response.response_detail(200, str(datas.inserted_id), resp)
    except Exception as error:
        return response.response_detail(400, error, resp)
