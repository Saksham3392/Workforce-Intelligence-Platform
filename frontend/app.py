import sys
import os
from pathlib import Path

# Ensure project root is first in sys.path and frontend dir does not shadow 'app' package
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

frontend_dir = str(Path(__file__).resolve().parent)
while frontend_dir in sys.path:
    sys.path.remove(frontend_dir)

import json
from collections import Counter
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import importlib
from app.ml.predictor import predict_employee_attrition
from app.validation.employee_schema import EmployeePredictionInput
from app.services import onet_service
importlib.reload(onet_service)

# Page configuration
st.set_page_config(
    page_title="AI Workforce Intelligence & Upskilling Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean Editorial Light Theme Styling (from Saksham3392/JavaProgrammingQ)
theme_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    :root {
        --bg-app: #f8f6f0;
        --bg-sidebar: #ede8dc;
        --bg-card: #ffffff;
        --bg-card-subtle: #f4f0e6;
        --border-color: #dcd4c3;
        --text-main: #181e30;
        --text-muted: #5e667e;
        --accent: #2563eb;
    }

    .stApp {
        background-color: #f8f6f0 !important;
        color: #181e30 !important;
        font-family: 'Manrope', -apple-system, sans-serif;
    }
    
    /* Hide Streamlit Header, Deploy Button, Hamburger Menu (Record Screencast, Print, Settings) and Footer */
    #MainMenu { visibility: hidden !important; display: none !important; }
    header { visibility: hidden !important; display: none !important; height: 0px !important; }
    footer { visibility: hidden !important; display: none !important; }
    [data-testid="stHeader"] { visibility: hidden !important; display: none !important; height: 0px !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
    .stDeployButton { display: none !important; }
    [data-testid="stDeployButton"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    
    /* Pull app content and sidebar to top with proper breathing room */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 2.0rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        max-width: 100% !important;
    }

    /* Remove sidebar header empty gap and pull sidebar to top */
    [data-testid="stSidebarHeader"] {
        display: none !important;
        height: 0px !important;
        padding: 0px !important;
    }

    [data-testid="stSidebar"] {
        background-color: #ede8dc !important;
        border-right: 1px solid #dcd4c3 !important;
        top: 0 !important;
    }

    [data-testid="stSidebarContent"] {
        padding-top: 1.2rem !important;
    }

    [data-testid="stSidebarUserContent"] {
        padding-top: 0.2rem !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0.2rem !important;
    }

    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 0px !important;
        padding-top: 0px !important;
        padding-bottom: 12px;
        border-bottom: 1px solid #dcd4c3;
        margin-bottom: 16px;
    }
    .brand-icon {
        background: #2563eb;
        color: #ffffff;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        box-shadow: 0 4px 12px rgba(37,99,235,0.3);
    }
    .brand-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #181e30;
        line-height: 1.2;
    }
    .brand-sub {
        font-size: 0.75rem;
        color: #5e667e;
        font-weight: 500;
    }

    .view-header {
        background: #ffffff;
        border: 1px solid #dcd4c3;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .view-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #181e30;
        margin-bottom: 2px;
        letter-spacing: -0.01em;
    }
    .view-subtitle {
        font-size: 0.84rem;
        color: #5e667e;
    }
    
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #dcd4c3;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.07);
    }
    
    .kpi-val {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: #2563eb;
    }
    
    .kpi-lbl {
        font-size: 0.8rem;
        font-weight: 600;
        color: #5e667e;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .profile-card {
        background-color: #ffffff;
        border: 1px solid #dcd4c3;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .badge-pill {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.78rem;
        letter-spacing: 0.02em;
    }
        font-weight: 600;
        font-size: 0.82rem;
        letter-spacing: 0.02em;
    }
    .badge-high {
        background-color: rgba(220, 38, 38, 0.1);
        color: #dc2626;
        border: 1px solid rgba(220, 38, 38, 0.25);
    }
    .badge-med {
        background-color: rgba(217, 119, 6, 0.1);
        color: #d97706;
        border: 1px solid rgba(217, 119, 6, 0.25);
    }
    .badge-low {
        background-color: rgba(22, 163, 74, 0.1);
        color: #16a34a;
        border: 1px solid rgba(22, 163, 74, 0.25);
    }

    .badge-dept {
        background-color: #eff6ff;
        color: #1e40af;
        border: 1px solid #bfdbfe;
    }
    
    .rec-card {
        background: #ffffff;
        border-left: 4px solid #2563eb;
        border-top: 1px solid #dcd4c3;
        border-right: 1px solid #dcd4c3;
        border-bottom: 1px solid #dcd4c3;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-radius: 8px;
        color: #181e30;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .skill-chip {
        display: inline-block;
        background-color: #f4f0e6;
        border: 1px solid #dcd4c3;
        color: #181e30;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 3px 4px 3px 0;
    }
    .skill-chip-missing {
        display: inline-block;
        background-color: #fff1f2;
        border: 1px solid #fecdd3;
        color: #e11d48;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 3px 4px 3px 0;
    }

    div[data-testid="stMetricValue"] {
        color: #181e30 !important;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stSelectbox label, .stMultiSelect label, .stTextInput label, .stNumberInput label, .stSlider label {
        color: #181e30 !important;
        font-weight: 600 !important;
    }

    /* Enforce Light Mode on Sidebar Texts, Labels and Radios */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #181e30;
    }
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #5e667e !important;
    }

    /* Radio Buttons in Sidebar and Main Views */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] label div,
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        color: #181e30 !important;
        font-weight: 500 !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"] span,
    div[data-testid="stRadio"] label[data-checked="true"] p {
        color: #2563eb !important;
        font-weight: 700 !important;
    }

    /* MultiSelect and Selectbox Base Containers */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #dcd4c3 !important;
        color: #181e30 !important;
    }
    div[data-baseweb="select"] input {
        color: #181e30 !important;
        background-color: transparent !important;
    }

    /* MultiSelect Tag Chips (Clean Blue Pills) */
    div[data-baseweb="tag"] {
        background-color: #2563eb !important;
        border: none !important;
        color: #ffffff !important;
        border-radius: 5px !important;
        padding: 2px 6px !important;
    }
    div[data-baseweb="tag"] span {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    div[data-baseweb="tag"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }
    div[data-baseweb="tag"]:hover {
        background-color: #1d4ed8 !important;
    }

    /* Dropdown Menus & Popovers */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #dcd4c3 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
    }
    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #181e30 !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="menu"] li:hover {
        background-color: #f4f0e6 !important;
        color: #2563eb !important;
    }

    /* General Inputs */
    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border-color: #dcd4c3 !important;
        color: #181e30 !important;
    }
    input, textarea, select {
        color: #181e30 !important;
    }
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models" / "v1"

