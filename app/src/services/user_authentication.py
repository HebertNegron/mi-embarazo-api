from models.user_model import UserModel
from utils.mongo_conn import MongoConnection

from bson import ObjectId

class UserAuthenticationService:
    def get_user_by_email(self, email: str) -> UserModel | None:
        with MongoConnection() as db:
            user = db.users.find_one({"email": email})
            if user:
                return UserModel(
                    **user
                )

    def save_user(self, user: UserModel) -> UserModel:

        with MongoConnection() as db:
            user_data: dict = {
                "email": user.email,
                "name": user.name,
                "password": user.password,
                "role": user.role
            }

            if user.role == 'doctor':
                user_data["phone"] = user.phone
                user_data["gender"] = user.gender
                user_data["office"] = user.office
                user_data["license"] = user.license
                user_data["specialization"] = user.specialization
            
            user_id = user.id if user.id is not None else ObjectId()

            result = db.users.update_one(
                {"_id": user_id},
                {"$set": user_data},
                upsert=True
            )

            if result.upserted_id:
                user_id = result.upserted_id
            
            new_user: dict = db.users.find_one({"_id": user_id}) or {}

            return UserModel(**new_user)
