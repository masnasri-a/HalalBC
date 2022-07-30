""" Auth Model Pages """

# pylint: disable=no-name-in-module
from typing import List, Union
from pydantic import BaseModel, Field

class SimulasiOne(BaseModel):
    creator_id:str = Field(..., example="UMKM:482171681413")
    keterangan:List[str]
    syarat:List[str]
    tanggal_simulasi:int

class SimulasiTwo(BaseModel):
    creator_id:str = Field(..., example="UMKM:482171681413")
    tanggal_simulasi:int