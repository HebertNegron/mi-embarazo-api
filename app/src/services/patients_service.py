from bson import ObjectId
from models.pyObjectId import PyObjectId
from models.patient import Patient
from utils.mongo_conn import MongoConnection

class PatientsService:

    def get_patients(self) -> list[Patient]:
        with MongoConnection() as db:
            patients = db.patients.find()

            return list(Patient(**patient) for patient in patients)
        
    def get_patients_by_doctor(self, doctor_id: str | None) -> list[Patient]:
        with MongoConnection() as db:
            patients = db.patients.find({"doctor": str(doctor_id)})

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
        if patient.doctor:
            patient.doctor = ObjectId(patient.doctor) 
        with MongoConnection() as db:
            result = db.patients.update_one(
                {"_id": ObjectId(patient_id)},
                {"$set": patient.model_dump(exclude={"id"}, exclude_none=True)}
            )

            return {"_id": str(patient_id)} if result.modified_count == 1 else None
        
    def delete_patient(self, patient_id: str) -> dict | None:
        with MongoConnection() as db:
            result =db.patients.delete_one({"_id": ObjectId(patient_id)})
        
            return {"_id": str(patient_id)} if result.deleted_count == 1 else None
    
    def save_last_appointment(self, patient_id: str, appointment_id: str, appointment_date: str) -> dict:
        with MongoConnection() as db:
            result = db.patients.update_one(
                {"_id": ObjectId(patient_id)},
                {"$set": {
                    "last_appointment_id": appointment_id,
                    "last_appointment": appointment_date
                }}
            )
            return {"_id": str(patient_id)} if result.modified_count == 1 else None
