
import traceback
from fastapi import APIRouter, UploadFile, File
from fastapi.exceptions import HTTPException
import aiofiles
app = APIRouter()


@app.post('/upload_files')
async def upload(image: UploadFile = File(...)):
    """ a function for insert images """
    try:
        destination_file_path = 'app/assets/'+image.filename
        print(destination_file_path)
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await image.read(1024):
                await out_file.write(content)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(400, "Failed Insert Images") from e
