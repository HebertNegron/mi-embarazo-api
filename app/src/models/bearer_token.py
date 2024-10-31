from pydantic import BaseModel


class BearerToken(BaseModel):
    access_token: str
    user_email: str
    user_id: str
    user_last_name: str
    user_name: str
    user_profile_image: str
