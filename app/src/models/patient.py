from pydantic import BaseModel, AfterValidator
from bson import ObjectId
from typing import Annotated

ObjectIdStr = Annotated[str, AfterValidator(lambda v: ObjectId.is_valid(v))]


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
    _id: ObjectIdStr | None = None
    record: str
    personalData: PersonalData