from pydantic import BaseModel

class Registration(BaseModel):
    creator_id:str

class BPJPH_Check(BaseModel):
    umkm_id:str
    BPJPH_id:str
    result:str
    description:str