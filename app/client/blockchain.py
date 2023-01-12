import json, time, random
import os
import traceback
from web3 import Web3
from web3.exceptions import ContractLogicError

url_node = 'http://103.176.79.228:8545'


def load_abi():
    pwd = os.getcwd()
    print(pwd)
    with open(pwd+'/abi/Halal.json', 'r') as files:
        return json.load(files)

def connect_contract():
    web3 = Web3(Web3.HTTPProvider(url_node))
    contract_address = '0x45aC327bA00Ecc952F8572BD331C3Ea53C46a154'
    web3.eth.defaultAccount = web3.eth.accounts[0]
    print(web3.eth.get_balance('0x45aC327bA00Ecc952F8572BD331C3Ea53C46a154'))

    abi = load_abi()['abi']
    if contract_address == None:
        bytecode = load_abi()['bytecode']
        contracts = web3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = contracts.constructor().transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        func_contract = web3.eth.contract(
            address=web3.toChecksumAddress(contract_address), abi=abi)
    else:
        func_contract = web3.eth.contract(
            address=web3.toChecksumAddress(contract_address), abi=abi)
    
    return web3, func_contract


def add_account(umkm_id, name, role):
    try:
        web3, client = connect_contract()
        tx_add_account = client.functions.add_account(
            umkm_id, name,role
        ).transact()
        tx = web3.eth.waitForTransactionReceipt(tx_add_account)
        print(tx)
        return "add account success"
    except:
        traceback.print_exc()

def get_account(umkm_id):
    try:
        _, client = connect_contract()
        get_account = client.functions.get_account(umkm_id).call()
        return get_account
    except ContractLogicError as error:
        traceback.print_exc()
        print("error = "+error)

def add_transaction(transaction_id:str, user_id:str, data:bytes):
    try:
        web3, client = connect_contract()
        add_tx = client.functions.add_transaction(
            transaction_id,
            user_id,
            data
        ).transact()
        web3.eth.waitForTransactionReceipt(add_tx)
        return add_tx.hex()
    except:
        traceback.print_exc()

def get_transaction(transaction_id):
    try:
        _, client = connect_contract()
        get_tx = client.functions.get_transaction(transaction_id).call()
        return get_tx
    except:
        traceback.print_exc()

def add_cert(umkm_id:str, cert_id:str, expired_at:int):
    try:
        web3, client = connect_contract()
        add_transaction = client.functions.add_certificate(
            umkm_id,
            cert_id,
            expired_at
        ).transact()
        web3.eth.waitForTransactionReceipt(add_transaction)
        return add_transaction.hex()
    except:
        traceback.print_exc()    

def get_cert(umkm_id):
    try:
        _, client = connect_contract()
        get_tx = client.functions.get_certificate(umkm_id).call()
        return get_tx
    except:
        traceback.print_exc()


if __name__ == "__main__":
    web3, client = connect_contract()
    
    # adder = add_account("UMKM:08", "new2s", "umkm")
    # print(adder)

    # get_acc = get_account("UMKM:08")
    # print(get_acc)
    while True:
        test_data = {
            "name":"nasri",
            "role":"umkm"
        }
        data = json.dumps(test_data)
        
        add_tx = add_transaction("TX", "UMKM:02", data)
        print(add_tx)
        time.sleep(random.randint(3,60))
    # get_tx = get_transaction("TX")
    # print(get_tx)

    # set_cert = add_cert("UMKM:02", "masnasri", 1621312312312)
    # print(set_cert)

    # get_cer = get_cert("UMKM:02")
    # print(get_cer)