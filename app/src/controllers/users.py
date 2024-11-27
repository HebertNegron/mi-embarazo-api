from fastapi import APIRouter, status, HTTPException, Depends
from services.users_service import UsersService
from models.user_model import UserModel, UserModelRequest
from utils.login_required import login_required


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