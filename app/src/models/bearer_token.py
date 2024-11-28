from pydantic import BaseModel


class BearerToken(BaseModel):
    access_token: str
    user_email: str
    user_id: str
    user_name: str
    user_phone: str | None = None
    role: str