
from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class DataAuditor(BaseModel):
    no_ktp: str
    name: str
    password: str
    username: str
    religion: str
    type: str
    address: str
    institution: str
    competence: str
    experience: str
    cert_competence: str
    experied_cert: int
    auditor_experience: str


class DataUMKM(BaseModel):
    username: str
    password: str
    company_name: str
    company_address: str
    company_number: str
    factory_name: str
    factory_address: str
    email: str
    product_name: str
    product_type: str
    marketing_area: str
    marketing_system: str


class DataKonsumen(BaseModel):
    username: str
    password: str
    name: str
    email: str
    phone: str
    address: str
