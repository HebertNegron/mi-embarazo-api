from pydantic import BaseModel, Field
from models.pyObjectId import PyObjectId

class UserModel(BaseModel):
    id: PyObjectId = Field(None, alias="_id")
    name: str
    last_name: str
    email: str
    password: str
    profile_image: str | None = None
    