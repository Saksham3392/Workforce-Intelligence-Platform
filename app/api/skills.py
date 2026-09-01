from fastapi import APIRouter
from app.services.recommendation_service import get_all_courses
from app.services.skill_gap_service import get_organization_skill_gaps

router = APIRouter(prefix="/skills", tags=["Skills & Upskilling"])

@router.get("/gaps")
def list_skill_gaps():
    return get_organization_skill_gaps()

@router.get("/courses")
def list_courses():
    return get_all_courses()
