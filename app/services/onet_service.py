"""
O*NET Workforce & Skills Intelligence Service
Provides querying, analytical searching, and benchmarking for O*NET essential skills,
workplace software technologies, hot technologies, and role skill requirements.
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from app.utils.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

def _load_essential_skills() -> pd.DataFrame:
    path = PROCESSED_DATA_DIR / "onet_essential_skills_processed.csv"
    if not path.exists():
        from app.services.onet_processor import process_onet_data
        process_onet_data(RAW_DATA_DIR, PROCESSED_DATA_DIR)
    return pd.read_csv(path)

def _load_software_skills() -> pd.DataFrame:
    path = PROCESSED_DATA_DIR / "onet_software_skills_processed.csv"
    if not path.exists():
        from app.services.onet_processor import process_onet_data
        process_onet_data(RAW_DATA_DIR, PROCESSED_DATA_DIR)
    return pd.read_csv(path)

def _load_hot_technologies() -> pd.DataFrame:
    path = PROCESSED_DATA_DIR / "onet_hot_technologies.csv"
    if not path.exists():
        from app.services.onet_processor import process_onet_data
        process_onet_data(RAW_DATA_DIR, PROCESSED_DATA_DIR)
    return pd.read_csv(path)

def _load_role_skills_matrix() -> pd.DataFrame:
    path = PROCESSED_DATA_DIR / "onet_role_skills_matrix.csv"
    if not path.exists():
        from app.services.onet_processor import process_onet_data
        process_onet_data(RAW_DATA_DIR, PROCESSED_DATA_DIR)
    return pd.read_csv(path)

def search_occupations(query: str = "", limit: int = 20) -> List[Dict[str, Any]]:
    """Search unique O*NET occupations by title or SOC code."""
    df_ess = _load_essential_skills()
    occupations = df_ess[["O*NET-SOC Code", "Title"]].drop_duplicates()
    
    if query:
        q = query.lower()
        mask = occupations["Title"].str.lower().str.contains(q, na=False) | occupations["O*NET-SOC Code"].str.lower().str.contains(q, na=False)
        occupations = occupations[mask]
        
    return occupations.head(limit).rename(columns={"O*NET-SOC Code": "soc_code", "Title": "title"}).to_dict(orient="records")

def get_essential_skills_by_soc(
    soc_code: str,
    min_importance: float = 0.0,
    min_level: float = 0.0,
    sort_by: str = "SkillScore"
) -> List[Dict[str, Any]]:
    """Retrieve essential skills for an occupation SOC code with filtering and sorting."""
    df_ess = _load_essential_skills()
    filtered = df_ess[df_ess["O*NET-SOC Code"] == soc_code.strip()]
    
    if filtered.empty:
        # Try matching by title
        filtered = df_ess[df_ess["Title"].str.lower() == soc_code.strip().lower()]
        
    if filtered.empty:
        return []
        
    if min_importance > 0.0:
        filtered = filtered[filtered["Importance"] >= min_importance]
    if min_level > 0.0:
        filtered = filtered[filtered["Level"] >= min_level]
        
    if sort_by in filtered.columns:
        filtered = filtered.sort_values(by=sort_by, ascending=False)
        
    return filtered.to_dict(orient="records")

def get_software_skills_by_soc(
    soc_code: str,
    hot_tech_only: bool = False,
    in_demand_only: bool = False,
    category: Optional[str] = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """Retrieve software tools associated with an occupation SOC code."""
    df_soft = _load_software_skills()
    filtered = df_soft[df_soft["O*NET-SOC Code"] == soc_code.strip()]
    
    if filtered.empty:
        filtered = df_soft[df_soft["Title"].str.lower() == soc_code.strip().lower()]
        
    if filtered.empty:
        return []
        
    if hot_tech_only:
        filtered = filtered[filtered["IsHotTech"] == True]
    if in_demand_only:
        filtered = filtered[filtered["IsInDemand"] == True]
    if category:
        filtered = filtered[filtered["CategoryName"].str.lower().str.contains(category.lower(), na=False)]
        
    return filtered.head(limit).to_dict(orient="records")

def get_top_hot_technologies(
    category: Optional[str] = None,
    limit: int = 25
) -> List[Dict[str, Any]]:
    """Retrieve top hot technologies across all labor market occupations."""
    df_hot = _load_hot_technologies()
    if category:
        df_hot = df_hot[df_hot["Category"].str.lower().str.contains(category.lower(), na=False)]
    return df_hot.head(limit).to_dict(orient="records")

def search_software_tools(query: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Search for software tools across occupations and return adoption statistics."""
    df_soft = _load_software_skills()
    q = query.lower()
    matches = df_soft[df_soft["SoftwareName"].str.lower().str.contains(q, na=False)]
    
    if matches.empty:
        return []
        
    summary = matches.groupby(["SoftwareName", "CategoryName"]).agg(
        occupations_count=("O*NET-SOC Code", "nunique"),
        is_hot_tech=("IsHotTech", "any"),
        is_in_demand=("IsInDemand", "any")
    ).reset_index().sort_values(by="occupations_count", ascending=False)
    
    return summary.head(limit).to_dict(orient="records")

