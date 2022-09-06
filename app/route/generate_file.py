""" Generate docx routing """

import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from utils.word import soal_evaluasi_docx, bukti_pelaksanan_docx
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
