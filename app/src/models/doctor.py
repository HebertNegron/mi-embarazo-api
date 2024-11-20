from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId

class Doctor(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")
    name: str
    major: str
    email: str
    phone: str
    gender: str
    password: str
    office: str
    professional_license: str