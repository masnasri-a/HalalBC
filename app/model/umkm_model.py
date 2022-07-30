""" Auth Model Pages """

# pylint: disable=no-name-in-module
from typing import List, Union
from pydantic import BaseModel


class InitUMKM(BaseModel):
    """ init """
    creator_id: str


class UmkmDetail(BaseModel):
    """ umkm detail info """
    id: str
    nama_ketua: str
    no_telp_ketua: str
    no_ktp_ketua: str
    nama_penanggungjawab: str
    logo_perusahaan: str
    ttd_penanggungjawab: str
    ttd_ketua: str


class ManagementHalahTeam(BaseModel):
    """ docx page 4 """
    id_report: str
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
    id: str
    tanggal_pelaksanaan: int
    pemateri: str
    data: list


class InputJawabanEvaluasi(BaseModel):
    id: str
    created_at: int
    tanggal: int
    nama: str
    data: dict


class JawabanAuditInternal(BaseModel):
    id: str
    created_at: int
    auditee: str
    nama_auditor: str
    bagian_diaudit: str
    data: list


class DaftarHadirKaji(BaseModel):
    """ daftar hadir kaji class """
    id: str
    tanggal: str
    list_orang: list
    pembahasan: list


class Lampiran(BaseModel):
    'lampiran'
    id: str

class DataPemeriksaan(BaseModel):
    Tanggal:str
    nama_dan_merk:str
    nama_dan_negara:str
    halal:str
    exp_bahan:str
    paraf:str

class Pemeriksaan(BaseModel):
    id: str
    data: List[DataPemeriksaan]

class DataStokBarang(BaseModel):
    tanggal_beli: str
    nama_bahan: str
    jumlah_bahan: str
    jumlah_keluar: str
    stok_sisa: str
    paraf: str

class StokBarang(BaseModel):
    """
    /form_stok_barang
    """
    id: str
    data: List[DataStokBarang]

class DataFormProduksi(BaseModel):
    tanggal_produksi: str
    nama_produk: str
    jumlah_awal: str
    jumlah_produk_keluar: str
    sisa_stok: str
    paraf: str

class FormProduksi(BaseModel):
    """
    /form_produksi
    """
    id: str
    data: List[DataFormProduksi]

class DataFormPemusnahan(BaseModel):
    """ data form pemusnhanan """
    tanggal_produksi: int
    tanggal_pemusnahan: int
    nama_produk:str
    jumlah:str
    penyebab:str
    penanggungjawab:str

class FormPemusnahan(BaseModel):
    """ form pemusnahan barang"""
    id: str
    data: List[DataFormPemusnahan]

class DataFormPengecekanKebersihan(BaseModel):
    tanggal: str
    produksi: bool
    gudang: bool
    mesin: bool
    kendaraan: bool
    penanggungjawab: str

class FormPengecekanKebersihan(BaseModel):
    id: str
    data: List[DataFormPengecekanKebersihan]

class DataDaftarBarangHalal(BaseModel):
    """ data barang halal """
    nama_merk: str
    nama_negara: str
    pemasok: str
    penerbit: str
    nomor: Union[str, int]
    masa_berlaku: str
    dokumen_lain: str
    keterangan: str

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
    id: str
    data: List[DataDaftarBarangHalal]


class DataMatrixProduksi(BaseModel):
    nama_bahan: str
    barang_1: str
    barang_2: str
    lainnya: str


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
    id: str
    data: List[DataMatrixProduksi]
