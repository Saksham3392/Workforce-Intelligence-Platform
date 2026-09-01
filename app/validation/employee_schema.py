from pydantic import BaseModel, Field
from typing import Optional, List

class EmployeePredictionInput(BaseModel):
    EmployeeID: int = Field(..., example=101, description="Unique Employee ID")
    Age: int = Field(..., ge=18, le=100, example=34)
    Department: str = Field(..., example="IT")
    JobRole: str = Field(..., example="Data Analyst")
    Gender: str = Field(default="Female", example="Female")
    EducationLevel: int = Field(default=3, ge=1, le=5, example=3)
    MonthlySalary: float = Field(..., ge=10000, le=500000, example=75000)
    OvertimeHoursPerMonth: float = Field(default=10.0, ge=0, le=100, example=15.0)
    LeavesTaken: int = Field(default=5, ge=0, le=60, example=8)
    ProjectsHandled: int = Field(default=4, ge=0, le=50, example=6)
    TrainingHours: int = Field(default=20, ge=0, le=200, example=35)
    YearsAtCompany: int = Field(default=4, ge=0, le=50, example=4)
    LastPromotionYear: int = Field(default=2023, ge=2000, le=2026, example=2023)
    WorkLifeBalanceScore: float = Field(default=3.5, ge=0.0, le=5.0, example=3.2)
    PerformanceRating: int = Field(default=3, ge=1, le=5, example=4)

class TopDriver(BaseModel):
    feature: str
    impact: float

class PredictionResponse(BaseModel):
    EmployeeID: int
    AttritionProbability: float
    RiskLevel: str
    TopRiskDrivers: List[TopDriver]
    ModelVersion: str
