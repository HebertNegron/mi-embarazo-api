from bson import ObjectId
from models.pyObjectId import PyObjectId
from models.appointment_request import AppointmentRequest
from models.appointment import Appointment
from utils.mongo_conn import MongoConnection
from datetime import datetime

class AppointmentsService:
    def get_appointments(self) -> list[Appointment]:
        with MongoConnection() as db:
            appointments = db.appointments.find()
            return list(Appointment(
                **appointment
            ) for appointment in appointments)
    
    def get_appointment(self, appointment_id: str) -> Appointment | None:
        with MongoConnection() as db:
            appointment = db.appointments.find_one({"_id": ObjectId(appointment_id)})

            if not appointment:
                return None

            return Appointment(**appointment)
        
    def get_appointments_by_doctor(self, doctor_id: PyObjectId | None) -> list[Appointment]:
        with MongoConnection() as db:
            appointments = db.appointments.find({"doctor": doctor_id})
            return list(Appointment(
                **appointment
            ) for appointment in appointments)
        
    def create_appointment(self, appointment: AppointmentRequest) -> dict:
        appointment_data = appointment.model_dump()
        appointment_data["doctor"] = ObjectId(appointment.doctor)
        appointment_data["date"] = datetime.strptime(appointment.date, "%Y-%m-%d")

        with MongoConnection() as db:
            result = db.appointments.insert_one(appointment_data)

            return {
                "_id": str(result.inserted_id)
            } 
        
    def update_appointment(self, appointment_id: str, appointment: Appointment) -> dict | None:
        with MongoConnection() as db:
            result = db.appointments.update_one(
                {"_id": ObjectId(appointment_id)},
                {"$set": appointment.model_dump()}
            )

            return {"_id": str(appointment_id)} if result.modified_count == 1 else None
        
    def delete_appointment(self, appointment_id: str) -> dict | None:
        with MongoConnection() as db:
            result =db.appointments.delete_one({"_id": ObjectId(appointment_id)})
        
            return {"_id": str(appointment_id)} if result.deleted_count == 1 else None