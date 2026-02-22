from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, reports, admin, webhooks

app = FastAPI(title="Disaster Severity Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(reports.router)
app.include_router(admin.router)
app.include_router(webhooks.router)

@app.get("/")
def root():
    return {"message": "Backend running"}