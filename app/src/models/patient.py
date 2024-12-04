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
    address: str | None = None
    maritalStatus: str | None = None
    street: str | None = None
    municipality: str | None = None
    locality: str | None = None
    state: str | None = None

class PregnancyData(BaseModel):
    lastMenstruation: str | None = None
    dueDate : str | None = None
    gestationStage : str | None = None
    previousPregnancies : int | None = None
    abortions : int | None = None
    pregnancyType : str | None = None
    complication : str | None = None
    observations : str | None = None

class MedicalHistory(BaseModel):
    medicalConditions: str | None = None
    gynecologicalHistory: str | None = None
    allergies : str | None = None
    familyHistory : str | None = None

class Patient(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")
    record: str | None = None
    name: str | None = None
    personalData: PersonalData | None = None
    last_appointment_id: PyObjectId | None = None
    last_appointment: str | None = None
    current_phone: str | None = None
    doctor_options: list | None = None
    schedule_options: list | None = None
    doctor: PyObjectId | None = None
    date: str | None = None
    pregnancyData: PregnancyData | None = None
    medicalHistory: MedicalHistory | None = None