"""
O*NET Data Processing Pipeline
Ingests raw O*NET essential skills and software skills CSVs, performs data cleaning,
normalization, pivoting, and generates processed datasets for role intelligence and skill querying.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def process_onet_data(raw_dir: Path, processed_dir: Path):
    print("Starting O*NET data processing pipeline...")
    
    essential_raw_path = raw_dir / "onet_essential_skills.csv"
    software_raw_path = raw_dir / "onet_software_skills.csv"
    occupation_raw_path = raw_dir / "occupation_data.csv"

    if not essential_raw_path.exists():
        if (raw_dir / "essential_skills.csv").exists():
            essential_raw_path = raw_dir / "essential_skills.csv"
        else:
            raise FileNotFoundError(f"Essential skills file not found in {raw_dir}")

    if not software_raw_path.exists():
        if (raw_dir / "software_skills.csv").exists():
            software_raw_path = raw_dir / "software_skills.csv"
        else:
            raise FileNotFoundError(f"Software skills file not found in {raw_dir}")

    # 1. Process Essential Skills
    print(f"Reading essential skills from {essential_raw_path}...")
    df_ess = pd.read_csv(essential_raw_path)
    
    # Clean text columns
    for col in ["O*NET-SOC Code", "Title", "Element ID", "Element Name", "Scale ID", "Scale Name"]:
        if col in df_ess.columns:
            df_ess[col] = df_ess[col].astype(str).str.strip()

    # Filter out suppressed rows if flag is Y
    if "Recommend Suppress" in df_ess.columns:
        df_ess = df_ess[df_ess["Recommend Suppress"] != "Y"].copy()

    # Pivot Scale Name so each row is (SOC, Title, Element ID, Element Name) with Importance and Level
    pivot_cols = ["O*NET-SOC Code", "Title", "Element ID", "Element Name"]
    df_importance = df_ess[df_ess["Scale Name"] == "Importance"][pivot_cols + ["Data Value", "Standard Error", "Lower CI Bound", "Upper CI Bound"]].rename(
        columns={
            "Data Value": "Importance",
            "Standard Error": "Importance_SE",
            "Lower CI Bound": "Importance_LowerCI",
            "Upper CI Bound": "Importance_UpperCI"
        }
    )
    
    df_level = df_ess[df_ess["Scale Name"] == "Level"][pivot_cols + ["Data Value", "Standard Error", "Lower CI Bound", "Upper CI Bound"]].rename(
        columns={
            "Data Value": "Level",
            "Standard Error": "Level_SE",
            "Lower CI Bound": "Level_LowerCI",
            "Upper CI Bound": "Level_UpperCI"
        }
    )

    df_ess_processed = pd.merge(df_importance, df_level, on=pivot_cols, how="outer")
    
    # Fill any missing metrics with median/defaults
    df_ess_processed["Importance"] = df_ess_processed["Importance"].fillna(0.0).round(2)
    df_ess_processed["Level"] = df_ess_processed["Level"].fillna(0.0).round(2)
    
    # Calculate Composite Skill Weight: (Importance * Level) normalized to 0-100 scale
    # Max possible = 5.0 * 7.0 = 35.0
    df_ess_processed["SkillScore"] = ((df_ess_processed["Importance"] * df_ess_processed["Level"]) / 35.0 * 100).round(1)

    ess_out_path = processed_dir / "onet_essential_skills_processed.csv"
    df_ess_processed.to_csv(ess_out_path, index=False)
    print(f"Saved processed essential skills ({len(df_ess_processed)} rows) to {ess_out_path}")

    # 2. Process Software Skills
    print(f"Reading software skills from {software_raw_path}...")
    df_soft = pd.read_csv(software_raw_path)

    # Clean text columns
    for col in ["O*NET-SOC Code", "Title", "Workplace Example", "Element ID", "Element Name", "Hot Technology", "In Demand"]:
        if col in df_soft.columns:
            df_soft[col] = df_soft[col].astype(str).str.strip()

    df_soft_processed = df_soft.rename(columns={
        "Workplace Example": "SoftwareName",
        "Element ID": "CategoryID",
        "Element Name": "CategoryName",
        "Hot Technology": "IsHotTech",
        "In Demand": "IsInDemand"
    }).copy()

    # Convert flags to boolean
    df_soft_processed["IsHotTech"] = df_soft_processed["IsHotTech"].str.upper() == "Y"
    df_soft_processed["IsInDemand"] = df_soft_processed["IsInDemand"].str.upper() == "Y"

    # Deduplicate
    df_soft_processed = df_soft_processed.drop_duplicates(subset=["O*NET-SOC Code", "SoftwareName", "CategoryID"])

    soft_out_path = processed_dir / "onet_software_skills_processed.csv"
    df_soft_processed.to_csv(soft_out_path, index=False)
    print(f"Saved processed software skills ({len(df_soft_processed)} rows) to {soft_out_path}")

    # 3. Create Hot Technologies and In-Demand Summary
    print("Generating Hot Technologies summary...")
    hot_summary = df_soft_processed[df_soft_processed["IsHotTech"]].groupby("SoftwareName").agg(
        Occurrences=("O*NET-SOC Code", "nunique"),
        Category=("CategoryName", "first"),
        InDemandCount=("IsInDemand", lambda x: int(x.sum()))
    ).reset_index().sort_values(by="Occurrences", ascending=False)

    hot_out_path = processed_dir / "onet_hot_technologies.csv"
    hot_summary.to_csv(hot_out_path, index=False)
    print(f"Saved hot technologies summary ({len(hot_summary)} tools) to {hot_out_path}")

    # 4. Create Role-to-O*NET Mapping & Skills Matrix
    if occupation_raw_path.exists():
        print("Mapping project occupations to O*NET benchmarks...")
        df_occ = pd.read_csv(occupation_raw_path)
        
        # Merge occupations with top essential skills and software tools
        role_benchmarks = []
        for _, occ_row in df_occ.iterrows():
            soc = occ_row["O*NET-SOC Code"].strip()
            title = occ_row["Title"].strip()
            
            # Top essential skills
            soc_ess = df_ess_processed[df_ess_processed["O*NET-SOC Code"] == soc].sort_values(by="SkillScore", ascending=False)
            top_skills = soc_ess["Element Name"].tolist()[:5]
            
            # Software skills
            soc_soft = df_soft_processed[df_soft_processed["O*NET-SOC Code"] == soc]
            hot_tools = soc_soft[soc_soft["IsHotTech"]]["SoftwareName"].tolist()[:10]
            in_demand_tools = soc_soft[soc_soft["IsInDemand"]]["SoftwareName"].tolist()[:5]
            
            role_benchmarks.append({
                "SOC_Code": soc,
                "Occupation_Title": title,
                "Top_Essential_Skills": ", ".join(top_skills),
                "Hot_Software_Tools": ", ".join(hot_tools),
                "In_Demand_Software": ", ".join(in_demand_tools),
                "Total_Software_Count": len(soc_soft)
            })

        df_benchmarks = pd.DataFrame(role_benchmarks)
        bench_out_path = processed_dir / "onet_role_skills_matrix.csv"
        df_benchmarks.to_csv(bench_out_path, index=False)
        print(f"Saved O*NET role skills matrix to {bench_out_path}")

    print("O*NET data processing completed successfully!")

if __name__ == "__main__":
    from app.utils.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
    process_onet_data(RAW_DATA_DIR, PROCESSED_DATA_DIR)
