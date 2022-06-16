""" umkm  routing pages """

from fastapi import APIRouter
from utils import word

app = APIRouter()

# @app.post('/submission_criteria')
# def submission_criteria():
@app.get('/test_create_docx')
def create_docx():
    """ function for create docs """
    word.word_generator()

@app.post('/insert_detail_umkm')
def detail_umkm():
    pass