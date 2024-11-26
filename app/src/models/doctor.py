from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId

class Doctor(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")
    name: str | None = None
    specialization: str | None = None
    email: str | None = None
    phone: str | None = None
    gender: str | None = None
    password: str | None = None
    office: str | None = None
    license: str | None = None
