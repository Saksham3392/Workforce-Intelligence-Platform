import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PREDICTIONS_DIR = DATA_DIR / "predictions"
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "v1" / "attrition_pipeline.joblib"
METADATA_PATH = MODELS_DIR / "v1" / "metadata.json"

PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
