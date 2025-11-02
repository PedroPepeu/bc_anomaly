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

events_count = contract.functions.getEventsCount().call()
print(f"Total events registered: {events_count}")

for i in range(events_count):
    ts, device_id, description = contract.functions.getEvent(i).call()
    print(f"Evento {i}:")
    print(f"    Timestamp: {ts}")
    print(f"    Device: {device_id}")
    print(f"    Description: {description}\n")
