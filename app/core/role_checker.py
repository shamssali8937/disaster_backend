from fastapi import Depends, HTTPException
from app.core.security import verify_token
from app.core.config import db

def allow_roles(roles: list):

    def role_dependency(user=Depends(verify_token)):

        user_doc = db.collection("Users").document(user["uid"]).get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not registered")

        role = user_doc.to_dict().get("role")

        if role not in roles:
            raise HTTPException(status_code=403, detail="Access denied")

        return user

    return role_dependency