from http import client
from config import mongo

class Simulasi():

    def __init__(self,creator_id, registered) -> None:
        self.creator_id = creator_id
        self.registered = registered

    def get_list_bahan(self):
        client, col = mongo.mongodb_config('BahanDetail')
        list_bahan = col.find_one({'creator_id':self.creator_id})
        client.close()
        detail_list_bahan = []
        for detail in list_bahan['list_bahan']:
            detail_list_bahan.append(detail)
        return detail_list_bahan

    def checking(bahan:dict):
        pass

    def logic(self):
        list_bahan = self.get_list_bahan()
        if not self.registered:
            for detail_bahan in list_bahan:
                if detail_bahan['halal'] is not True:
                    return {
                        "message":"Sistem belum terintegrasi halal, Bahan masih ada yang belum bersertifasi halal",
                        "data":None
                    }, False
                else :
                    return {
                        "message":"Sistem belum terintegrasi halal, Silahkan daftarkan produk anda",
                        "data":None
                    }, True
        else:
            for detail_bahan in list_bahan:
                if detail_bahan['halal'] is not True:
                    return {
                        "message":"Sistem sudah terintegrasi halal, Bahan masih ada yang belum bersertifasi halal",
                        "data":"Bahan masih ada yang belum bersertifasi halal"
                    }, False
                else :
                    return {
                        "message":"Sistem sudah terintegrasi halal, Silahkan daftarkan ulang produk anda",
                        "data":"Silahkan daftarkan ulang produk anda"
                    }, True

    def result(self):
        self.logic()