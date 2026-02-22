from fastapi import APIRouter, Depends
from app.core.role_checker import allow_roles
from app.core.config import db

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/reports")
async def get_all_reports(user=Depends(allow_roles(["Admin"]))):

    docs = db.collection("Reports").stream()
    return [doc.to_dict() for doc in docs]