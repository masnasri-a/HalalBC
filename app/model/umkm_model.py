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
    data:list

class InputJawabanEvaluasi(BaseModel):
    id:str
    created_at:int
    tanggal:int
    nama:str
    data:dict

class JawabanAuditInternal(BaseModel):
    id:str
    created_at:int
    auditee:str
    nama_auditor:str
    bagian_diaudit:str
    data:list


class DaftarHadirKaji(BaseModel):
    """ daftar hadir kaji class """
    id: str
    tanggal: str
    list_orang: list
    pembahasan: list


class Pemeriksaan(BaseModel):
    """
    /form_pembelian_pemeriksaan_import
    /form_pembelian_pemeriksaan
    [
        {
            "Tanggal":"",
            "nama_dan_merk":"",
            "nama_dan_negara":"",
            "halal":True,
            "exp_bahan":"",
            "paraf":""
        }
    ]
    """
    id: str
    data:list


class StokBarang(BaseModel):
    """
    /form_stok_barang
    [
        {
            "tanggal_beli":"",
            "nama_bahan":"",
            "jumlah_bahan":"",
            "jumlah_keluar":"",
            "stok_sisa":"",
            "paraf":""
        }
    ]
    """
    id:str
    data:list

class FormProduksi(BaseModel):
    """
    /form_produksi
    [
        {
            "tanggal_produksi":"",
            "nama_produk":"",
            "jumlah_awal":"",
            "jumlah_produk_keluar":"",
            "sisa_stok":"",
            "paraf":""
            
        }
    ]
    """
    id:str
    data:list

class FormPemusnahan(BaseModel):
    """
    /form_pemusnahan
    [
        {
            "tanggal_produksi":"",
            "nama_produk":"",
            "tanggal_produksi":"",
            "jumlah":"",
            "penyebab":"",
            "tanggal_pemusnahan":"",
            "penanggungjawab":""
        }
    ]
    """
    id:str
    data:list

class FormPengecekanKebersihan(BaseModel):
    """
    /form_pengecekan_kebersihan
    [{
        "tanggal":"",
        "produksi":True,
        "gudang":True,
        "mesin":True,
        "kendaraan":True,
        "penanggungjawab":"",
    }]
    """
    id:str
    data:list


class DaftarBarangHalal(BaseModel):
    """
    /daftar_barang_halal
    [{
        "nama_merk":"",
        "nama_negara":"",
        "pemasok":"",
        "penerbit":"",
        "nomor":"",
        "masa_berlaku":"",
        "dokumen_lain":"",
        "keterangan":""
    }]
    """
    id:str
    data:list

class MatrixProduksi(BaseModel):
    """
    /matriks_produk
    [{
        "nama_bahan":"",
        "barang_1":"",
        "barang_2":"",
        "lainnya":"",
    }]
    """
    id:str
    data:list
    