from jose import JWTError
from typing import Annotated
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from models.user_model import UserModel
from utils.json_web_token_tools import JsonWebTokenTools
from services.user_authentication import UserAuthenticationService


async def login_required(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="auth/login")
)]):
    credentials_exception = HTTPException(
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )

    try:
        token_payload = JsonWebTokenTools.validate_access_token(token)

        user_email = token_payload.get("sub")

        if user_email is None:
            raise credentials_exception

        user_repository = UserAuthenticationService()
        user = user_repository.get_user_by_email(user_email)
        if user is None or not user.id:
            raise credentials_exception


        return UserModel(
            email=user.email, id=user.id, last_name=user.last_name, name=user.name
        )
    except JWTError:
        raise credentials_exception
