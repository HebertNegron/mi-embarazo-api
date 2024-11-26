from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId
from typing import Literal

UserRoles = Literal["doctor", "admin"]

class UserModel(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")
    name: str
    email: str
    password: str
    role: UserRoles
    profile_image: str | None = None
    major: str | None = None
    phone: str | None = None
    gender: str | None = None
    office: str | None = None
    professional_license: str | None = None