from fastapi import APIRouter

from fastapi import status
from fastapi.exceptions import HTTPException

from services.patients_service import PatientsService
from models.patient import Patient

patients_router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)

@patients_router.get("")
def get_patients() -> list[Patient]:
    patients: list[Patient] = PatientsService().get_patients()
    return patients


@patients_router.get("/{patient_id}")
def get_patient(patient_id: str) -> Patient:
    patient: Patient | None = PatientsService().get_patient(patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return patient


@patients_router.post("")
def create_patient(patient: Patient) -> dict:
    created_patient: dict = PatientsService().create_patient(patient)
    return created_patient


@patients_router.put("/{patient_id}")
def update_patient(patient_id: str, patient: Patient) -> dict:
    response: dict | None = PatientsService().update_patient(patient_id, patient)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return response


@patients_router.delete("/{patient_id}")
def delete_patient(patient_id: str) -> dict:
    patient: dict | None = PatientsService().delete_patient(patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return patient
    
    