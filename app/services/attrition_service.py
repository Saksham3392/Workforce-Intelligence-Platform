import pandas as pd
from app.utils.config import PROCESSED_DATA_DIR

def get_attrition_by_department():
    df = pd.read_csv(PROCESSED_DATA_DIR / "employee_intelligence.csv")
    dept_stats = df.groupby("Dept").agg(
        total_employees=("Employee_ID", "count"),
        high_risk_count=("Risk", lambda x: (x == "HIGH").sum()),
        avg_attrition_prob=("Attrition_Prob", "mean"),
        avg_engagement=("Engagement", "mean")
    ).reset_index()

    dept_stats["high_risk_percentage"] = (
        (dept_stats["high_risk_count"] / dept_stats["total_employees"]) * 100
    ).round(1)
    dept_stats["avg_attrition_prob"] = (dept_stats["avg_attrition_prob"] * 100).round(1)
    dept_stats["avg_engagement"] = dept_stats["avg_engagement"].round(1)

    return dept_stats.to_dict(orient="records")
