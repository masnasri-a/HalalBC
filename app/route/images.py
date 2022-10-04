
import traceback
from fastapi import APIRouter, UploadFile, File, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
import requests
from config import mongo
from model import util_model
from utils import response, util
import aiofiles
app = APIRouter()


@app.post('/upload_files', status_code=200)
async def upload(resp: Response,image: UploadFile = File(...)):
    """ a function for insert images """
    try:
        type_file = image.content_type
        new_file_name = util.sha256(str(image.filename)+str(util.get_created_at()))
        destination_file_path = 'app/assets/'+new_file_name+'.'+type_file.split('/')[-1]
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await image.read(1024):
                await out_file.write(content)
            url = 'http://103.13.206.148:5001/api/v0/add/'
            files = {'media': open(destination_file_path, 'rb')}
            res = requests.post(url, files=files)
            print(res.json()['Hash'])
        return response.response_detail(200, new_file_name+'.'+type_file.split('/')[-1], resp)
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Insert Images") from error

@app.get('/load_image')
async def load_image(image_name:str):
    """ load images data """
    try:
        return FileResponse('app/assets/'+image_name)
    except Exception as error:
        raise HTTPException(400, "Error load image") from error

@app.post('/input_signature')
def input_signature(model : util_model.SignatureModel, resp : Response):
    try:
        _id = util.id_generator('SIGN')
        model_data = model.dict()
        model_data['_id'] = _id
        client, util_col = mongo.mongodb_config('UtilData')
        util_col.insert_one(model_data)
        client.close()
        return response.response_detail(200, "insert signature success", resp)
    except Exception as error:
        traceback.print_exc()
        return response.response_detail(400, "Error Insert Signature", resp)

@app.get('/load_signature')
def load_signature(resp: Response, types:str = "UMKM", type_id:str = "UMKM:482171681413"):
    try:
        client, util_col = mongo.mongodb_config('UtilData')
        list_data = util_col.find({'$and':[{'types':types},{'type_id':type_id}]})
        model_return = []
        for data in list_data:
            model_return.append({
                "id":data['_id'],
                "name":data['name'],
                "title":data['title'],
                "sign":data['sign']
            })
        client.close()
        return response.response_detail(200, model_return, resp)
    except Exception as error:
        print(error)
        traceback.print_exc()
        return response.response_detail(400, "Signatre Not Found" ,resp)

