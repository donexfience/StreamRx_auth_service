import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from strawberry.types import Info
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.jwt_token_service import JWTTokenService
# Import necessary use cases and modules
from application.use_cases.auth_use_cases import AuthUseCases
from infrastructure.database.connection import get_db_session
from infrastructure.repositories.user_repository import UserRepositoryImpl
from infrastructure.services.password_service_impl import PasswordServiceImpl

# Import the defined types
from presentation.graphql.types import UserRegistrationInput, UserType, UserLoginInput, AuthResponse


async def get_auth_use_cases(session: AsyncSession = Depends(get_db_session)):
    user_repository = UserRepositoryImpl(session)
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
    async def list_users(
            self,
            session: AsyncSession = Depends(get_db_session)
    ) -> List[UserType]:
        user_repository = UserRepositoryImpl(session)
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
    async def register(
            self,
            input: UserRegistrationInput,
            auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
    ) -> UserType:
        user = await auth_use_cases.register_user(
            email=input.email,
            password=input.password
        )
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

    @strawberry.mutation
    async def refresh_token(
            self,
            refresh_token: str,
            token_service: JWTTokenService = Depends()
    ) -> AuthResponse:
        payload = token_service.decode_token(refresh_token)
        user_id = payload.get("sub")
        session: AsyncSession = Depends(get_db_session)
        user_repository = UserRepositoryImpl(session)
        user = await user_repository.get_by_id(user_id, session)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        new_access_token = token_service.create_access_token(user)
        return AuthResponse(access_token=new_access_token)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)
