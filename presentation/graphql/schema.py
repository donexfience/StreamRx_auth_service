import strawberry
from typing import List, Optional
from fastapi import Depends, HTTPException
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.auth_use_cases import AuthUseCases
from infrastructure.database.connection import get_db_session
from infrastructure.repositories.user_repository import UserRepositoryImpl
from presentation.graphql.types import UserRegistrationInput, UserType, UserLoginInput, AuthResponse
from infrastructure.services.password_service_impl import PasswordServiceImpl
from application.services.jwt_token_service import JWTTokenService


async def get_auth_use_cases(session: AsyncSession = Depends(get_db_session)) -> AuthUseCases:
    user_repository = UserRepositoryImpl()
    password_service = PasswordServiceImpl()
    token_service = JWTTokenService()
    return AuthUseCases(user_repository, password_service, token_service)


@strawberry.type
class Query:
    @strawberry.field
    async def current_user(self, info: Info) -> Optional[UserType]:
        user = info.context.get("current_user")
        if user:
            return UserType(
                id=user.id,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        return None

    @strawberry.field
    async def list_users(self, info: Info) -> List[UserType]:
        session: AsyncSession = info.context['db']
        user_repository = UserRepositoryImpl()
        users = await user_repository.get_all(session)
        return [UserType(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        ) for user in users]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register(self, input: UserRegistrationInput, info: Info) -> UserType:
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
    async def login(self, input: UserLoginInput, info: Info) -> AuthResponse:
        session: AsyncSession = info.context['db']
        auth_use_cases = await get_auth_use_cases(session)
        access_token = await auth_use_cases.login_user(email=input.email, password=input.password)
        return AuthResponse(access_token=access_token)

    @strawberry.mutation
    async def refresh_token(self, refresh_token: str, info: Info) -> AuthResponse:
        session: AsyncSession = info.context['db']
        token_service = JWTTokenService()
        payload = token_service.decode_token(refresh_token)
        user_id = payload.get("sub")
        user_repository = UserRepositoryImpl()
        user = await user_repository.get_by_id(user_id, session)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        new_access_token = token_service.create_access_token(user)
        return AuthResponse(access_token=new_access_token)


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
