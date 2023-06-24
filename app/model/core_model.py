from typing import List, Optional
from pydantic import BaseModel, Field, validator
from config import mongo


class Registration(BaseModel):
    creator_id:str
    prev_id:Optional[str] = ""

class BPJPH_Check(BaseModel):
    umkm_id:str
    BPJPH_id:str
    result:str = Field(..., example = "Data sudah sesuai semua")
    description:str

class Appointment(BaseModel):
    bpjphh_id:str
    lph_id:str
    umkm_id:str

class LPHCheckingData(BaseModel):
    umkm_id:str
    lph_id:str
    status:str = Field(..., example="Approved / review")
    description:str = Field(..., example="Harus dilakukan Peninjauan karena .....")

class ReviewBussinessPlace(BaseModel):
    umkm_id:str
    lph_id:str
    description:str = Field(..., example="Data yang diberikan tidak sesuai hasil cek lapangan")
    status:str = Field(..., example="Approved / Decline")

class MUIGetData(BaseModel):
    umkm_id:str
    # lph_id:str
    # description:str = Field(..., example="Data yang diberikan tidak sesuai hasil cek lapangan")
    # status:str = Field(..., example="Approved / Decline")

class MUICheckingData(BaseModel):
    umkm_id:str
    mui_id:str
    status:str = Field(..., example="Approved / Decline")
    description:str = Field(..., example="Data sudah sesuai")

class UploadCertificate(BaseModel):
    umkm_id:str
    cert_id:str
    expire:int
    status:str


class ReviewUMKM(BaseModel):
    umkm_id:str
    consumen_id:str
    point:int = Field(..., example=5)
    review:str = Field(..., example="Ternyata ada minyak babi yang dipakai")

    @validator('umkm_id',allow_reuse=True)
    def umkm(cls, value):
        client, col = mongo.mongodb_config('Accounts')
        data = col.find_one({'_id':value})
        client.close()
        if data is not None:
            del data['password']
            return data
        else:
            raise ValueError('umkm id is not found')

    @validator('consumen_id', allow_reuse=True)
    def consumen(cls, value):
        client, col = mongo.mongodb_config('Accounts')
        data = col.find_one({'_id':value})
        client.close()
        if data is not None:
            del data['password']
            return data
        else:
            raise ValueError('consumen id is not found')

class Pelaporan(BaseModel):
    image:str
    description:str
    umkm_name:str
    address:str
    user_name:str