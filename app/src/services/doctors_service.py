from bson import ObjectId
from models.doctor import Doctor
from utils.mongo_conn import MongoConnection

class DoctorsService:

    def get_doctors(self) -> list[Doctor]:
        with MongoConnection() as db:
            doctors = db.doctors.find()

            return list(Doctor(**doctor) for doctor in doctors)
        
    def get_doctor(self, doctor_id: str) -> Doctor | None:
        with MongoConnection() as db:
            doctor = db.doctors.find_one({"_id": ObjectId(doctor_id)})

            if not doctor:
                return None

            return Doctor(**doctor)
        
    def create_doctor(self, doctor: Doctor) -> dict:
        with MongoConnection() as db:
            result = db.doctors.insert_one(doctor.model_dump())

            return {
                "_id": str(result.inserted_id)
            } 
        
    def update_doctor(self, doctor_id: str, doctor: Doctor) -> dict | None:
        with MongoConnection() as db:
            result = db.doctors.update_one(
                {"_id": ObjectId(doctor_id)},
                {"$set": doctor.model_dump()}
            )

            return {"_id": str(doctor_id)} if result.modified_count == 1 else None
        
    def delete_doctor(self, doctor_id: str) -> dict | None:
        with MongoConnection() as db:
            result =db.doctors.delete_one({"_id": ObjectId(doctor_id)})
        
            return {"_id": str(doctor_id)} if result.deleted_count == 1 else None