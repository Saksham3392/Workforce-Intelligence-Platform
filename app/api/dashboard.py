from fastapi import APIRouter, HTTPException
import pandas as pd
from app.utils.config import PROCESSED_DATA_DIR
from app.services.attrition_service import get_attrition_by_department
from app.services.skill_gap_service import get_organization_skill_gaps, get_employee_skill_profile
from app.services.recommendation_service import get_recommendations_summary

router = APIRouter(prefix="", tags=["Dashboard & Analytics"])

@router.get("/dashboard/summary")
def dashboard_summary():
    df = pd.read_csv(PROCESSED_DATA_DIR / "employee_intelligence.csv")
    total_employees = len(df)
    high_risk_count = int((df["Risk"] == "HIGH").sum())
    avg_engagement = round(float(df["Engagement"].mean()), 1)
    
    return {
        "total_employees": total_employees,
        "high_risk_employees": high_risk_count,
        "average_engagement": avg_engagement,
        "high_risk_percentage": round((high_risk_count / total_employees) * 100, 1)
    }

@router.get("/dashboard/attrition-by-department")
def attrition_by_department():
    return get_attrition_by_department()

@router.get("/dashboard/skill-gaps")
def organization_skill_gaps():
    return get_organization_skill_gaps()

@router.get("/dashboard/recommendations")
def recommendations():
    return get_recommendations_summary()

@router.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    profile = get_employee_skill_profile(employee_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found.")
    return profile
