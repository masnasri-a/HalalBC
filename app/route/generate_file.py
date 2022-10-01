""" Generate docx routing """

import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from utils.word import soal_evaluasi_docx, bukti_pelaksanan_docx, audit_internal_docx, data_hadir_kaji_ulang_docx, form_pembelian_pemeriksaan_bahan_docx, form_produksi_docx, form_stok_bahan_docx, form_pemusnahan_barang_docx, form_pengecheckan_kebersihan_docx, daftar_bahan_halal_docx, matrik_produk_docx, surat_pernyataan_daftar_alamat_docx
from config import mongo
# from docx import Document
# from docx.enum.text import WD_ALIGN_PARAGRAPH
# from docx.shared import Pt

app = APIRouter()

@app.get("/soal_evaluasi", response_class=FileResponse)
def soal_evaluasi(doc_id: str):
    """
        Generate soal dan jawaban data evaluasi
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        jawaban = col.find_one({"_id": doc_id}, {"jawaban_evaluasi": 1})['jawaban_evaluasi']
        print(jawaban)
        docx_result = soal_evaluasi_docx(jawaban)
        client.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)

@app.get("/soal_evaluasi", response_class=FileResponse)
def soal_evaluasi(doc_id: str):
    """
        Generate soal dan jawaban data evaluasi
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        jawaban = col.find_one({"_id": doc_id}, {"jawaban_evaluasi": 1})['jawaban_evaluasi']
        docx_result = soal_evaluasi_docx(jawaban)
        client.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
@app.get("/bukti_pelaksanaan", response_class=FileResponse)
def bukti_pelaksanaan(doc_id: str):
    """
        Generate Bukti pelaksanaan Pelatihan internal
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        client_sign, col_sign = mongo.mongodb_config('UtilData')
        bukti = col.find_one({"_id": doc_id}, {"bukti_pelaksanaan": 1,  'creator': 1})
        sign = col_sign.find_one({"type_id": bukti['creator']})
        docx_result = bukti_pelaksanan_docx(bukti['bukti_pelaksanaan'], sign)
        client.close()
        client_sign.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)

@app.get("/audit_internal", response_class=FileResponse)
def audit_internal(doc_id: str):
    """
        Generate Audit Internal
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        client_sign, col_sign = mongo.mongodb_config('UtilData')
        bukti = col.find_one({"_id": doc_id}, {"jawaban_audit": 1,  'creator': 1})
        sign = col_sign.find_one({"type_id": bukti['creator']})
        docx_result = audit_internal_docx(bukti['jawaban_audit'], sign)
        client.close()
        client_sign.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
    
@app.get("/data_hadir_kaji_ulang", response_class=FileResponse)
def data_hadir_kaji_ulang(doc_id: str):
    """
        Generate Daftar Hadir Kaji Ulang Managements
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        client_sign, col_sign = mongo.mongodb_config('UtilData')
        bukti = col.find_one({"_id": doc_id}, {"daftar_hasil_kaji": 1,  'creator': 1})
        sign = col_sign.find_one({"type_id": bukti['creator']})
        docx_result = data_hadir_kaji_ulang_docx(bukti['daftar_hasil_kaji'], sign)
        client.close()
        client_sign.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
    
@app.get("/surat_pernyataan_daftar_alamat", response_class=FileResponse)
def surat_pernyataan_daftar_alamat():
    """
        Generate Surat Pernyataan Daftar Alamat Fasilitas Produksi Dan Bebas Dari Babi dan Turunannya
    """
    try:
        docx_result = surat_pernyataan_daftar_alamat_docx()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
    
@app.get("/form_pembelian_pemeriksaan_bahan", response_class=FileResponse)
def form_pembelian_pemeriksaan_bahan(doc_id: str):
    """
        Generate Form Pembelian dan Pemeriksaan bahan
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        bukti = col.find_one({"_id": doc_id}, {"pembelian_import": 1,  'pembelian': 1})
        docx_result = form_pembelian_pemeriksaan_bahan_docx(bukti['pembelian'], bukti['pembelian_import'])
        client.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
    
@app.get("/form_stok_bahan", response_class=FileResponse)
def form_stok_bahan(doc_id: str):
    """
        Generate Form Stok Bahan
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        bukti = col.find_one({"_id": doc_id}, {"stok_barang": 1})
        docx_result = form_stok_bahan_docx(bukti['stok_barang'])
        client.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
    
@app.get("/form_produksi", response_class=FileResponse)
def form_produksi(doc_id: str):
    """
        Generate Form Produksi
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        bukti = col.find_one({"_id": doc_id}, {"form_produksi": 1})
        docx_result = form_produksi_docx(bukti['form_produksi'])
        client.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
    
@app.get("/form_pemusnahan_barang", response_class=FileResponse)
def form_pemusnahan_barang(doc_id: str):
    """
        Generate Form Pemusnahan barang / produk
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        bukti = col.find_one({"_id": doc_id}, {"form_pemusnahan": 1})
        docx_result = form_pemusnahan_barang_docx(bukti['form_pemusnahan'])
        client.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
    
@app.get("/form_pengecheckan_kebersihan", response_class=FileResponse)
def form_pengecheckan_kebersihan(doc_id: str):
    """
        Generate Form Pengecheckan Kebersihan Fasilitas Produksi dan Kendaraan
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        bukti = col.find_one({"_id": doc_id}, {"form_pengecekan_kebersihan": 1})
        docx_result = form_pengecheckan_kebersihan_docx(bukti['form_pengecekan_kebersihan'])
        client.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
    
@app.get("/daftar_bahan_halal", response_class=FileResponse)
def daftar_bahan_halal(doc_id: str):
    """
        Generate Daftar Bahan Halal
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        client_acc, col_acc = mongo.mongodb_config('Accounts')
        client_sign, col_sign = mongo.mongodb_config('UtilData')
        bukti = col.find_one({"_id": doc_id}, {"daftar_bahan_halal": 1, "creator": 1})
        sign = col_sign.find_one({"type_id": bukti['creator']})
        acc = col_acc.find_one({"_id": bukti['creator']})
        docx_result = daftar_bahan_halal_docx(bukti['daftar_bahan_halal'], acc, sign)
        client.close()
        client_sign.close()
        client_acc.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    
    
    
@app.get("/matrik_produk", response_class=FileResponse)
def matrik_produk(doc_id: str):
    """
        Generate Matrik Produk
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        client_acc, col_acc = mongo.mongodb_config('Accounts')
        client_sign, col_sign = mongo.mongodb_config('UtilData')
        bukti = col.find_one({"_id": doc_id}, {"matriks_produk": 1, "creator": 1})
        sign = col_sign.find_one({"type_id": bukti['creator']})
        acc = col_acc.find_one({"_id": bukti['creator']})
        docx_result = matrik_produk_docx(bukti['matriks_produk'], acc, sign)
        client.close()
        client_sign.close()
        client_acc.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)