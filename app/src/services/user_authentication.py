from models.doctor import Doctor
from utils.mongo_conn import MongoConnection

from bson import ObjectId

class UserAuthenticationService:
    def get_user_by_email(self, email: str) -> Doctor | None:
        with MongoConnection() as db:
            user = db.doctors.find_one({"email": email})
            
            if user:
                return Doctor(
                    **user
                )

    def save_user(self, user: Doctor) -> Doctor:
        with MongoConnection() as db:
            user_data: dict = {
                "email": user.email,
                "name": user.name,
                "password": user.password,
                "major": user.major,
                "phone": user.phone,
                "gender": user.gender,
                "office": user.office,
                "professional_license": user.professional_license
            }
            
            user_id = user.id if user.id is not None else ObjectId()

            result = db.doctors.update_one(
                {"_id": user_id},
                {"$set": user_data},
                upsert=True
            )

            if result.upserted_id:
                user_id = result.upserted_id
            
            new_user:dict = db.doctors.find_one({"_id": user_id}) or {}

            return Doctor(**new_user)
