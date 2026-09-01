import json
import joblib
from app.utils.config import MODEL_PATH, METADATA_PATH
from app.utils.logger import logger

class ModelManager:
    _instance = None
    _pipeline = None
    _metadata = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        if cls._instance._pipeline is None or cls._instance._metadata is None:
            cls._instance._load()
        return cls._instance

    def _load(self):
        logger.info(f"Loading ML Model Pipeline from {MODEL_PATH}")
        self._pipeline = joblib.load(MODEL_PATH)
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self._metadata = json.load(f)
        logger.info(f"Model v{self._metadata.get('version', '1.0')} successfully initialized.")

    @property
    def pipeline(self):
        if self._pipeline is None:
            self._load()
        return self._pipeline

    @property
    def metadata(self):
        if self._metadata is None:
            self._load()
        return self._metadata
