from passlib.context import CryptContext

from application.interface.password_service import PasswordService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordServiceImpl(PasswordService):
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
