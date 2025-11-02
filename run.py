import pandas as pd
import joblib
from model.train_model import preprocess
from register_anomaly import send_anomaly_to_blockchain, web3

COLUMN_NAMES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'class', 'difficulty'
]

df_test = pd.read_csv('model/KDDTest+.txt', header=None, names=COLUMN_NAMES)

X_test, y_test = preprocess(df_test)
train_cols = joblib.load('model/train_cols.joblib')
X_test = X_test.reindex(columns=train_cols, fill_value=0)
scaler = joblib.load('model/data_scaler_nslkdd.joblib')
X_test_scaled = scaler.transform(X_test)

model = joblib.load('model/iforest_nslkdd_model.joblib')

for idx, (row, scaled_row) in enumerate(zip(df_test.iterrows(), X_test_scaled)):
    result = model.predict([scaled_row])[0]
    if result == -1:
        device_id = "device-001"
        description = f"Batch anomaly detected at index {idx}"
        device_account = web3.eth.accounts[0]
        send_anomaly_to_blockchain(device_account, device_id, description)
