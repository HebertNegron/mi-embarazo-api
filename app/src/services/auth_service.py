from utils.password_encryptor import PasswordEncryptor
from models.user_model import UserModel
from .user_authentication import UserAuthenticationService

class AuthService:
    def __init__(
        self,
        password_encryptor: PasswordEncryptor,
        user_service: UserAuthenticationService,
    ) -> None:
        self.password_encryptor = password_encryptor
        self.user_service = user_service

    def login(self, email: str, password: str) -> UserModel:
        user = self.user_service.get_user_by_email(email)


        if not user or not self.password_encryptor.verify_password_hash(
            password, user.password
        ):
            raise Exception("Invalid credentials")

        return user

    def signup(self, user: UserModel) -> UserModel:
        if self.user_service.get_user_by_email(user.email):
            raise Exception("This email address is already in use")

        registered_user = self.user_service.save_user(
            UserModel(
                _id=None,
                email=user.email,
                name=user.name,
                password=self.password_encryptor.get_password_hash(user.password),
                role=user.role,
                specialization=user.specialization,
                phone=user.phone,
                gender=user.gender,
                office=user.office,
                license=user.license
            )
        )
        return registered_user
