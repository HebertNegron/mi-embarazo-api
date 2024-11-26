from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId

class PersonalData(BaseModel):
    name: str
    gender: str
    phone: str
    age: int
    birthDate: str
    email: str
    password: str
    curp: str
    maritalStatus: str
    occupation: str
    address: dict

class Patient(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")
    record: str
    name: str
    personalData: PersonalData | None = None
    current_phone: str | None = None
    doctor_options: list | None = None
    schedule_options: list | None = None
    doctor: str | None = None
    date: str | None = None