import kagglehub
import shutil
from pathlib import Path


# Download latest version
path = kagglehub.dataset_download("reihanenamdari/breast-cancer")
dataset_dir = Path(__file__).resolve().parent / "dataset"
shutil.copytree(path, dataset_dir, dirs_exist_ok=True)

print("Dataset files copied to:", dataset_dir)

