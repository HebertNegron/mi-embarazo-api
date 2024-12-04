from datetime import datetime
from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId

class Appointment(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")
    patient: PyObjectId | None = None
    patient_name: str | None = None
    record: str | None = None
    doctor: PyObjectId | None = None
    file: PyObjectId | None = None
    date: str | datetime | None = None
    time: str | None = None
    date_type: str | None = None
    status: str | None = None
    weight: float | None = None
    bloodPressure: str | None = None
    fetalHeartRate: str | None = None
    fetalStatus: str | None = None
    observations: str | None = None
    prescription: str | None = None