from utils.password_encryptor import PasswordEncryptor
from models.doctor import Doctor
from .user_authentication import UserAuthenticationService

class AuthService:
    def __init__(
        self,
        password_encryptor: PasswordEncryptor,
        user_service: UserAuthenticationService,
    ) -> None:
        self.password_encryptor = password_encryptor
        self.user_service = user_service

    def login(self, email: str, password: str) -> Doctor:
        
        user = self.user_service.get_user_by_email(email)

        if not user or not self.password_encryptor.verify_password_hash(
            password, user.password
        ):
            raise Exception("Invalid credentials")

        return user

    def signup(self, user: Doctor) -> Doctor:
        if self.user_service.get_user_by_email(user.email):
            raise Exception("This email address is already in use")

        registered_user = self.user_service.save_user(
            Doctor(
                _id=None,
                email=user.email,
                name=user.name,
                password=self.password_encryptor.get_password_hash(user.password),
                major=user.major,
                phone=user.phone,
                gender=user.gender,
                office=user.office,
                professional_license=user.professional_license
            )
        )
        return registered_user
