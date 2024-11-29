from datetime import datetime
from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId

class Appointment(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")
    patient: PyObjectId
    patient_name: str | None = None
    record: str | None = None
    doctor: PyObjectId
    file: PyObjectId | None = None
    date: str | datetime
    time: str
    date_type: str 
    status: str
    weight: float | None = None
    bloodPressure: str | None = None
    fetalHeartRate: str | None = None
    fetalStatus: str | None = None
    observations: str | None = None
    prescription: str | None = None