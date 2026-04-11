from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import reports

app = FastAPI(title="Disaster Severity Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Only ONE router
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Backend running"}