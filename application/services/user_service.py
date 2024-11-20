from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from application.interface.password_service import PasswordService
from domain.entities.user import User
from domain.interface.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service

    async def authenticate_user(self, username: str, password: str, session: AsyncSession) -> User:
        user = await self.user_repository.get_by_email(username)
        if (user and self.password_service.verify_password(password, user.password)):
            return user
            raise HTTPException(status_code=400, detail="Incorrect username or password")
