from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_dashboard_summary_endpoint():
    response = client.get("/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_employees"] == 2500
    assert data["high_risk_employees"] > 0
    assert "average_engagement" in data

def test_predict_attrition_api():
    payload = {
        "EmployeeID": 501,
        "Age": 45,
        "Department": "IT",
        "JobRole": "Developer",
        "Gender": "Male",
        "EducationLevel": 4,
        "MonthlySalary": 95000.0,
        "OvertimeHoursPerMonth": 5.0,
        "LeavesTaken": 3,
        "ProjectsHandled": 5,
        "TrainingHours": 40,
        "YearsAtCompany": 8,
        "LastPromotionYear": 2024,
        "WorkLifeBalanceScore": 4.5,
        "PerformanceRating": 4
    }
    response = client.post("/predict/attrition", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["EmployeeID"] == 501
    assert 0.0 <= res["AttritionProbability"] <= 1.0
    assert res["RiskLevel"] == "LOW"

def test_employee_detail_endpoint():
    response = client.get("/employees/101")
    assert response.status_code == 200
    assert response.json()["Employee_ID"] == 101

def test_employee_not_found_returns_404():
    response = client.get("/employees/999999")
    assert response.status_code == 404
