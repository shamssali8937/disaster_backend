# from pydantic import BaseModel

# class ReportResponse(BaseModel):
#     report_id: str
#     disaster_type: str
#     severity: float
#     media_url: str
#     status: str

from pydantic import BaseModel


class ReportResponse(BaseModel):

    report_id: str

    damage_intensity: str

    severity: float

    confidence: float

    pre_image_url: str

    post_image_url: str

    status: str