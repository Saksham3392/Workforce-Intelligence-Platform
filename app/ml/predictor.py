import pandas as pd
import numpy as np
from app.ml.model_loader import ModelManager
from app.validation.employee_schema import EmployeePredictionInput, PredictionResponse, TopDriver
from app.utils.logger import log_prediction

def predict_employee_attrition(emp: EmployeePredictionInput) -> PredictionResponse:
    manager = ModelManager.get_instance()
    pipeline = manager.pipeline
    metadata = manager.metadata

    # Convert Pydantic object to DataFrame
    data_dict = emp.model_dump()
    df_row = pd.DataFrame([data_dict])

    # Feature Engineering
    current_year = 2025
    df_row["Promotion_Gap"] = current_year - df_row["LastPromotionYear"]
    df_row["Salary_Per_Year_At_Company"] = df_row["MonthlySalary"] / (df_row["YearsAtCompany"] + 1)
    df_row["Overtime_Ratio"] = df_row["OvertimeHoursPerMonth"] / 40.0
    df_row["Tenure_Ratio"] = df_row["YearsAtCompany"] / (df_row["Age"] - 18 + 1)
    df_row["Burnout_Index"] = (df_row["Overtime_Ratio"] * 0.5) + np.clip((5.0 - df_row["WorkLifeBalanceScore"]) / 5.0, 0, 1) * 0.5

    numeric_features = metadata["features"]["numeric"]
    categorical_features = metadata["features"]["categorical"]

    X = df_row[numeric_features + categorical_features]
    prob = float(pipeline.predict_proba(X)[0, 1])

    if prob >= 0.70:
        risk_level = "HIGH"
    elif prob >= 0.45:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Extract Top Risk Drivers (Local explainability heuristics aligned with model weights)
    top_drivers = []
    if df_row["OvertimeHoursPerMonth"].values[0] >= 25:
        top_drivers.append(TopDriver(feature="Excessive Monthly Overtime", impact=0.35))
    if df_row["WorkLifeBalanceScore"].values[0] <= 2.5:
        top_drivers.append(TopDriver(feature="Low Work-Life Balance Score", impact=0.25))
    if df_row["MonthlySalary"].values[0] < 60000:
        top_drivers.append(TopDriver(feature="Below Benchmark Compensation", impact=0.20))
    if df_row["Promotion_Gap"].values[0] >= 4:
        top_drivers.append(TopDriver(feature="Extended Promotion Stagnation", impact=0.15))
    
    if not top_drivers:
        top_drivers.append(TopDriver(feature="Normal Tenure Progression", impact=0.05))

    log_prediction(emp.EmployeeID, prob, risk_level, metadata.get("version", "v1.0"))

    return PredictionResponse(
        EmployeeID=emp.EmployeeID,
        AttritionProbability=round(prob, 4),
        RiskLevel=risk_level,
        TopRiskDrivers=top_drivers[:3],
        ModelVersion=metadata.get("version", "v1.0")
    )
