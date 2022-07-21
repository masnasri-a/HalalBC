""" Generate docx routing """

import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from utils.word import soal_evaluasi_docx
from config import mongo
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


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
        print(docx_result)
        client.close()
        return FileResponse(path=docx_result, filename="coba.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=error)
    