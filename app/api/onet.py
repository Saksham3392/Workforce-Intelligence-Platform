"""
O*NET Workforce & Skills Intelligence API Router
Exposes endpoints for querying O*NET essential skills, software tools, hot technologies, and role benchmarks.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict, Any
from app.services import onet_service

router = APIRouter(prefix="/onet", tags=["O*NET Workforce Intelligence"])

@router.get("/summary")
def get_onet_summary():
    """Retrieve aggregate summary analytics for O*NET datasets."""
    return onet_service.get_onet_analytics_summary()

@router.get("/occupations")
def search_occupations(
    query: str = Query(default="", description="Search query by title or SOC code"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return")
):
    """Search O*NET occupations by title or SOC code."""
    return onet_service.search_occupations(query=query, limit=limit)

@router.get("/essential-skills")
def get_essential_skills(
    soc_code: str = Query(..., description="O*NET-SOC Code or Occupation Title (e.g. 15-1252.00)"),
    min_importance: float = Query(default=0.0, ge=0.0, le=5.0, description="Minimum Importance score (1-5)"),
    min_level: float = Query(default=0.0, ge=0.0, le=7.0, description="Minimum Level score (0-7)"),
    sort_by: str = Query(default="SkillScore", description="Sort field: SkillScore, Importance, or Level")
):
    """Retrieve essential skills for a specific occupation SOC code."""
    results = onet_service.get_essential_skills_by_soc(
        soc_code=soc_code,
        min_importance=min_importance,
        min_level=min_level,
        sort_by=sort_by
    )
    if not results:
        raise HTTPException(status_code=404, detail=f"No essential skills found for '{soc_code}'")
    return results

@router.get("/software-skills")
def get_software_skills(
    soc_code: str = Query(..., description="O*NET-SOC Code or Occupation Title (e.g. 15-1252.00)"),
    hot_tech_only: bool = Query(default=False, description="Filter for Hot Technologies only"),
    in_demand_only: bool = Query(default=False, description="Filter for In-Demand software only"),
    category: Optional[str] = Query(default=None, description="Filter by software category name"),
    limit: int = Query(default=50, ge=1, le=200, description="Max records to return")
):
    """Retrieve workplace software tools for a specific occupation."""
    results = onet_service.get_software_skills_by_soc(
        soc_code=soc_code,
        hot_tech_only=hot_tech_only,
        in_demand_only=in_demand_only,
        category=category,
        limit=limit
    )
    if not results:
        raise HTTPException(status_code=404, detail=f"No software skills found for '{soc_code}'")
    return results

@router.get("/hot-technologies")
def get_hot_technologies(
    category: Optional[str] = Query(default=None, description="Filter by software category"),
    limit: int = Query(default=25, ge=1, le=100, description="Max records to return")
):
    """Retrieve top hot technologies across the labor market."""
    return onet_service.get_top_hot_technologies(category=category, limit=limit)

@router.get("/software-search")
def search_software_tools(
    query: str = Query(..., min_length=2, description="Software tool search keyword (e.g. Python, Docker, Excel)"),
    limit: int = Query(default=25, ge=1, le=100, description="Max records to return")
):
    """Search for software tools across occupations and view adoption statistics."""
    return onet_service.search_software_tools(query=query, limit=limit)

@router.get("/benchmark")
def benchmark_role(
    role: str = Query(..., description="Company job role to benchmark (e.g. Data Analyst, Software Engineer)")
):
    """Benchmark an internal organization job role against O*NET standards."""
    result = onet_service.get_role_onet_benchmark(role_name=role)
    if not result:
        raise HTTPException(status_code=404, detail=f"No matching O*NET occupation found for role '{role}'")
    return result
