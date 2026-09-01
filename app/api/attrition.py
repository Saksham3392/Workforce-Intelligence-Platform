from fastapi import APIRouter, HTTPException
from app.validation.employee_schema import EmployeePredictionInput, PredictionResponse
from app.ml.predictor import predict_employee_attrition
from app.services.attrition_service import get_attrition_by_department

router = APIRouter(prefix="/predict", tags=["Attrition Prediction"])

@router.post("/attrition", response_model=PredictionResponse)
def predict_attrition(payload: EmployeePredictionInput):
    try:
        return predict_employee_attrition(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
