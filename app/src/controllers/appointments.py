from fastapi import APIRouter, status, HTTPException, Depends
from models.user_model import UserModel
from models.appointment_request import AppointmentRequest
from models.appointment import Appointment
from services.appointments_service import AppointmentsService
from utils.login_required import login_required


appointments_router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
    dependencies=[
        Depends(
            login_required
        )
    ]
)

@appointments_router.get("")
def get_appointments() -> list[Appointment]:
    appointments: list[Appointment] = AppointmentsService().get_appointments()
    return appointments

@appointments_router.get("/doctors")
def get_appointments_by_doctor(credentials: UserModel = Depends(login_required)) -> list[Appointment]:
    appointments: list[Appointment] = AppointmentsService().get_appointments_by_doctor(credentials.id)
    return appointments

@appointments_router.get("/patients/{patient_id}")
def get_appointments_by_patients(patient_id: str) -> list[Appointment]:
    appointments: list[Appointment] = AppointmentsService().get_appointments_by_patient(patient_id)
    return appointments

@appointments_router.get("/{appointment_id}")
def get_appointment(appointment_id: str) -> Appointment:
    appointment: Appointment | None = AppointmentsService().get_appointment(appointment_id)

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    return appointment


@appointments_router.post("", status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: AppointmentRequest) -> dict:
    created_appointment: dict = AppointmentsService().create_appointment(appointment)
    return created_appointment


@appointments_router.put("/{appointment_id}", status_code=status.HTTP_200_OK)
def update_appointment(appointment_id: str, appointment: Appointment) -> dict:
    response: dict | None = AppointmentsService().update_appointment(appointment_id, appointment)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    return response


@appointments_router.delete("/{appointment_id}", status_code=status.HTTP_200_OK)
def delete_appointment(appointment_id: str) -> dict:
    appointment: dict | None = AppointmentsService().delete_appointment(appointment_id)

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    return appointment
    
    