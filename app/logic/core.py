from config import mongo


class Core():

    def inset_register(_id):
        client, col = mongo.mongodb_config('Core')
        col.insert_one({
            {
                "_id": _id,
                "status_registration": False,
                "status_check_by_BPJPH": False,
                "desc_check_by_BPJPH": "",
                "desc_result": "",
                "LPH_appointment": {
                    "BPJPH_id":None,
                    "LPH_id":None
                },
                "LPH_Checking_data_status":"",
                "LPH_Checking_data_desc":"",
                "status_LPH_check_field": False,
                "LPH_review_status":"",
                "LPH_to_MUI": "",
                "status_checked_MUI": False,
                "MUI_decicion_result": "",
                "Certificate_status": False,
                "Certificate_data": "",
                "QR_data": ""
            }
        })
        client.close()
