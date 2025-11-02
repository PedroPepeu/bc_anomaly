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

devices = [
    { "account": web3.eth.accounts[0], "deviceId": "device-001", "description": "DDoS detected!" },
    { "account": web3.eth.accounts[1], "deviceId": "device-002", "description": "Malware detected!" },
    { "account": web3.eth.accounts[2], "deviceId": "device-003", "description": "Unauthorized login attempt!" }
]

for d in devices:
    tx = contract.functions.reportAnomaly(d["deviceId"], d["description"]).transact({'from': d["account"]})
    web3.eth.wait_for_transaction_receipt(tx)
    print(f"Event from {d['deviceId']} registered in the blockchain.")
