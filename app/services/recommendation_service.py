import pandas as pd
from app.utils.config import PROCESSED_DATA_DIR

def get_recommendations_summary(limit: int = 20):
    df_emp = pd.read_csv(PROCESSED_DATA_DIR / "employee_intelligence.csv")
    recs = df_emp[df_emp["Risk"] == "HIGH"][["Employee_ID", "Name", "Dept", "Role", "Risk", "Primary_Gap", "Recommendation"]].head(limit)
    return recs.to_dict(orient="records")

def get_all_courses():
    df_courses = pd.read_csv(PROCESSED_DATA_DIR / "courses.csv")
    return df_courses.to_dict(orient="records")
