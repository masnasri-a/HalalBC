""" Auth Model Pages """

# pylint: disable=no-name-in-module
from pydantic import BaseModel

class InitUMKM(BaseModel):
    """ init """
    creator_id:str

class UmkmDetail(BaseModel):
    """ umkm detail info """
    id: str
    nama_ketua: str
    nama_penanggungjawab: str
    logo_perusahaan: str
    ttd_penanggungjawab: str
    ttd_ketua: str


class ManagementHalahTeam(BaseModel):
    """ docx page 4 """
    id_report:str
    ketua: str = """1. Bertanggungjawab dalam sosialisasi kebijakan halal
2.	Bertanggungjawab dalam penunjukkan tim manajemen halal
3.	Bertanggungjawab dalam pelatihan eksternal/internal 
4.	Bertanggungjawab dalam audit internal dan pengiriman laporan berkala ke LPPOM MUI
5.	Mengkoordinasikan kaji ulang manajemen
"""
    pembelian: str = """1. Bertanggungjawab dalam proses seleksi bahan baru
2.	Bertanggungjawab dalam proses pembelian bahan baku
3.	Membuat dan memperbaharui Daftar Bahan Halal serta memonitoring masa berlaku dokumen bahan
4.	Bertanggungjawab dalam proses pemeriksaan kedatangan bahan
"""
    produksi: str = """1. Bertanggungjawab dalam proses produksi halal
2.	Bertanggungjawab dalam proses pengembangan produk  
3.	Bertanggungjawab dalam proses pencucian fasilitas produksi 
4.	Bertanggungjawab dalam pengananan produk yang tidak memenuhi kriteria (jika terjadi)  
"""
    pemyimpanan: str = """1. Bertanggungjawab dalam proses penyimpanan bahan dan produk jadi
2.	Bertanggungjawab dalam proses transportasi bahan dan produk jadi 
"""

class Pelaksanaan(BaseModel):
    """ docx page 13 """
    id:str
    tanggal_pelaksanaan:int
    pemateri:str
    data:dict
    

class DaftarHadirKaji(BaseModel):
    """ daftar hadir kaji class """
    id: str
    tanggal: str
    list_orang: dict
    pembahasan: dict
