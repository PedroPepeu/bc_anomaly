from web3 import Web3
import json
from dotenv import load_dotenv
import os

load_dotenv()

ganache_url = os.getenv("GANACHE_URL")
contract_address = os.getenv("CONTRACT_ADDRESS")
web3 = Web3(Web3.HTTPProvider(ganache_url))

with open('build/contracts/AnomalyEvent.json') as f:
    contract_json = json.load(f)
abi = contract_json['abi']
contract = web3.eth.contract(address=contract_address, abi=abi)

def send_anomaly_to_blockchain(device_account, device_id, description):
    tx = contract.functions.reportAnomaly(device_id, description).transact({'from': device_account})
    web3.eth.wait_for_transaction_receipt(tx)
    print(f"Event from {device_id} registered in the blockchain.")
