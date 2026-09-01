from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import attrition, dashboard, skills, onet
from app.utils.logger import logger
from app.ml.model_loader import ModelManager

app = FastAPI(
    title="Enterprise HR AI - Workforce Intelligence & Upskilling API",
    description="Agentic workforce intelligence system predicting attrition, measuring engagement, identifying skill gaps, and recommending upskilling courses.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML model at startup
@app.on_event("startup")
def startup_event():
    logger.info("Initializing Enterprise HR AI API Services...")
    ModelManager.get_instance()
    logger.info("Services and Model Pipeline are ready.")

# Mount routers
app.include_router(attrition.router)
app.include_router(dashboard.router)
app.include_router(skills.router)
app.include_router(onet.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Enterprise HR AI - Workforce Intelligence Platform",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
