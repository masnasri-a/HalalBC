from config import mongo
import uuid

id = uuid.uuid1()


def inset_register(_id, prev_id):
    client, col = mongo.mongodb_config('Core')
    col.insert_one(
        {
            "_id": id.hex,
            "prev_id": prev_id,
            "umkm_id": _id,
            "registration": {
                "status": False,
                "date": 0
            },
            "bpjph_checked": {
                "status": False,
                "desc": "",
                "result": "",
                "date": 0
            },
            "lph_appointment": {
                "bpjph_id": "",
                "lph_id": "",
                "date": 0
            },
            "lph_checked": {
                "status": "",
                "date": 0,
                "desc": "",
                "survey_location": False,
                "review_status": "",
                "to_mui": ""
            },
            "mui": {
                "checked_status": False,
                "decision_desc": "",
                "date": 0,
                "approved": False
            },
            "certificate": {
                "created_date": 0,
                "expired_date": 0,
                "status": False,
                "data": ""
            },
            "QR_data": ""
        })
    client.close()
