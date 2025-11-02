from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

with open('build/contracts/AnomalyEvent.json') as f:
    contract_json = json.load(f)

abi = contract_json['abi']

contract_address = "0x33cdec3fE336c9Aa5918d52bBEfC1551a02CbA61"

contract = web3.eth.contract(address=contract_address, abi=abi)

account = web3.eth.accounts[0]

tx = contract.functions.reportAnomaly("device-xyz", "Attack detected!").transact({'from': account})
web3.eth.wait_for_transaction_receipt(tx)

print("Anomaly event registered in the blockchain")
