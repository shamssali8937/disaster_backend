# from fastapi import APIRouter, File, UploadFile
# from app.models.ai_model import ai_model
# from app.services.firestore_service import db_service
# from app.schemas.schemas import ReportResponse

# router = APIRouter(prefix="/reports", tags=["Reports"])

# @router.post("/create", response_model=ReportResponse)
# async def create_report(file: UploadFile = File(...)):

#     file_bytes = await file.read()

#     # 🔍 AI Prediction
#     disaster, severity = ai_model.analyze(file_bytes)

#     # ☁️ Upload file (optional)
#     media_url = db_service.upload_file(
#         file_bytes, file.filename, file.content_type
#     )

#     # 📝 Save report
#     report_id = db_service.create_report(
#         "anonymous", media_url, disaster, severity
#     )

#     return ReportResponse(
#         report_id=report_id,
#         disaster_type=disaster,
#         severity=severity,
#         media_url=media_url,
#         status="Pending"
#     )






# 2
# from fastapi import APIRouter, File, UploadFile
# from app.models.ai_model import ai_model
# from app.services.firestore_service import db_service
# from app.schemas.schemas import ReportResponse

# router = APIRouter(prefix="/reports", tags=["Reports"])

# @router.post("/create", response_model=ReportResponse)
# async def create_report(file: UploadFile = File(...)):
#     file_bytes = await file.read()

#     # 🔍 AI Prediction (Calling the Hugging Face API)
#     disaster, severity = await ai_model.analyze(file_bytes)

#     # ☁️ Upload file to your service
#     media_url = db_service.upload_file(file_bytes, file.filename, file.content_type)

#     # 📝 Save to Firebase
#     report_id = db_service.create_report("anonymous", media_url, disaster, severity)

#     return ReportResponse(
#         report_id=report_id,
#         disaster_type=disaster,
#         severity=severity,
#         media_url=media_url,
#         status="Pending"
#     )

from fastapi import APIRouter, File, UploadFile
from app.models.ai_model import ai_model
from app.schemas.schemas import ReportResponse

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post(
    "/create",
    response_model=ReportResponse
)
async def create_report(

    pre_image: UploadFile = File(...),
    post_image: UploadFile = File(...)

):

    pre_bytes = await pre_image.read()
    post_bytes = await post_image.read()

    result = await ai_model.analyze(
        pre_image_bytes=pre_bytes,
        post_image_bytes=post_bytes,
        pre_filename=pre_image.filename,
        post_filename=post_image.filename
    )

    return {
        "report_id": "report_123",

        "damage_intensity": result["damage_intensity"],

        "severity": result["severity"],

        "confidence": result["confidence"],

        "pre_image_url": "No Storage Used",

        "post_image_url": "No Storage Used",

        "status": "Pending"
    }