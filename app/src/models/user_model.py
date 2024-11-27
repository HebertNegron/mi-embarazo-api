from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId
from typing import Literal

UserRoles = Literal["doctor", "admin"]

class UserModel(BaseModel):
    id: PyObjectId | None = Field(None, alias="_id")
    name: str
    password: str
    role: UserRoles
    profile_image: str | None = None
    specialization: str | None = None
    email: str
    phone: str | None = None
    gender: str | None = None
    office: str | None = None
    license: str | None = None

class UserModelRequest(BaseModel):
    name: str | None = None
    password: str | None = None
    role: UserRoles | None = None
    profile_image: str | None = None
    specialization: str | None = None
    email: str | None = None
    phone: str | None = None
    gender: str | None = None
    office: str | None = None
    license: str | None = None