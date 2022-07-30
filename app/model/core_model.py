from pydantic import BaseModel, Field

class Registration(BaseModel):
    creator_id:str

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
    unkm_id:str
    lph_id:str
    description:str = Field(..., example="Data yang diberikan tidak sesuai hasil cek lapangan")
    status:str = Field(..., example="Approved / Decline")

class MUIGetData(BaseModel):
    umkm_id:str
    lph_id:str
    description:str = Field(..., example="Data yang diberikan tidak sesuai hasil cek lapangan")
    status:str = Field(..., example="Approved / Decline")

class MUICheckingData(BaseModel):
    umkm_id:str
    mui_id:str
    status:str = Field(..., example="Approved / Decline")
    description:str = Field(..., example="Data sudah sesuai")

class UploadCertificate(BaseModel):
    umkm_id:str
    cert_id:str