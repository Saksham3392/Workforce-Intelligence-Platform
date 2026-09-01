import pytest
from pydantic import ValidationError
from app.validation.employee_schema import EmployeePredictionInput

def test_valid_employee_input():
    valid_data = {
        "EmployeeID": 101,
        "Age": 32,
        "Department": "IT",
        "JobRole": "Software Engineer",
        "Gender": "Female",
        "EducationLevel": 3,
        "MonthlySalary": 85000.0,
        "OvertimeHoursPerMonth": 15.0,
        "LeavesTaken": 6,
        "ProjectsHandled": 5,
        "TrainingHours": 24,
        "YearsAtCompany": 4,
        "LastPromotionYear": 2023,
        "WorkLifeBalanceScore": 3.4,
        "PerformanceRating": 4
    }
    model = EmployeePredictionInput(**valid_data)
    assert model.EmployeeID == 101
    assert model.MonthlySalary == 85000.0

def test_invalid_age_raises_validation_error():
    invalid_data = {
        "EmployeeID": 102,
        "Age": 15,  # below minimum age 18
        "Department": "IT",
        "JobRole": "Developer",
        "MonthlySalary": 70000.0
    }
    with pytest.raises(ValidationError):
        EmployeePredictionInput(**invalid_data)

def test_negative_salary_raises_validation_error():
    invalid_data = {
        "EmployeeID": 103,
        "Age": 30,
        "Department": "Sales",
        "JobRole": "Sales Executive",
        "MonthlySalary": -500.0
    }
    with pytest.raises(ValidationError):
        EmployeePredictionInput(**invalid_data)
