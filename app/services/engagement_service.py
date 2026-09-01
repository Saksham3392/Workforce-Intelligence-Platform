import pandas as pd
from app.utils.config import PROCESSED_DATA_DIR

def get_engagement_overview():
    df = pd.read_csv(PROCESSED_DATA_DIR / "employee_intelligence.csv")
    return {
        "overall_average": round(float(df["Engagement"].mean()), 1),
        "department_averages": df.groupby("Dept")["Engagement"].mean().round(1).to_dict(),
        "disengaged_employees_count": int((df["Engagement"] < 60).sum())
    }