@st.cache_data
def load_data():
    df_emp = pd.read_csv(PROCESSED_DIR / "employee_intelligence.csv")
    df_attr = pd.read_csv(PROCESSED_DIR / "employee_attrition_processed.csv")
    
    # Enrich df_emp with exact employee feature columns
    cols_to_merge = [
        'EmployeeID', 'Gender', 'EducationLevel', 'OvertimeHoursPerMonth', 
        'LeavesTaken', 'ProjectsHandled', 'TrainingHours', 'LastPromotionYear', 
        'YearsAtCompany', 'WorkLifeBalanceScore'
    ]
    avail_cols = [c for c in cols_to_merge if c in df_attr.columns]
    df_emp = df_emp.merge(
        df_attr[avail_cols], 
        left_on='Employee_ID', 
        right_on='EmployeeID', 
        how='left'
    )
    
    df_skills = pd.read_csv(PROCESSED_DIR / "employee_skills.csv")
    df_courses = pd.read_csv(PROCESSED_DIR / "courses.csv")
    df_role_skills = pd.read_csv(PROCESSED_DIR / "role_skills.csv")
    
    with open(MODELS_DIR / "metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    return df_emp, df_skills, df_courses, df_role_skills, metadata

df_emp, df_skills, df_courses, df_role_skills, metadata = load_data()

# ----------------- SIDEBAR BRANDING & NAVIGATION -----------------
st.sidebar.markdown("""
<div class="brand-container">
    <div class="brand-icon">HR</div>
    <div>
        <div class="brand-text">Enterprise HR AI</div>
        <div class="brand-sub">Workforce Intelligence Platform</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("**BUSINESS METRICS & ANALYTICS**")

nav_options = [
    "📊 Workforce Health & Retention KPIs",
    "🔍 Talent Risk & Capability Diagnostics",
    "⚡ Predictive Attrition Risk Scoring",
    "🌐 Market Competency & Skill Benchmarks",
    "🧠 AI Governance & Decision Transparency"
]

selected_tab = st.sidebar.radio(
    "Select Business Metric Domain",
    nav_options,
    index=0,
    key="nav_radio_view",
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**GLOBAL WORKFORCE FILTERS**")

all_departments = sorted(df_emp["Dept"].unique().tolist())
all_risks = ["HIGH", "MEDIUM", "LOW"]

department_filter = st.sidebar.multiselect(
    "Departments",
    options=all_departments,
    default=all_departments,
    help="Filter data across the entire platform by Department",
    key="nav_dept_filter"
)

risk_filter = st.sidebar.multiselect(
    "Risk Tiers",
    options=all_risks,
    default=all_risks,
    help="Filter data across the entire platform by Predicted Attrition Risk",
    key="nav_risk_filter"
)

# Apply filters strictly to the selected options
filtered_df = df_emp[
    (df_emp["Dept"].isin(department_filter)) &
    (df_emp["Risk"].isin(risk_filter))
]

def reset_filters_callback():
    st.session_state["nav_dept_filter"] = all_departments
    st.session_state["nav_risk_filter"] = all_risks

if len(department_filter) < len(all_departments) or len(risk_filter) < len(all_risks):
    st.sidebar.button("🔄 Reset Global Filters", on_click=reset_filters_callback, key="reset_filters_btn")

# Sidebar summary counter pill
filtered_pct = (len(filtered_df) / len(df_emp) * 100) if len(df_emp) > 0 else 0
st.sidebar.caption(f"**Cohort Scope**: {len(filtered_df):,} of {len(df_emp):,} employees ({filtered_pct:.1f}%)")

# -------------------------------------------------------------
# 1. TAB: WORKFORCE HEALTH & RETENTION KPIS
# -------------------------------------------------------------
if selected_tab == "📊 Workforce Health & Retention KPIs":
    st.markdown("""
    <div class="view-header">
        <div class="view-title">📊 Workforce Health & Retention KPIs</div>
        <div class="view-subtitle">Executive business metrics, organizational turnover risk, department health indices, and strategic headcount roster.</div>
    </div>
    """, unsafe_allow_html=True)

    total_emp = len(filtered_df)
    
    if total_emp == 0:
        st.warning("⚠️ No employees match the selected department and risk filters. Please adjust filters in the sidebar.")
        if st.button("🔄 Reset to Full Workforce", on_click=reset_filters_callback, key="empty_reset_exec_btn"):
            st.rerun()
    else:
        high_risk_count = int((filtered_df["Risk"] == "HIGH").sum())
        avg_engagement = float(filtered_df["Engagement"].mean())
        avg_salary = float(filtered_df["MonthlySalary"].mean())
        high_risk_pct = (high_risk_count / total_emp * 100)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Workforce in View</div><div class="kpi-val">{total_emp:,}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="kpi-card" style="border-color: #FECACA; background: #FFF5F5;"><div class="kpi-lbl">High Risk Cohort</div><div class="kpi-val" style="color: #DC2626;">{high_risk_count:,} <span style="font-size: 1rem; color: #EF4444;">({high_risk_pct:.1f}%)</span></div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Avg Engagement Score</div><div class="kpi-val" style="color: #059669;">{avg_engagement:.1f}%</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Avg Monthly Salary</div><div class="kpi-val" style="color: #1E40AF;">${avg_salary:,.0f}</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        col_chart1, col_chart2 = st.columns([6, 4])
        
        with col_chart1:
            st.subheader("🏢 Attrition Risk Distribution by Department")
            dept_risk = filtered_df.groupby(["Dept", "Risk"]).size().reset_index(name="Count")
            fig_bar = px.bar(
                dept_risk,
                x="Dept",
                y="Count",
                color="Risk",
                barmode="stack",
                color_discrete_map={"HIGH": "#EF4444", "MEDIUM": "#F59E0B", "LOW": "#10B981"},
                template="plotly_white"
            )
            fig_bar.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                height=320,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_chart2:
            st.subheader("🎯 Risk Breakdown for Selected Cohort")
            risk_counts = filtered_df["Risk"].value_counts().reset_index()
            risk_counts.columns = ["Risk", "Count"]
            fig_pie = px.pie(
                risk_counts,
                names="Risk",
                values="Count",
                color="Risk",
                color_discrete_map={"HIGH": "#EF4444", "MEDIUM": "#F59E0B", "LOW": "#10B981"},
                hole=0.42,
                template="plotly_white"
            )
            fig_pie.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                height=320,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        c_gaps, c_recs = st.columns([5, 5])

        with c_gaps:
            st.subheader("⚠️ Critical Organization Skill Deficits")
            all_gaps = []
            for gaps in filtered_df["Skill_Gap"].dropna():
                if gaps != "None (Proficient)":
                    for s in gaps.split(", "):
                        all_gaps.append(s)
            
            gap_counts = Counter(all_gaps).most_common(8)
            
            if gap_counts:
                df_gap_chart = pd.DataFrame(gap_counts, columns=["Skill", "Count"])
                df_gap_chart["Severity"] = df_gap_chart["Count"].apply(lambda c: "HIGH" if c >= 100 else ("MEDIUM" if c >= 50 else "LOW"))
                
                fig_gap = px.bar(
                    df_gap_chart,
                    x="Count",
                    y="Skill",
                    orientation="h",
                    color="Severity",
                    color_discrete_map={"HIGH": "#DC2626", "MEDIUM": "#D97706", "LOW": "#2563EB"},
                    labels={"Count": "Employees Missing Skill", "Skill": "Skill Name"},
                    template="plotly_white"
                )
                fig_gap.update_layout(
                    yaxis=dict(autorange="reversed"),
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=340,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_gap, use_container_width=True)
            else:
                st.info("No skill gaps detected in the active cohort.")

        with c_recs:
            st.subheader("💡 Priority Upskilling Intervention Recommendations")
            recs_pool = filtered_df.sort_values(by="Attrition_Prob", ascending=False)[
                ["Employee_ID", "Name", "Role", "Risk", "Primary_Gap", "Recommendation"]
            ].head(6)
            
            if not recs_pool.empty:
                for _, r in recs_pool.iterrows():
                    badge_class = "badge-high" if r["Risk"] == "HIGH" else ("badge-med" if r["Risk"] == "MEDIUM" else "badge-low")
                    st.markdown(f"""
                    <div class="rec-card">
                        <strong>ID {r['Employee_ID']} — {r['Name']}</strong> • <span style="color:#5e667e;">{r['Role']}</span> 
                        <span class="badge-pill {badge_class}">{r['Risk']} RISK</span><br/>
                        Skill Gap: <strong>{r['Primary_Gap']}</strong> ➔ <em>{r['Recommendation']}</em>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No employee recommendations in view.")

        st.markdown("---")
        st.subheader("📋 Filtered Workforce Master Records")
        
        display_df = filtered_df[[
            "Employee_ID", "Name", "Dept", "Role", "Age", "MonthlySalary", 
            "Attrition_Prob", "Risk", "Engagement", "Primary_Gap", "Recommendation"
        ]].copy()
        
        display_df["Attrition_Prob"] = (display_df["Attrition_Prob"] * 100).round(1).astype(str) + "%"
        display_df["MonthlySalary"] = "$" + display_df["MonthlySalary"].map("{:,.0f}".format)
        display_df["Engagement"] = display_df["Engagement"].astype(str) + "%"
        
        st.dataframe(display_df, use_container_width=True, height=280)

# -------------------------------------------------------------
# 2. TAB: TALENT RISK & CAPABILITY DIAGNOSTICS
# -------------------------------------------------------------
elif selected_tab == "🔍 Talent Risk & Capability Diagnostics":
    st.markdown("""
    <div class="view-header">
        <div class="view-title">🔍 Talent Risk & Capability Diagnostics</div>
        <div class="view-subtitle">Individual 360° employee flight risk profile, live intervention ROI cockpit, verified capability mapping, and AI upskilling paths.</div>
    </div>
    """, unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("⚠️ No employees match the active filters. Defaulting to full workforce.")
        target_df = df_emp
    else:
        target_df = filtered_df

    # Quick search & selector bar
    col_sel1, col_sel2 = st.columns([7, 3])
    with col_sel1:
        emp_options = {
            f"ID {row['Employee_ID']} — {row['Name']} ({row['Dept']} • {row['Role']} • {row['Risk']} RISK)": row['Employee_ID']
            for _, row in target_df.iterrows()
        }
        selected_label = st.selectbox("Select Employee Profile to Inspect", options=list(emp_options.keys()), key="drill_emp_select_main")
        selected_emp_id = emp_options[selected_label]
        
    with col_sel2:
        st.metric(
            label="Employees in Active Scope",
            value=f"{len(target_df):,}",
            delta=f"Filtered from {len(df_emp):,}"
        )

    emp_row = target_df[target_df["Employee_ID"] == selected_emp_id].iloc[0]
    emp_current_skills = df_skills[df_skills["EmployeeID"] == selected_emp_id]["Skill"].tolist()
    role_req_skills = df_role_skills[df_role_skills["Role"] == emp_row["Role"]]["Skill"].tolist()
    missing_skills = sorted(list(set(role_req_skills) - set(emp_current_skills)))
    match_pct = round((len(role_req_skills) - len(missing_skills)) / len(role_req_skills) * 100) if role_req_skills else 100

    # Compact Modern Employee Profile Card
    risk_class = "badge-high" if emp_row["Risk"] == "HIGH" else ("badge-med" if emp_row["Risk"] == "MEDIUM" else "badge-low")
    
    st.markdown(f"""
    <div class="profile-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 1.22rem; font-weight: 700; color: #181e30;">{emp_row['Name']}</span>
                    <span class="badge-pill {risk_class}">{emp_row['Risk']} RISK ({emp_row['Attrition_Prob']*100:.1f}%)</span>
                    <span class="badge-pill badge-dept">{emp_row['Dept']}</span>
                </div>
                <div style="color: #5e667e; font-size: 0.86rem; font-weight: 500;">
                    <strong>{emp_row['Role']}</strong> • Employee ID: <code>#{emp_row['Employee_ID']}</code> • Age: {emp_row['Age']} yrs
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.72rem; font-weight: 600; color: #5e667e; text-transform: uppercase; letter-spacing: 0.04em;">Monthly Compensation</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #2563eb; font-family: 'Space Grotesk', sans-serif;">${emp_row['MonthlySalary']:,}<span style="font-size: 0.8rem; color: #5e667e; font-weight: 500;">/mo</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------- UNIFIED REAL-TIME INTERVENTION & GAUGE COCKPIT -----------------
    # Extract exact real employee baseline values
    emp_id_int = int(emp_row["Employee_ID"])
    cur_salary = float(emp_row.get("MonthlySalary", 65000))
    cur_overtime = float(emp_row.get("OvertimeHoursPerMonth", 20))
    cur_wlb = float(emp_row.get("WorkLifeBalanceScore", 3.0))
    cur_training = int(emp_row.get("TrainingHours", 20))
    cur_prom_year = int(emp_row.get("LastPromotionYear", 2023))
    cur_tenure = int(emp_row.get("YearsAtCompany", 4))
    cur_leaves = int(emp_row.get("LeavesTaken", 10))
    cur_projects = int(emp_row.get("ProjectsHandled", 5))
    cur_gender = str(emp_row.get("Gender", "Female"))
    cur_edu = int(emp_row.get("EducationLevel", 3))
    cur_perf = int(emp_row.get("PerformanceRating", 3))

    st.markdown("### ⚡ Real-Time Attrition Risk Gauge & What-If Cockpit")
    st.caption("Adjust managerial intervention levers on the left to project real-time risk mitigation on the live gauge:")

    c_levers, c_live_gauge = st.columns([6, 4])
    
    with c_levers:
        lev_col1, lev_col2 = st.columns(2)
        with lev_col1:
            sim_salary = st.slider(
                "Monthly Salary ($)",
                min_value=max(10000, int(cur_salary * 0.5)),
                max_value=max(250000, int(cur_salary * 2.0)),
                value=int(cur_salary),
                step=2500,
                key=f"live_sal_{emp_id_int}",
                help="Adjust compensation lever"
            )
            sim_promoted = st.checkbox(
                "Grant Promotion in 2026",
                value=False,
                key=f"live_prom_{emp_id_int}",
                help="Eliminate promotion stagnation"
            )
            sim_training = st.slider(
                "Annual Training (Hours)",
                min_value=0,
                max_value=120,
                value=min(120, cur_training),
                step=5,
                key=f"live_train_{emp_id_int}",
                help="Upskilling investment"
            )

        with lev_col2:
            sim_overtime = st.slider(
                "Monthly Overtime (Hours)",
                min_value=0.0,
                max_value=60.0,
                value=float(cur_overtime),
                step=1.0,
                key=f"live_ot_{emp_id_int}",
                help="Adjust overtime workload"
            )
            sim_wlb = st.slider(
                "Work-Life Balance (1.0 to 5.0)",
                min_value=1.0,
                max_value=5.0,
                value=float(round(cur_wlb, 1)),
                step=0.1,
                key=f"live_wlb_{emp_id_int}",
                help="Adjust employee wellbeing score"
            )

    # Real-time ML Prediction with Simulated Levers
    sim_input = EmployeePredictionInput(
        EmployeeID=emp_id_int,
        Age=int(emp_row["Age"]),
        Department=str(emp_row["Dept"]),
        JobRole=str(emp_row["Role"]),
        Gender=cur_gender,
        EducationLevel=cur_edu,
        MonthlySalary=float(sim_salary),
        OvertimeHoursPerMonth=float(sim_overtime),
        LeavesTaken=cur_leaves,
        ProjectsHandled=cur_projects,
        TrainingHours=int(sim_training),
        YearsAtCompany=cur_tenure,
        LastPromotionYear=2026 if sim_promoted else cur_prom_year,
        WorkLifeBalanceScore=float(sim_wlb),
        PerformanceRating=cur_perf
    )
    
    sim_result = predict_employee_attrition(sim_input)
    baseline_prob = float(emp_row["Attrition_Prob"]) * 100
    sim_prob = sim_result.AttritionProbability * 100
    prob_delta = baseline_prob - sim_prob

    with c_live_gauge:
        gauge_color = "#EF4444" if sim_result.RiskLevel=="HIGH" else ("#F59E0B" if sim_result.RiskLevel=="MEDIUM" else "#10B981")
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=sim_prob,
            delta={
                'reference': baseline_prob,
                'position': "bottom",
                'valueformat': ".1f",
                'prefix': "Δ vs Baseline: ",
                'suffix': "%",
                'increasing': {'color': '#ef4444'},
                'decreasing': {'color': '#10b981'}
            },
            number={'suffix': "%", 'font': {'color': '#181e30', 'family': 'Space Grotesk', 'size': 32}},
            title={'text': f"<b>Live {sim_result.RiskLevel} Risk</b>", 'font': {'color': gauge_color, 'size': 16}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#5e667e'},
                'bar': {'color': gauge_color},
                'steps': [
                    {'range': [0, 45], 'color': "rgba(16, 185, 129, 0.12)"},
                    {'range': [45, 70], 'color': "rgba(245, 158, 11, 0.12)"},
                    {'range': [70, 100], 'color': "rgba(239, 68, 68, 0.12)"}
                ],
                'threshold': {
                    'line': {'color': '#6b7280', 'width': 3},
                    'thickness': 0.8,
                    'value': baseline_prob
                }
            }
        ))
        fig_gauge.update_layout(
            height=250,
            margin=dict(l=15, r=15, t=30, b=15),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Active Risk Attribution
    driver_chips = []
    for d in sim_result.TopRiskDrivers:
        driver_chips.append(f"<span class='skill-chip'>⚠️ {d.feature} (+{d.impact*100:.0f}%)</span>")
    st.markdown("<strong>Active ML Risk Drivers:</strong> " + "".join(driver_chips), unsafe_allow_html=True)

    st.markdown("---")

    # Engagement, Performance & Competency Index
    col_metric, col_skills = st.columns([4, 6])
    
    with col_metric:
        st.subheader("📊 Performance & Career Index")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Engagement Score", f"{emp_row['Engagement']}%", delta="Normal" if emp_row['Engagement']>=70 else "Low Alert", delta_color="normal" if emp_row['Engagement']>=70 else "inverse")
        with m2:
            st.metric("Performance Rating", f"{emp_row['PerformanceRating']} / 5", delta="Validated")
            
        st.markdown(f"""
        - **Tenure Progression**: **{cur_tenure}** years at organization.
        - **Role Competency Coverage**: **{match_pct}%** of required skills met.
        - **Primary Skill Gap**: <span class="badge-pill badge-high">{emp_row['Primary_Gap']}</span>
        """, unsafe_allow_html=True)

    with col_skills:
        st.subheader("🧩 Role Competency & Skill Gap Breakdown")
        sk_col1, sk_col2 = st.columns(2)
        with sk_col1:
            st.markdown("#### ✅ Current Verified Skills")
            if emp_current_skills:
                chips_html = "".join([f'<span class="skill-chip">✓ {s}</span>' for s in emp_current_skills])
                st.markdown(chips_html, unsafe_allow_html=True)
            else:
                st.info("No recorded skills in verified database.")

        with sk_col2:
            st.markdown(f"#### ⚠️ Identified Deficits ({len(missing_skills)} Missing)")
            if missing_skills:
                missing_html = "".join([f'<span class="skill-chip-missing">✗ {s}</span>' for s in missing_skills])
                st.markdown(missing_html, unsafe_allow_html=True)
            else:
                st.success("🎉 Full Competency! Meets all required role skills.")

    st.markdown("---")

    # AI Course Recommendation & Pathway
    st.subheader("🎓 AI-Prescribed Upskilling Recommendation")
    matching_courses = df_courses[df_courses["TargetSkill"] == emp_row["Primary_Gap"]]
    
    if not matching_courses.empty:
        c_row = matching_courses.iloc[0]
        st.markdown(f"""
        <div class="rec-card" style="border-left-color: #10b981;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 700; font-size: 1.05rem; color: #181e30;">{c_row['Title']}</span>
                <span class="badge-pill badge-dept">{c_row['CourseID']}</span>
            </div>
            <div style="color: #5e667e; font-size: 0.88rem; margin-bottom: 6px;">
                Category: <strong>{c_row['Category']}</strong> • Target Deficit: <strong>{c_row['TargetSkill']}</strong> • Difficulty: <strong>{c_row['Difficulty']}</strong> • Duration: <strong>{c_row['DurationHours']} Hours</strong> • Rating: <strong>{c_row['Rating']} ⭐</strong>
            </div>
            <div style="color: #16a34a; font-size: 0.86rem; font-weight: 600;">
                🎯 Projected Outcome: Closes '{emp_row['Primary_Gap']}' deficit and enhances role mastery.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"**Recommended Pathway**: {emp_row['Recommendation']}")

# -------------------------------------------------------------
# 3. TAB: PREDICTIVE ATTRITION RISK SCORING
# -------------------------------------------------------------
elif selected_tab == "⚡ Predictive Attrition Risk Scoring":
    st.markdown("""
    <div class="view-header">
        <div class="view-title">⚡ Predictive Attrition Risk Scoring</div>
        <div class="view-subtitle">Instant candidate and employee flight risk calculation, Pydantic schema validation, and key driver attribution metrics.</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("attrition_prediction_form"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            p_emp_id = st.number_input("Employee ID", min_value=1, value=9999, key="pred_emp_id")
            p_age = st.number_input("Age", min_value=18, max_value=80, value=32, key="pred_age")
            p_dept = st.selectbox("Department", options=all_departments, key="pred_dept")
            p_role = st.selectbox("Job Role", options=sorted(df_emp["Role"].unique()), key="pred_role")
            p_gender = st.selectbox("Gender", options=["Female", "Male", "Other"], key="pred_gender")
            p_edu = st.selectbox("Education Level (1=HighSchool, 5=Doctorate)", options=[1, 2, 3, 4, 5], index=2, key="pred_edu")

        with col_b:
            p_salary = st.number_input("Monthly Salary ($)", min_value=20000, max_value=500000, value=65000, step=5000, key="pred_salary")
            p_overtime = st.slider("Monthly Overtime Hours", min_value=0, max_value=60, value=25, key="pred_overtime")
            p_leaves = st.number_input("Leaves Taken (Past Year)", min_value=0, max_value=60, value=12, key="pred_leaves")
            p_projects = st.number_input("Projects Handled", min_value=1, max_value=30, value=7, key="pred_projects")
            p_training = st.number_input("Training Hours", min_value=0, max_value=150, value=20, key="pred_training")

        with col_c:
            p_tenure = st.number_input("Years at Company", min_value=0, max_value=40, value=4, key="pred_tenure")
            p_prom_year = st.number_input("Last Promotion Year", min_value=2010, max_value=2026, value=2023, key="pred_prom_year")
            p_wlb = st.slider("Work-Life Balance Score (0.0 = Poor, 5.0 = Excellent)", min_value=0.0, max_value=5.0, value=2.2, step=0.1, key="pred_wlb")
            p_perf = st.selectbox("Performance Rating (1-5)", options=[1, 2, 3, 4, 5], index=2, key="pred_perf")

        submitted = st.form_submit_button("🚀 Run Live Attrition Assessment")

    if submitted:
        inp = EmployeePredictionInput(
            EmployeeID=p_emp_id,
            Age=p_age,
            Department=p_dept,
            JobRole=p_role,
            Gender=p_gender,
            EducationLevel=p_edu,
            MonthlySalary=float(p_salary),
            OvertimeHoursPerMonth=float(p_overtime),
            LeavesTaken=p_leaves,
            ProjectsHandled=p_projects,
            TrainingHours=p_training,
            YearsAtCompany=p_tenure,
            LastPromotionYear=p_prom_year,
            WorkLifeBalanceScore=float(p_wlb),
            PerformanceRating=p_perf
        )
        
        result = predict_employee_attrition(inp)
        
        st.markdown("### 🎯 Assessment Outcome")
        r_col1, r_col2 = st.columns([5, 5])
        
        with r_col1:
            st.metric(
                label="Calculated Attrition Risk",
                value=f"{result.RiskLevel} RISK",
                delta=f"Prob: {result.AttritionProbability*100:.1f}%",
                delta_color="inverse" if result.RiskLevel=="HIGH" else "normal"
            )
        
        with r_col2:
            st.markdown("#### 🔬 Key Contributing Risk Drivers:")
            for d in result.TopRiskDrivers:
                st.write(f"- ⚠️ **{d.feature}** (Impact Weight: +{d.impact*100:.0f}%)")

# -------------------------------------------------------------
# 4. TAB: MARKET COMPETENCY & SKILL BENCHMARKS
# -------------------------------------------------------------
elif selected_tab == "🌐 Market Competency & Skill Benchmarks":
    st.markdown("""
    <div class="view-header">
        <div class="view-title">🌐 Market Competency & Skill Benchmarks</div>
        <div class="view-subtitle">Official O*NET standardized essential skills, workplace software tools, hot technologies, and role benchmarks.</div>
    </div>
    """, unsafe_allow_html=True)
    
    summary = onet_service.get_onet_analytics_summary()
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Standard Occupations</div><div class="kpi-val">{summary["total_occupations"]:,}</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Workplace Software Tools</div><div class="kpi-val">{summary["unique_software_tools"]:,}</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Hot Technologies</div><div class="kpi-val">{summary["total_hot_technologies"]}</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">In-Demand Usages</div><div class="kpi-val">{summary["total_in_demand_instances"]:,}</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    onet_subtab = st.radio(
        "Intelligence Mode",
        ["🔍 Occupation Skill Explorer", "🔥 Hot Technologies & In-Demand Tools", "🛠️ Software Search & Adoption"],
        horizontal=True,
        key="onet_subtab_radio_widget"
    )
    
    if onet_subtab == "🔍 Occupation Skill Explorer":
        c_search, c_soc = st.columns([3, 7])
        with c_search:
            search_query = st.text_input("Search Occupation Title or SOC", value="Developer", key="onet_occ_search_input")
            matched_occs = onet_service.search_occupations(search_query, limit=15)
            occ_options = {f"{o['title']} ({o['soc_code']})": o['soc_code'] for o in matched_occs}
            if occ_options:
                selected_label = st.selectbox("Select Occupation", list(occ_options.keys()), key="onet_occ_select")
                selected_soc = occ_options[selected_label]
            else:
                st.warning("No occupations found.")
                selected_soc = None
                
        with c_soc:
            if selected_soc:
                ess_skills = onet_service.get_essential_skills_by_soc(selected_soc)
                soft_tools = onet_service.get_software_skills_by_soc(selected_soc, limit=30)
                
                t1, t2 = st.tabs(["Core Essential Skills", "Workplace Software & Tools"])
                with t1:
                    df_ess_view = pd.DataFrame(ess_skills)
                    if not df_ess_view.empty:
                        fig_ess = px.bar(
                            df_ess_view.sort_values(by="Importance", ascending=True),
                            x="Importance",
                            y="Element Name",
                            orientation="h",
                            color="SkillScore",
                            title=f"Core Skills for {selected_soc}",
                            labels={"Element Name": "Skill Element", "Importance": "Importance (1-5)"},
                            template="plotly_white",
                            color_continuous_scale="Blues"
                        )
                        fig_ess.update_layout(
                            height=400,
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)"
                        )
                        st.plotly_chart(fig_ess, use_container_width=True)
                        st.dataframe(df_ess_view[["Element Name", "Importance", "Level", "SkillScore"]], use_container_width=True)
                    else:
                        st.info("No essential skills found for this code.")
                        
                with t2:
                    df_soft_view = pd.DataFrame(soft_tools)
                    if not df_soft_view.empty:
                        st.dataframe(
                            df_soft_view[["SoftwareName", "CategoryName", "IsHotTech", "IsInDemand"]],
                            use_container_width=True
                        )
                    else:
                        st.info("No software skills found for this code.")
                        
    elif onet_subtab == "🔥 Hot Technologies & In-Demand Tools":
        st.markdown("### Top Hot Technologies Across Labor Market Occupations")
        hot_techs = onet_service.get_top_hot_technologies(limit=20)
        df_hot_view = pd.DataFrame(hot_techs)
        fig_hot = px.bar(
            df_hot_view.head(15),
            x="Occurrences",
            y="SoftwareName",
            orientation="h",
            color="InDemandCount",
            title="Top 15 Hot Technologies by Number of Occupations",
            color_continuous_scale="Blues",
            template="plotly_white"
        )
        fig_hot.update_layout(
            yaxis=dict(autorange="reversed"),
            height=450,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_hot, use_container_width=True)
        st.dataframe(df_hot_view, use_container_width=True)
        
    elif onet_subtab == "🛠️ Software Search & Adoption":
        st.markdown("### 🛠️ Labor Market Software Adoption & Tech Penetration")
        st.caption("Search across 15,000+ workplace software tools to analyze occupational demand, hot tech status, and internal role mapping.")

        quick_tools = ["Python", "SQL", "AWS", "Docker", "Salesforce", "Tableau", "Git", "Java", "Kubernetes", "Linux"]
        st.markdown("**🔥 Quick Popular Search Shortcuts:**")
        cols_btn = st.columns(len(quick_tools))
        
        # Initialize search state if not set
        if "onet_soft_search_kw" not in st.session_state:
            st.session_state["onet_soft_search_kw"] = "Python"

        for idx, t_name in enumerate(quick_tools):
            if cols_btn[idx].button(t_name, key=f"quick_tool_btn_{t_name}"):
                st.session_state["onet_soft_search_kw"] = t_name
                st.rerun()

        tool_kw = st.text_input(
            "Search Software Tool / Technology Keyword:",
            value=st.session_state.get("onet_soft_search_kw", "Python"),
            key="onet_soft_search_kw_input",
            help="Type any programming language, cloud platform, enterprise software, or tool name"
        )
        
        if tool_kw:
            results = onet_service.search_software_tools(tool_kw, limit=30)
            if results:
                df_tool_res = pd.DataFrame(results)
                
                # Top matched tool
                top_tool_name = df_tool_res.iloc[0]["SoftwareName"]
                if hasattr(onet_service, "get_software_occupations"):
                    top_tool_occs = onet_service.get_software_occupations(top_tool_name)
                else:
                    df_soft_data = pd.read_csv(PROCESSED_DIR / "onet_software_skills_processed.csv")
                    matches = df_soft_data[df_soft_data["SoftwareName"].str.lower() == top_tool_name.strip().lower()]
                    if matches.empty:
                        matches = df_soft_data[df_soft_data["SoftwareName"].str.lower().str.contains(top_tool_name.strip().lower(), na=False)]
                    unique_occs = matches[["Title", "O*NET-SOC Code", "CategoryName", "IsHotTech", "IsInDemand"]].drop_duplicates()
                    top_tool_occs = unique_occs.rename(columns={
                        "Title": "occupation_title",
                        "O*NET-SOC Code": "soc_code",
                        "CategoryName": "category",
                        "IsHotTech": "is_hot_tech",
                        "IsInDemand": "is_in_demand"
                    }).sort_values(by="is_in_demand", ascending=False).to_dict(orient="records")
                df_top_occs = pd.DataFrame(top_tool_occs)
                
                # Tool Adoption KPI Cards
                total_demanding_occs = len(df_top_occs)
                is_hot = bool(df_tool_res.iloc[0]["is_hot_tech"])
                in_demand_count = int(df_top_occs["is_in_demand"].sum()) if not df_top_occs.empty else 0
                top_category = str(df_tool_res.iloc[0]["CategoryName"])

                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    st.metric("Primary Matched Tool", top_tool_name, delta="Target Query Match")
                with k2:
                    st.metric("Labor Market Occupations", f"{total_demanding_occs:,}", delta=f"{in_demand_count} In-Demand")
                with k3:
                    st.metric("Market Status", "🔥 Hot Technology" if is_hot else "Standard Tool", delta="High Growth" if is_hot else "Stable")
                with k4:
                    st.metric("Primary Category", top_category[:24] + ("..." if len(top_category)>24 else ""))

                st.markdown("---")

                # Layout: Left = Variation Comparisons, Right = Demanding Occupations List
                col_chart, col_occs = st.columns([5, 5])
                
                with col_chart:
                    st.markdown(f"#### 📊 Related '{tool_kw}' Technologies by Occupational Penetration")
                    fig_soft_chart = px.bar(
                        df_tool_res.head(10),
                        x="occupations_count",
                        y="SoftwareName",
                        orientation="h",
                        color="is_in_demand",
                        labels={"occupations_count": "Number of Occupations", "SoftwareName": "Software Tool", "is_in_demand": "High Demand"},
                        color_discrete_map={True: "#2563eb", False: "#93c5fd"},
                        template="plotly_white"
                    )
                    fig_soft_chart.update_layout(
                        yaxis=dict(autorange="reversed"),
                        height=360,
                        margin=dict(l=10, r=10, t=20, b=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig_soft_chart, use_container_width=True)

                with col_occs:
                    st.markdown(f"#### 🏢 Occupations Requiring **{top_tool_name}** ({total_demanding_occs})")
                    if not df_top_occs.empty:
                        df_display_occs = df_top_occs.rename(columns={
                            "occupation_title": "Occupation Title",
                            "soc_code": "SOC Code",
                            "category": "Software Category",
                            "is_hot_tech": "Hot Tech",
                            "is_in_demand": "In Demand"
                        })
                        st.dataframe(df_display_occs, use_container_width=True, height=360)
                    else:
                        st.info("No specific occupation breakdown available.")

                # Internal Organization Match
                st.markdown(f"#### 💼 Internal Organization Role Mapping for **{top_tool_name}**")
                internal_roles = sorted(df_emp["Role"].unique())
                matched_internal = []
                for r in internal_roles:
                    r_words = set(r.lower().split())
                    for occ in top_tool_occs:
                        occ_words = set(occ["occupation_title"].lower().split())
                        if len(r_words.intersection(occ_words)) >= 1:
                            emp_cnt = len(df_emp[df_emp["Role"] == r])
                            matched_internal.append({
                                "Internal Company Role": r,
                                "Active Employees in Cohort": emp_cnt,
                                "Matched O*NET Occupation": occ["occupation_title"],
                                "SOC Code": occ["soc_code"],
                                "High Market Demand": "✅ Yes" if occ["is_in_demand"] else "—"
                            })
                            break
                
                if matched_internal:
                    df_internal_matched = pd.DataFrame(matched_internal)
                    st.dataframe(df_internal_matched, use_container_width=True)
                else:
                    st.info("No direct internal role title match found in company records.")
            else:
                st.warning(f"⚠️ No workplace software tools found matching keyword '{tool_kw}'. Try another term like 'Python', 'AWS', 'SQL', or 'Docker'.")

# -------------------------------------------------------------
# 5. TAB: AI GOVERNANCE & DECISION TRANSPARENCY
# -------------------------------------------------------------
elif selected_tab == "🧠 AI Governance & Decision Transparency":
    st.markdown("""
    <div class="view-header">
        <div class="view-title">🧠 AI Governance & Decision Transparency</div>
        <div class="view-subtitle">Model version registry, cross-algorithm performance comparisons, and global SHAP feature importance.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    - **Active Model**: `{metadata['model_name']}`
    - **Pipeline Version**: `{metadata['version']}`
    - **Algorithm**: `{metadata['algorithm']}`
    - **Training Timestamp**: `{metadata['training_date']}`
    - **Dataset Size**: `{metadata['dataset_size']:,} instances`
    """)
    
    st.subheader("📊 Cross-Model Performance Matrix")
    st.dataframe(pd.DataFrame(metadata["all_model_comparison"]).T, use_container_width=True)
    
    st.subheader("🌐 Global SHAP Feature Importance")
    df_drivers = pd.DataFrame(metadata["top_global_drivers"], columns=["Feature", "Absolute Weight"])
    fig_imp = px.bar(
        df_drivers,
        x="Absolute Weight",
        y="Feature",
        orientation="h",
        color="Absolute Weight",
        color_continuous_scale="Blues",
        template="plotly_white"
    )
    fig_imp.update_layout(
        yaxis=dict(autorange="reversed"),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_imp, use_container_width=True)
