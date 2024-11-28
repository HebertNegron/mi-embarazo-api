from fastapi import APIRouter, Body, status, HTTPException, Depends
from services.user_authentication import UserAuthenticationService
from services.users_service import UsersService
from models.user_model import UserModel, UserModelRequest
from utils.login_required import login_required
from utils.password_encryptor import PasswordEncryptor


users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[
        Depends(
            login_required
        )
    ]
)
@users_router.get("/by_id")
def get_user(credentials: UserModel = Depends(login_required)) -> UserModel:
    user: UserModel | None = UsersService().get_user(credentials.id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return user

@users_router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: str, user: UserModelRequest) -> dict:
    response: dict | None = UsersService().update_user(user_id, user)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return response

@users_router.post("/verify_password", status_code=status.HTTP_200_OK)
def verify_password(email: str = Body(...), password: str = Body(...)) -> dict:
    user: UserModel | None = UserAuthenticationService().get_user_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    is_valid = PasswordEncryptor().password_context.verify(password, user.password)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    return {"message": "Password is correct"}