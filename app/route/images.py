import traceback
from fastapi import APIRouter, UploadFile, File
import aiofiles
app = APIRouter()

@app.post('/upload_files')
async def upload(image: UploadFile = File(...)):
    try:
        destination_file_path = 'app/assets/'+image.filename
        print(destination_file_path)
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await image.read(1024):
                await out_file.write(content)
    except:
        traceback.print_exc()