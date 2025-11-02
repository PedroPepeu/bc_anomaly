import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import time

print("Script 'Caminho Feliz' (NSL-KDD) CORRIGIDO iniciado...")

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
CATEGORICAL_FEATURES = ['protocol_type', 'service', 'flag']
LABEL_COLUMN = 'class'
NORMAL_CLASS_NAME = 'normal'

def preprocess(df):
    X = df.drop(columns=[LABEL_COLUMN, 'difficulty'])
    y_labels = df[LABEL_COLUMN]
    
    y = np.where(y_labels == NORMAL_CLASS_NAME, 1, -1)
    
    X_dummies = pd.get_dummies(X, columns=CATEGORICAL_FEATURES, dummy_na=False)
        
    return X_dummies, y

print("Carregando e processando KDDTrain+.txt...")
try:
    df_train = pd.read_csv('KDDTrain+.txt', header=None, names=COLUMN_NAMES)
except FileNotFoundError:
    print("ERRO: Arquivo 'KDDTrain+.txt' não encontrado.")
    exit()

X_train_df, y_train = preprocess(df_train)
print(f"Distribuição no Treino:\n{df_train[LABEL_COLUMN].value_counts(normalize=True)}")

print("\nCarregando e processando KDDTest+.txt...")
try:
    df_test = pd.read_csv('KDDTest+.txt', header=None, names=COLUMN_NAMES)
except FileNotFoundError:
    print("ERRO: Arquivo 'KDDTest+.txt' não encontrado.")
    exit()

X_test_df, y_test = preprocess(df_test)

print("\nAlinhando colunas de treino e teste...")

train_cols = X_train_df.columns

X_test_aligned = X_test_df.reindex(columns=train_cols, fill_value=0)

print(f"Formato Treino: {X_train_df.shape}, Formato Teste Alinhado: {X_test_aligned.shape}")
if X_train_df.shape[1] != X_test_aligned.shape[1]:
     print("ERRO: Alinhamento falhou!")
     exit()

print("Escalonando dados...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_df)
X_test_scaled = scaler.transform(X_test_aligned) 

print("\nTreinando o modelo IsolationForest...")
start_time = time.time()

contamination_rate = (y_train == -1).sum() / len(y_train)
print(f"Taxa de contaminação (anomalias) no treino: {contamination_rate:.4f}")

model = IsolationForest(
    n_estimators=100,
    contamination=contamination_rate,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled) 
print(f"Treinamento concluído em {time.time() - start_time:.2f} segundos.")

print("\nAvaliando o modelo no conjunto de TESTE...")
y_pred = model.predict(X_test_scaled) 

print("\nRelatório de Classificação (NSL-KDD):")
print(classification_report(y_test, y_pred, target_names=['Anomalia (-1)', 'Normal (1)']))
print("\nMatriz de Confusão (NSL-KDD):")
cm = confusion_matrix(y_test, y_pred)
print(cm)
print("Formato: [ [Verdadeiro Anomalia, Falso Normal], [Falso Anomalia, Verdadeiro Normal] ]")

# --- 9. SALVAR O MODELO ---
print("\nSalvando o modelo treinado...")
joblib.dump(model, 'iforest_nslkdd_model.joblib')
joblib.dump(scaler, 'data_scaler_nslkdd.joblib')
print("Modelo salvo como 'iforest_nslkdd_model.joblib'")
print("\nScript concluído!")
