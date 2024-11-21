import strawberry
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info

from application.interface.password_service import PasswordService
from application.services.jwt_token_service import JWTTokenService
from application.use_cases.auth_use_cases import AuthUseCases

from infrastructure.database.connection import get_db_session
from infrastructure.repositories.user_repository import UserRepositoryImpl

from presentation.graphql.schema import UserRegistrationInput, UserType, UserLoginInput, AuthResponse


async def get_auth_use_cases(session: AsyncSession = Depends(get_db_session())):
    user_repository = UserRepositoryImpl(session)
    password_service = PasswordService()
    token_service = JWTTokenService()
    return AuthUseCases(user_repository, password_service, token_service)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register(self, input: UserRegistrationInput, info: Info) -> UserType:
        # Add input validation
        if not input.email or not input.password:
            raise ValueError("Email and password are required")

        session: AsyncSession = info.context['db']
        auth_use_cases = await get_auth_use_cases(session)
        user = await auth_use_cases.register_user(email=input.email, password=input.password)
        return UserType(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    @strawberry.mutation
    async def login(
        self,
        input: UserLoginInput,
        auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
    ) -> AuthResponse:
        access_token = await auth_use_cases.login_user(
            email=input.email,
            password=input.password
        )
        return AuthResponse(access_token=access_token)