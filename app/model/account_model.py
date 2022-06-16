""" pages for account model """

from typing import Optional
# pylint: disable=no-name-in-module
from pydantic import BaseModel

class DataPassword(BaseModel):
    
    id: str
    password: str
    new_password: str

class DataAuditor(BaseModel):
    id: str
    no_ktp: str
    name: str
    religion: Optional[str]
    address: Optional[str]
    institution: Optional[str]
    competence: Optional[str]
    experience: Optional[str]
    cert_competence: Optional[str]
    experied_cert: Optional[int]
    auditor_experience: Optional[str]

class DataUMKM(BaseModel):
    id: str
    company_name: str
    company_address: Optional[str]
    company_number: Optional[str]
    factory_name: str
    factory_address: Optional[str]
    email: Optional[str]
    product_name: str
    product_type: str
    marketing_area: Optional[str]
    marketing_system: Optional[str]
    
class DataKonsumen(BaseModel):
    id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]