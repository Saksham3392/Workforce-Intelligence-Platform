import pandas as pd
from collections import Counter
from app.utils.config import PROCESSED_DATA_DIR

def get_organization_skill_gaps():
    df_emp = pd.read_csv(PROCESSED_DATA_DIR / "employee_intelligence.csv")
    
    all_gaps = []
    for gaps in df_emp["Skill_Gap"].dropna():
        if gaps != "None (Proficient)":
            for s in gaps.split(", "):
                all_gaps.append(s)

    counts = Counter(all_gaps)
    result = []
    for skill, count in counts.most_common(15):
        if count >= 100:
            severity = "HIGH"
        elif count >= 50:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        result.append({
            "skill": skill,
            "employees_missing": count,
            "severity": severity
        })
    return result

def get_employee_skill_profile(employee_id: int):
    df_emp = pd.read_csv(PROCESSED_DATA_DIR / "employee_intelligence.csv")
    df_skills = pd.read_csv(PROCESSED_DATA_DIR / "employee_skills.csv")
    
    emp_record = df_emp[df_emp["Employee_ID"] == employee_id]
    if emp_record.empty:
        return None
    
    row = emp_record.iloc[0].to_dict()
    current_skills = df_skills[df_skills["EmployeeID"] == employee_id]["Skill"].tolist()
    
    row["CurrentSkills"] = current_skills
    return row
