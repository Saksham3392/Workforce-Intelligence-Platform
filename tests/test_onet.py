"""
Automated unit tests for O*NET workforce intelligence services and API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.onet_service import (
    search_occupations,
    get_essential_skills_by_soc,
    get_software_skills_by_soc,
    get_top_hot_technologies,
    search_software_tools,
    get_role_onet_benchmark,
    get_onet_analytics_summary
)

client = TestClient(app)

def test_onet_analytics_summary():
    summary = get_onet_analytics_summary()
    assert isinstance(summary, dict)
    assert summary["total_occupations"] > 800
    assert summary["total_software_records"] > 20000
    assert summary["unique_software_tools"] > 5000
    assert summary["total_hot_technologies"] > 100
    assert summary["avg_essential_importance"] > 0

def test_search_occupations():
    results = search_occupations("Developer", limit=5)
    assert isinstance(results, list)
    assert len(results) > 0
    assert any("Developer" in r["title"] for r in results)

def test_get_essential_skills_by_soc():
    # 15-1252.00 is Software Developers
    skills = get_essential_skills_by_soc("15-1252.00", min_importance=3.0)
    assert isinstance(skills, list)
    assert len(skills) > 0
    assert "Element Name" in skills[0]
    assert "Importance" in skills[0]
    assert "Level" in skills[0]
    assert "SkillScore" in skills[0]
    assert skills[0]["Importance"] >= 3.0

def test_get_software_skills_by_soc():
    soft = get_software_skills_by_soc("15-1252.00", hot_tech_only=True)
    assert isinstance(soft, list)
    assert len(soft) > 0
    assert all(s["IsHotTech"] is True for s in soft)

def test_top_hot_technologies():
    hot = get_top_hot_technologies(limit=10)
    assert isinstance(hot, list)
    assert len(hot) == 10
    assert "SoftwareName" in hot[0]
    assert "Occurrences" in hot[0]
    # Check top tools include Excel or Office
    tool_names = [h["SoftwareName"] for h in hot]
    assert "Microsoft Excel" in tool_names or "Microsoft Office software" in tool_names

def test_search_software_tools():
    results = search_software_tools("Python")
    assert isinstance(results, list)
    assert len(results) > 0
    first = results[0]
    assert "SoftwareName" in first
    assert "Python" in first["SoftwareName"]
    assert first["occupations_count"] > 50

def test_get_role_onet_benchmark():
    benchmark = get_role_onet_benchmark("Data Analyst")
    assert benchmark is not None
    assert "SOC_Code" in benchmark
    assert "Top_Essential_Skills" in benchmark
    assert "Hot_Software_Tools" in benchmark

# API Endpoint Tests
def test_api_onet_summary():
    response = client.get("/onet/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_occupations" in data

def test_api_onet_occupations():
    response = client.get("/onet/occupations?query=Scientist&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5

def test_api_onet_essential_skills():
    response = client.get("/onet/essential-skills?soc_code=15-1252.00&min_importance=3.5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_api_onet_software_skills():
    response = client.get("/onet/software-skills?soc_code=15-1252.00&hot_tech_only=true")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_api_onet_hot_technologies():
    response = client.get("/onet/hot-technologies?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

def test_api_onet_software_search():
    response = client.get("/onet/software-search?query=Docker")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_api_onet_benchmark():
    response = client.get("/onet/benchmark?role=Software Engineer")
    assert response.status_code == 200
    data = response.json()
    assert "SOC_Code" in data
