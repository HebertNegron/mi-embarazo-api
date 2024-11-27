from models.pyObjectId import PyObjectId
from models.user_model import UserModel, UserModelRequest
from utils.mongo_conn import MongoConnection
from bson import ObjectId

class UsersService:
    def get_user(self, user_id: PyObjectId | None) -> UserModel | None:
        with MongoConnection() as db:
            user = db.users.find_one({"_id": user_id})

            if not user:
                return None

            return UserModel(**user)
        
    def update_user(self,  user_id: str, user: UserModelRequest) -> dict | None:
        update_object = user.model_dump(exclude={"id", "password"}, exclude_none=True)
        with MongoConnection() as db:
            result = db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_object}
            )

            return {"_id": str(user_id)} if result.modified_count == 1 else None