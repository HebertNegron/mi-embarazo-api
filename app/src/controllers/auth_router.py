from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models.user_model import UserModel
from models import BearerToken
from utils.password_encryptor import PasswordEncryptor

from services import AuthService, UserAuthenticationService
from utils.json_web_token_tools import JsonWebTokenTools

auth_router = APIRouter()
auth_service = AuthService(
    password_encryptor=PasswordEncryptor(),
    user_service=UserAuthenticationService(),
)


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> BearerToken:
    try:
        user = auth_service.login(email=user_data.username, password=user_data.password)

        return BearerToken(
            access_token=JsonWebTokenTools.create_access_token(user.email),
            user_email=user.email,
            user_id=str(user.id),
            user_name=user.name,
            role=user.role
        )
    except Exception:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup_user(user: UserModel) -> BearerToken:
    try:
        user = auth_service.signup(user)

        return BearerToken(
            access_token=JsonWebTokenTools.create_access_token(user.email),
            user_email=user.email,
            user_id=str(user.id),
            user_name=user.name,
            role=user.role
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email address is already in use",
        )
    
