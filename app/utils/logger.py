import os
import logging
from datetime import datetime
from app.utils.config import PREDICTIONS_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-5s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("EnterpriseHR_AI")

def log_prediction(employee_id: int, probability: float, risk_level: str, model_version: str = "v1.0"):
    log_file = PREDICTIONS_DIR / "prediction_audit.csv"
    file_exists = log_file.exists()
    
    with open(log_file, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("timestamp,employee_id,probability,risk_level,model_version\n")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp},{employee_id},{probability:.4f},{risk_level},{model_version}\n")
    
    logger.info(f"Prediction logged -> Employee: {employee_id}, Risk: {risk_level} ({probability:.1%})")
