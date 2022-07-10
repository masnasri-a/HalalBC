from pydantic import BaseModel, Field

class SignatureModel(BaseModel):
    """ signature input """
    name: str = Field(..., example="Faisal")
    title: str = Field(..., example="Pemimpin Perusahaan")
    sign:str = Field(..., example="default.png")
    types:str = Field(..., example="UMKM")
    type_id:str = Field(..., example="UMKM:482171681413")