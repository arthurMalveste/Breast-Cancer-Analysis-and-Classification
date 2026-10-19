import urllib.request
from pathlib import Path

import pandas as pd

# BCSC (Breast Cancer Surveillance Consortium), espelho público no OpenML (ID 43687)
ARFF_URL = "https://openml.org/data/v1/download/22102512/Breast-cancer-prediction.arff"
dataset_dir = Path(__file__).resolve().parent / "dataset"
dataset_dir.mkdir(exist_ok=True)
arff_path = dataset_dir / "Breast-cancer-prediction.arff"
csv_path = dataset_dir / "breast_cancer_screening_bcsc.csv"

urllib.request.urlretrieve(ARFF_URL, arff_path)

# Lê o cabeçalho do ARFF para pegar os nomes das colunas e onde os dados começam
lines = arff_path.read_text(encoding="utf-8").splitlines()
columns = [l.split()[1] for l in lines if l.upper().startswith("@ATTRIBUTE")]
data_start = next(i for i, l in enumerate(lines) if l.upper().startswith("@DATA")) + 1

df = pd.read_csv(
    arff_path,
    skiprows=data_start,
    header=None,
    names=columns,
    quotechar="'",
    na_values=["Missing"],
)
df.to_csv(csv_path, index=False)
arff_path.unlink()

print(f"Dataset salvo em: {csv_path} ({df.shape[0]} linhas, {df.shape[1]} colunas)")
