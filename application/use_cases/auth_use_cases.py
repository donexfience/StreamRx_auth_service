from sqlalchemy.util import has_dupes, await_only

from domain.entities.user import User
from domain.interface.user_repository import UserRepository
from application.interface.password_service import PasswordService


class AuthUseCases:
    def __init__(
            self,
            user_repository: UserRepository,
            password_service: PasswordService
    ):
        self.user_repository = user_repository
        self.password_service = password_service

    async def register_user(self, email: str, password: str) -> User:
        existing_user = await  self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("user already existed")
        hashed_password = self.password_service.hash_password(password)
        user = User(id=None, email=email, hashed_password=hashed_password)
        return await self.user_repository.create(user)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("User not found")

        if not self.password_service.verify_password(password, user.hashed_password):
            raise ValueError("Invalid password")

        return user
