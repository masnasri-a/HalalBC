
import traceback
from fastapi import APIRouter, UploadFile, File, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from utils import response
import aiofiles
app = APIRouter()


@app.post('/upload_files', status_code=200)
async def upload(resp: Response,image: UploadFile = File(...)):
    """ a function for insert images """
    try:
        destination_file_path = 'app/assets/'+image.filename
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await image.read(1024):
                await out_file.write(content)
        return response.response_detail(200, image.filename, resp)
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(400, "Failed Insert Images") from error

@app.get('/load_image')
async def load_image(image_name:str):
    try:
        return FileResponse('app/assets/'+image_name)
    except Exception as error:
        raise HTTPException(400, "Error load image") from error
