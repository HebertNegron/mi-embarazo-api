from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId

class AppointmentRequest(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")  # Allow _id to be optional
    patient: Optional[PyObjectId]
    patient_name: Optional[str] = None
    record: Optional[str] = None
    doctor: Optional[PyObjectId] = None
    file: Optional[PyObjectId] = None
    date: Optional[str | datetime] = None
    time: Optional[str] = None
    date_type: Optional[str] = None
    status: Optional[str] = None
    weight: Optional[float] = None
    bloodPressure: Optional[str] = None
    fetalHeartRate: Optional[str] = None
    fetalStatus: Optional[str] = None
    observations: Optional[str] = None
    prescription: Optional[str] = None
