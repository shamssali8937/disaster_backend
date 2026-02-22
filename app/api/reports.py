from fastapi import APIRouter, Depends, File, UploadFile
from app.models.ai_model import ai_model
from app.services.firestore_service import db_service
from app.schemas.schemas import ReportResponse
from app.core.role_checker import allow_roles

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/create", response_model=ReportResponse)
async def create_report(
    file: UploadFile = File(...),
    user=Depends(allow_roles(["Citizen"]))
):

    file_bytes = await file.read()

    disaster, severity = ai_model.analyze(file_bytes)

    media_url = db_service.upload_file(file_bytes, file.filename, file.content_type)

    report_id = db_service.create_report(user["uid"], media_url, disaster, severity)

    return ReportResponse(
        report_id=report_id,
        disaster_type=disaster,
        severity=severity,
        media_url=media_url,
        status="Pending"
    )