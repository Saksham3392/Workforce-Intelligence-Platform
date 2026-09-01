from pydantic import BaseModel, Field
from typing import Optional

class EngagementRecord(BaseModel):
    EmployeeID: int
    EngagementScore: float = Field(..., ge=0, le=100)
    KPI_Score: float
    Attendance_Percent: float
    PeerRating: float
    ManagerFeedback: float
