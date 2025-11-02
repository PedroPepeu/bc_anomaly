import joblib
import pandas as pd
import numpy as np
from register_anomaly import send_anomaly_to_blockchain, web3

model = joblib.load('model/iforest_nslkdd_model.joblib')
scaler = joblib.load('model/data_scaler_nslkdd.joblib')

new_data = np.zeros(scaler.n_features_in_)

scaled_data = scaler.transform([new_data])

result = model.predict(scaled_data)[0]
if result == -1:
    device_id = "device-001"
    description = "Real-time anomaly detected in device-001"
    device_account = web3.eth.accounts[0]
    send_anomaly_to_blockchain(device_account, device_id, description)
else:
    print("no anomaly detected, nothing registered")
