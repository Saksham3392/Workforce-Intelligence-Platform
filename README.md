# Enterprise HR AI — Workforce Intelligence & Upskilling Platform

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7.svg?logo=render&logoColor=white)](https://render.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, end-to-end People Analytics & Agentic AI platform that predicts employee flight risk, monitors workforce health metrics, diagnoses organizational skill deficits using standardized O*NET benchmarks, and simulates retention interventions in real time.

---

### 🌐 Live Interactive Demo
Experience the platform in action directly in your browser without local setup:  
👉 **https://workforce-intelligence-platform-xsqx.onrender.com**

And to view in localhost offline
```cmd
cd /d "c:\Users\Asus\Downloads\CSE AI 5th Sem\AGAI\Projects\AGAI Project" && set PYTHONPATH=. && start http://localhost:8501 && python -m streamlit run frontend/app.py
```

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           HR & MARKET DATA SOURCES                      │
│      Employee Master  •  Performance & Engagement  •  O*NET Standards   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      DATA FOUNDATION & SCHEMA VALIDATION                │
│            Pydantic v2 Schema  •  Normalization  •  Feature Joins       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            ▼                        ▼                        ▼
    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
    │  ML ENGINE   │         │  ENGAGEMENT  │         │  SKILL GAP   │
    │  & SHAP XAI  │         │  ANALYTICS   │         │  & O*NET DB  │
    └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
           │                        │                        │
    Calibrated Risk (0-1)     Engagement Index       Set-Difference Deficits
    SHAP Feature Weights      Department Rollups     Personalized Pathways
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   UNIFIED SINGLE SOURCE OF TRUTH                        │
│                `employee_intelligence.csv` Database                     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
            ┌────────────────────────┴────────────────────────┐
            ▼                                                 ▼
┌─────────────────────────────┐                     ┌─────────────────────┐
│       FASTAPI BACKEND       │                     │ STREAMLIT DASHBOARD │
│  REST API & Audit Logging   │                     │ Executive Cockpit   │
└─────────────────────────────┘                     └─────────────────────┘
```

---

## 🏢 Business Metrics & Analytics Modules

The interactive dashboard is organized into 5 core business metric domains:

1. **📊 Workforce Health & Retention KPIs**
   - Organization-wide retention rates, active flight risk breakdown (`HIGH`, `MEDIUM`, `LOW`), department turnover exposure rollups, and searchable workforce master headcount rosters.

2. **🔍 Talent Risk & Capability Diagnostics**
   - 360-degree employee profile drill-down, verified skill inventory vs. role requirements, and **⚡ Real-Time What-If Retention Cockpit** (adjust compensation, workload, and promotion levers to project risk mitigation in real time).

3. **⚡ Predictive Attrition Risk Scoring**
   - On-demand candidate and employee flight risk assessment powered by machine learning with strict Pydantic v2 schema validation and top feature risk weight attribution.

4. **🌐 Market Competency & Skill Benchmarks**
   - Official O*NET standardized occupational competencies, hot labor market technologies, and software search with adoption metrics across 15,000+ workplace tools.

5. **🧠 AI Governance & Decision Transparency**
   - Model version registry, cross-algorithm evaluation matrix (Logistic Regression, Random Forest, XGBoost with ROC-AUC > 0.98), and global SHAP explainability feature weights.

---

## 📂 Project Repository Structure

```
AGAI Project/
├── app/
│   ├── api/                  # FastAPI REST route controllers
│   ├── ml/                   # Model loader, metadata & inference engine
│   ├── services/             # Core business logic (Attrition, O*NET, Skill Gap)
│   ├── utils/                # Config, dynamic paths, and logging
│   ├── validation/           # Pydantic v2 request/response schemas
│   └── main.py               # FastAPI application entrypoint
├── data/
│   ├── raw/                  # Source CSV datasets
│   ├── processed/            # Normalized, cleaned, and joined datasets
│   └── predictions/          # Live prediction audit logs
├── frontend/
│   └── app.py                # Streamlit Executive Intelligence Platform
├── models/
│   └── v1/                   # Serialized ML pipeline (.pkl) & metadata.json
├── notebooks/                # 16 Step-by-step exploratory analysis notebooks
├── tests/                    # 28 Automated unit and integration tests
├── .dockerignore             # Docker build exclusions
├── .gitignore                # Git version control exclusions
├── Dockerfile                # Production multi-service container spec
├── docker-compose.yml        # Docker compose configuration
├── render.yaml               # Render Infrastructure-as-Code Blueprint
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Quickstart: Local Development

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/<your-username>/enterprise-hr-ai-platform.git
cd enterprise-hr-ai-platform

# Create and activate virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run Automated Tests
```bash
pytest -v
```

### 4. Launch Application Services

**Launch Streamlit Frontend:**
```bash
streamlit run frontend/app.py
```
> Open [http://localhost:8501](http://localhost:8501) in your browser.

**Launch FastAPI Backend (Optional / REST API):**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
> Access Swagger API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 🐳 Docker Deployment

### Run with Docker:
```bash
# Build the container image
docker build -t enterprise-hr-ai-platform .

# Run container (Maps Streamlit to port 8501 and FastAPI to 8000)
docker run -p 8501:8501 -p 8000:8000 enterprise-hr-ai-platform
```

### Run with Docker Compose:
```bash
docker-compose up --build
```

---

## 🌐 How to Deploy to Render

Deploying this platform to [Render](https://render.com) is straightforward and supports zero-downtime hosting.

### Method 1: Deploy with Docker (Recommended)
1. **Push your code to GitHub** (see instructions below).
2. Go to your [Render Dashboard](https://dashboard.render.com/) and click **New +** ➔ **Web Service**.
3. Connect your GitHub repository.
4. Select **Docker** as the Runtime environment.
5. Set the following settings:
   - **Name**: `enterprise-hr-ai-platform`
   - **Branch**: `main`
   - **Region**: Closest to your users (e.g. Oregon, Frankfurt, Singapore)
   - **Instance Type**: `Free` or `Starter`
6. Add Environment Variables:
   - `PORT` = `8501`
   - `PYTHONUNBUFFERED` = `1`
7. Click **Deploy Web Service**. Render will build the `Dockerfile` and publish your platform.

### Method 2: Deploy with Render Blueprint (`render.yaml`)
1. In Render, select **New +** ➔ **Blueprint**.
2. Select your repository. Render will automatically detect [`render.yaml`](render.yaml) and configure the deployment with one click.

---

## 📤 How to Push to GitHub

Follow these steps to initialize and push this codebase to GitHub:

```bash
# 1. Initialize Git repository
git init

# 2. Add all project files
git add .

# 3. Commit your changes
git commit -m "Initial commit: Enterprise HR AI Workforce Intelligence Platform"

# 4. Set default branch to main
git branch -M main

# 5. Link to your remote GitHub repository
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# 6. Push code to GitHub
git push -u origin main
```

---

## 📡 REST API Reference

The FastAPI backend provides production-ready endpoints for programmatic integration:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/predict/attrition` | Run ML flight risk inference on an employee payload |
| `GET` | `/dashboard/summary` | Retrieve executive workforce overview metrics |
| `GET` | `/dashboard/attrition-by-department` | Departmental attrition risk distribution |
| `GET` | `/dashboard/skill-gaps` | Organization-wide missing skill deficits & severity tiers |
| `GET` | `/dashboard/recommendations` | High-risk employee personalized upskilling pathways |
| `GET` | `/employees/{employee_id}` | 360-degree profile and verified skills for an employee |
| `GET` | `/skills/courses` | Catalog of accredited AI upskilling courses |
| `GET` | `/health` | System health and model readiness check |

---

## 🧪 Model Performance & Evaluation

The attrition risk engine was benchmarked across multiple algorithms:

| Algorithm | ROC-AUC | Precision (High Risk) | Recall (High Risk) | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **XGBoost Classifier (Production)** | **0.985** | **0.912** | **0.884** | **0.898** |
| Random Forest | 0.978 | 0.895 | 0.862 | 0.878 |
| Logistic Regression | 0.884 | 0.791 | 0.745 | 0.767 |

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
