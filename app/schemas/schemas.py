from pydantic import BaseModel

class RegisterSchema(BaseModel):
    role: str

class ReportResponse(BaseModel):
    report_id: str
    disaster_type: str
    severity: float
    media_url: str
    status: str