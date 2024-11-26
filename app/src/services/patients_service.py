from bson import ObjectId
from models.patient import Patient
from utils.mongo_conn import MongoConnection

class PatientsService:

    def get_patients(self) -> list[Patient]:
        with MongoConnection() as db:
            patients = db.patients.find()

            return list(Patient(**patient) for patient in patients)
        
    def get_patient(self, patient_id: str) -> Patient | None:
        with MongoConnection() as db:
            patient = db.patients.find_one({"_id": ObjectId(patient_id)})

            if not patient:
                return None

            return Patient(**patient)
        
    def get_patient_by_phone(self, phone: str) -> dict | None:
        with MongoConnection() as db:
            patient = db.patients.find_one({"personalData.phone": phone})

            if not patient:
                return None

            return patient
        
    def create_patient(self, patient: Patient) -> dict:
        with MongoConnection() as db:
            result = db.patients.insert_one(patient.model_dump())

            return {
                "_id": str(result.inserted_id)
            } 
        
    def update_patient(self, patient_id: str, patient: Patient) -> dict | None:
        with MongoConnection() as db:
            result = db.patients.update_one(
                {"_id": ObjectId(patient_id)},
                {"$set": patient.model_dump()}
            )

            return {"_id": str(patient_id)} if result.modified_count == 1 else None
        
    def delete_patient(self, patient_id: str) -> dict | None:
        with MongoConnection() as db:
            result =db.patients.delete_one({"_id": ObjectId(patient_id)})
        
            return {"_id": str(patient_id)} if result.deleted_count == 1 else None