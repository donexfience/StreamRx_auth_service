from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.entities.user import User
from domain.interface.user_repository import UserRepository

from infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    async def create(self, user: User, session: AsyncSession) -> User:
        user_model = UserModel(
            email=user.email,
            hashed_password=user.password,
            is_active=user.is_active,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user_model)
        await session.commit()
        await session.refresh(user_model)
        return User.from_orm(user_model)

    async def get_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        result = await session.execute(select(UserModel).where(UserModel.email == email))
        user_model = result.scalars().first()
        return User.from_orm(user_model) if user_model else None

    async def get_by_id(self, id: int, session: AsyncSession) -> Optional[User]:
        user_model = await session.get(UserModel, id)
        return User.from_orm(user_model) if user_model else None
