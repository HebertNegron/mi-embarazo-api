from pydantic import BaseModel
from models.pyObjectId import PyObjectId

class AppointmentRequest(BaseModel):
    _id: PyObjectId | None = None
    patient: PyObjectId
    doctor: PyObjectId
    file: PyObjectId | None = None
    date: str
    time: str
    date_type: str 
    status: str
    weight: float | None = None
    bloodPressure: str | None = None
    fetalHeartRate: str | None = None
    fetalStatus: str | None = None
    observations: str | None = None
    prescription: str | None = None