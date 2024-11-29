from bson import ObjectId
from models.pyObjectId import PyObjectId
from models.appointment_request import AppointmentRequest
from models.appointment import Appointment
from utils.mongo_conn import MongoConnection
from datetime import datetime

from bson import ObjectId

def serialize_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


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
        
    def get_appointments_by_doctor(self, doctor_id: str | None) -> list[Appointment]:
        with MongoConnection() as db:
            appointments = db.appointments.find({'doctor': str(doctor_id)})
            return [Appointment(**appointment) for appointment in appointments]
        
    def create_appointment(self, appointment: AppointmentRequest) -> dict:
        appointment_data = appointment.model_dump()
        appointment_data["_id"] = ObjectId()  # Generate a new ObjectId for the document
        appointment_data["doctor"] = ObjectId(appointment.doctor)  # Convert doctor to ObjectId
        appointment_data["date"] = datetime.strptime(appointment.date, "%Y-%m-%d")  # Parse date
        
        with MongoConnection() as db:
            # Insert the document into the database
            result = db.appointments.insert_one(appointment_data)
            
            # Retrieve the inserted document using the inserted ID
            inserted_document = db.appointments.find_one({"_id": result.inserted_id})
            
            # Convert ObjectId fields to strings for serialization
            if inserted_document:
                inserted_document["_id"] = str(inserted_document["_id"])
                if "doctor" in inserted_document:
                    inserted_document["doctor"] = str(inserted_document["doctor"])
                if "patient" in inserted_document:
                    inserted_document["patient"] = str(inserted_document["patient"])

            return inserted_document
        
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