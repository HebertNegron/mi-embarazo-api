from models.user_model import UserModel
from utils.mongo_conn import MongoConnection

from bson import ObjectId

class UserAuthenticationService:
    def get_user_by_email(self, email: str) -> UserModel | None:
        with MongoConnection() as db:
            user = db.users.find_one({"email": email})
            
            if user:
                return UserModel(
                    **user,
                    id=str(user["_id"])
                )

    def save_user(self, user: UserModel) -> UserModel:
        with MongoConnection() as db:
            user_data: dict = {
                "email": user.email,
                "last_name": user.last_name,
                "name": user.name,
                "password": user.password,
            }
            
            if user.id:
                user_id = ObjectId(user.id)
            else:
                user_id = None

            result = db.users.update_one(
                {"_id": user_id} if user_id else {},
                {"$set": user_data},
                upsert=True
            )

            if result.upserted_id:
                user_id = result.upserted_id
            
            new_user:dict = db.users.find_one({"_id": user_id}) or {}

            return UserModel(**new_user)
