from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schemas import RegisterSchema
from app.services.firestore_service import db_service
from app.core.security import verify_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register(data: RegisterSchema, user=Depends(verify_token)):

    if data.role not in ["Citizen", "NGO", "Admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    db_service.create_user(user["uid"], user.get("email"), data.role)

    return {"message": "User registered successfully"}