def get_software_occupations(software_name: str) -> List[Dict[str, Any]]:
    """Retrieve all occupations requiring a specific software tool."""
    df_soft = _load_software_skills()
    matches = df_soft[df_soft["SoftwareName"].str.lower() == software_name.strip().lower()]
    if matches.empty:
        matches = df_soft[df_soft["SoftwareName"].str.lower().str.contains(software_name.strip().lower(), na=False)]
    if matches.empty:
        return []
    
    unique_occs = matches[["Title", "O*NET-SOC Code", "CategoryName", "IsHotTech", "IsInDemand"]].drop_duplicates()
    return unique_occs.rename(columns={
        "Title": "occupation_title",
        "O*NET-SOC Code": "soc_code",
        "CategoryName": "category",
        "IsHotTech": "is_hot_tech",
        "IsInDemand": "is_in_demand"
    }).sort_values(by="is_in_demand", ascending=False).to_dict(orient="records")

def get_role_onet_benchmark(role_name: str) -> Optional[Dict[str, Any]]:
    """Benchmark an internal organization job role against O*NET standards."""
    df_matrix = _load_role_skills_matrix()
    
    # Try exact match or substring match
    r_lower = role_name.lower().strip()
    match = df_matrix[df_matrix["Occupation_Title"].str.lower().str.contains(r_lower, na=False)]
    
    if match.empty:
        # Fallback keyword matching
        keywords = r_lower.split()
        for kw in keywords:
            if len(kw) > 3:
                match = df_matrix[df_matrix["Occupation_Title"].str.lower().str.contains(kw, na=False)]
                if not match.empty:
                    break
                    
    if match.empty:
        return None
        
    return match.iloc[0].to_dict()

def get_onet_analytics_summary() -> Dict[str, Any]:
    """Retrieve aggregate analytics and summary statistics for O*NET datasets."""
    df_ess = _load_essential_skills()
    df_soft = _load_software_skills()
    df_hot = _load_hot_technologies()
    
    total_occupations = df_ess["O*NET-SOC Code"].nunique()
    total_software_records = len(df_soft)
    unique_software_tools = df_soft["SoftwareName"].nunique()
    total_hot_tech = len(df_hot)
    total_in_demand = int(df_soft["IsInDemand"].sum())
    
    top_categories = df_soft["CategoryName"].value_counts().head(5).to_dict()
    avg_importance = round(float(df_ess["Importance"].mean()), 2)
    avg_level = round(float(df_ess["Level"].mean()), 2)
    
    return {
        "total_occupations": total_occupations,
        "total_essential_skills_records": len(df_ess),
        "total_software_records": total_software_records,
        "unique_software_tools": unique_software_tools,
        "total_hot_technologies": total_hot_tech,
        "total_in_demand_instances": total_in_demand,
        "avg_essential_importance": avg_importance,
        "avg_essential_level": avg_level,
        "top_software_categories": top_categories
    }
