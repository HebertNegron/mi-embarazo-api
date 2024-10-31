from passlib.context import CryptContext

class PasswordEncryptor():
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def get_password_hash(password: str) -> str:
        return PasswordEncryptor.password_context.hash(password)

    @staticmethod
    def verify_password_hash(password: str, hashed_password: str) -> bool:
        return PasswordEncryptor.password_context.verify(
            password, hashed_password
        )
