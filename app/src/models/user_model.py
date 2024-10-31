from typing import Annotated
from bson import ObjectId
from pydantic import AfterValidator, BaseModel

ObjectIdStr = Annotated[str, AfterValidator(lambda v: ObjectId.is_valid(v))]

class UserModel(BaseModel):
    id: ObjectIdStr | None = None
    name: str
    last_name: str
    email: str
    password: str
    profile_image: str | None = None
    