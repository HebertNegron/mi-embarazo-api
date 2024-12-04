from fastapi import APIRouter, Body, status, HTTPException, Depends
from models.user_model import UserModel
from services import AuthService, UserAuthenticationService
from models.doctor import Doctor
from services.doctors_service import DoctorsService
from utils.login_required import login_required
from utils.password_encryptor import PasswordEncryptor


doctors_router = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
    dependencies=[
        Depends(
            login_required
        )
    ]
)
auth_service = AuthService(
    password_encryptor=PasswordEncryptor(),
    user_service=UserAuthenticationService(),
)

@doctors_router.get("")
def get_doctors() -> list[Doctor]:
    doctors: list[Doctor] = DoctorsService().get_doctors()
    return doctors

@doctors_router.get("/{doctor_id}", status_code=status.HTTP_200_OK)
def get_doctor(doctor_id: str) -> Doctor:
    doctor: Doctor = DoctorsService().get_doctor(doctor_id)

    return doctor


@doctors_router.put("/{doctor_id}", status_code=status.HTTP_200_OK)
def update_doctor(doctor_id: str, doctor: Doctor) -> dict:
    response: dict | None = DoctorsService().update_doctor(doctor_id, doctor)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )
    return response


@doctors_router.delete("/{doctor_id}", status_code=status.HTTP_200_OK)
def delete_doctor(doctor_id: str) -> dict:
    doctor: dict | None = DoctorsService().delete_doctor(doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )
    return doctor

@doctors_router.post("/get_schedule/{doctor_id}", status_code=status.HTTP_200_OK)
def get_schedule(doctor_id: str, date: str = Body(embed=True)) -> list:
    schedule: list = DoctorsService().get_schedule(doctor_id, date)

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )
    return schedule
    
