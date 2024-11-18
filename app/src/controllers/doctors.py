from fastapi import APIRouter, status, HTTPException, Depends
from models.doctor import Doctor
from services.doctors_service import DoctorsService
from utils.login_required import login_required

doctors_router = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
    dependencies=[
        Depends(
            login_required
        )
    ]
)

@doctors_router.get("")
def get_doctors() -> list[Doctor]:
    doctors: list[Doctor] = DoctorsService().get_doctors()
    return doctors


@doctors_router.get("/{doctor_id}")
def get_doctor(doctor_id: str) -> Doctor:
    doctor: Doctor | None = DoctorsService().get_doctor(doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )
    return doctor


@doctors_router.post("", status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: Doctor) -> dict:
    created_doctor: dict = DoctorsService().create_doctor(doctor)
    return created_doctor


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
    
    
