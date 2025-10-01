import os
import shutil
import pandas as pd

def ensure_directories(dirs: list[str]):
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def clean_temp_files(temp_dir: str):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

def validate_csv_file(source: str) -> tuple[bool, str, pd.DataFrame | None]:
    try:
        df = pd.read_csv(source)
        if df.empty:
            return False, "Dataset vazio.", None
        return True, "Válido.", df
    except Exception as e:
        return False, f"Erro: {str(e)}", None