from bson import ObjectId
from models.doctor import Doctor
from utils.mongo_conn import MongoConnection
from datetime import datetime

class DoctorsService:

    def get_doctors(self) -> list[Doctor]:
        with MongoConnection() as db:
            doctors = db.users.find({"role": "doctor"})

            return list(Doctor(**doctor) for doctor in doctors)
        
    def update_doctor(self, doctor_id: str, doctor: Doctor) -> dict | None:
        update_object = doctor.model_dump(exclude={"id", "password"})
        with MongoConnection() as db:
            db.users.update_one(
                {"_id": ObjectId(doctor_id)},
                {"$set": update_object}
            )

            return update_object
        
    def delete_doctor(self, doctor_id: str) -> dict | None:
        with MongoConnection() as db:
            result =db.users.delete_one({"_id": ObjectId(doctor_id)})
        
            return {"_id": str(doctor_id)} if result.deleted_count == 1 else None
        
    def get_schedule(self, doctor_id: str, date: str) -> list[str]:
        isodate = datetime.strptime(date, "%d-%m-%Y")
        with MongoConnection() as db:
            query = {"doctor": ObjectId(doctor_id), "date": isodate}
            doctor_appointments = list(db.appointments.find(query))

            slots = []
            for i in range(8, 18):
                slots.append(str(i) + ":00")

            for appointment in doctor_appointments:
                slots.remove(appointment["time"])

            return slots