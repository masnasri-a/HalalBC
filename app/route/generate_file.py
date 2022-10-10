""" Generate docx routing """

import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from utils.word import sjh_full_ver, bukti_pelaksanan_docx, audit_internal_docx, data_hadir_kaji_ulang_docx, form_pembelian_pemeriksaan_bahan_docx, form_produksi_docx, form_stok_bahan_docx, form_pemusnahan_barang_docx, form_pengecheckan_kebersihan_docx, daftar_bahan_halal_docx, matrik_produk_docx, surat_pernyataan_daftar_alamat_docx
from config import mongo
# from docx import Document
# from docx.enum.text import WD_ALIGN_PARAGRAPH
# from docx.shared import Pt

app = APIRouter()

@app.get("/generate_sjh", response_class=FileResponse)
def generate_sjh(doc_id: str):
    """
        Generate soal dan jawaban data evaluasi
    """
    try:
        client, col = mongo.mongodb_config('DocumentDetails')
        client_acc, col_acc = mongo.mongodb_config('Accounts')
        client_sign, col_sign = mongo.mongodb_config('UtilData')
        document_detail = col.find_one({"_id": doc_id})
        sign = col_sign.find_one({"type_id": document_detail['creator']})
        acc = col_acc.find_one({"_id": document_detail['creator']})
        docx_result = sjh_full_ver(document_detail, acc, sign)
        
        client.close()
        client_acc.close()
        client_sign.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
