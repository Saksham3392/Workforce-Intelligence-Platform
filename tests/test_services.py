from app.services.attrition_service import get_attrition_by_department
from app.services.skill_gap_service import get_organization_skill_gaps, get_employee_skill_profile
from app.services.recommendation_service import get_recommendations_summary, get_all_courses

def test_attrition_by_department_structure():
    depts = get_attrition_by_department()
    assert isinstance(depts, list)
    assert len(depts) > 0
    first = depts[0]
    assert "Dept" in first
    assert "total_employees" in first
    assert "high_risk_count" in first
    assert "avg_attrition_prob" in first

def test_organization_skill_gaps_ranking():
    gaps = get_organization_skill_gaps()
    assert isinstance(gaps, list)
    assert len(gaps) > 0
    assert "skill" in gaps[0]
    assert "employees_missing" in gaps[0]
    assert "severity" in gaps[0]
    assert gaps[0]["severity"] in ["HIGH", "MEDIUM", "LOW"]

def test_employee_profile_lookup():
    profile = get_employee_skill_profile(101)
    assert profile is not None
    assert profile["Employee_ID"] == 101
    assert "CurrentSkills" in profile
    assert "Skill_Gap" in profile
    assert "Recommendation" in profile

def test_courses_catalog_retrieval():
    courses = get_all_courses()
    assert len(courses) >= 10
    assert "CourseID" in courses[0]
    assert "Title" in courses[0]
