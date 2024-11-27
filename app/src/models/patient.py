from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId

class PersonalData(BaseModel):
    name: str | None = None
    gender: str | None = None
    phone: str | None = None
    age: int | None = None
    birthDate: str | None = None
    email: str | None = None
    password: str | None = None
    curp: str | None = None
    maritalStatus: str | None = None
    occupation: str | None = None
    address: dict | None = None

class Patient(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")
    record: str | None = None
    name: str | None = None
    personalData: PersonalData | None = None
    current_phone: str | None = None
    doctor_options: list | None = None
    schedule_options: list | None = None
    doctor: str | None = None
    date: str | None = None