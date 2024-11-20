from pydantic import BaseModel
from models.pyObjectId import PyObjectId

class Appointment(BaseModel):
    _id: PyObjectId | None = None
    patient: PyObjectId
    doctor: PyObjectId
    file: PyObjectId | None = None
    date: str 
    time: str
    date_type: str
    status: str