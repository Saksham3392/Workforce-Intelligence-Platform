import pytest
from app.ml.model_loader import ModelManager
from app.ml.predictor import predict_employee_attrition
from app.validation.employee_schema import EmployeePredictionInput

def test_model_pipeline_loading():
    manager = ModelManager.get_instance()
    assert manager.pipeline is not None
    assert manager.metadata is not None
    assert "roc_auc" in manager.metadata["metrics"]
    assert manager.metadata["metrics"]["roc_auc"] > 0.80

def test_prediction_returns_valid_probability():
    inp = EmployeePredictionInput(
        EmployeeID=201,
        Age=29,
        Department="Sales",
        JobRole="Sales Executive",
        Gender="Male",
        EducationLevel=3,
        MonthlySalary=45000.0,
        OvertimeHoursPerMonth=35.0,
        LeavesTaken=10,
        ProjectsHandled=8,
        TrainingHours=10,
        YearsAtCompany=3,
        LastPromotionYear=2021,
        WorkLifeBalanceScore=1.5,
        PerformanceRating=2
    )
    result = predict_employee_attrition(inp)
    assert 0.0 <= result.AttritionProbability <= 1.0
    assert result.RiskLevel in ["HIGH", "MEDIUM", "LOW"]
    assert len(result.TopRiskDrivers) > 0
