from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.jwt_token_service import JWTTokenService
from application.services.user_service import UserService
from infrastructure.database.connection import get_db_session
from infrastructure.repositories.user_repository import UserRepositoryImpl
from infrastructure.services.password_service_impl import PasswordServiceImpl

router = APIRouter()


@router.post('/login')
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db_session),
        token_service: JWTTokenService = Depends()
):
    user_repo = UserRepositoryImpl(session)
    password_service = PasswordServiceImpl()
    user_service = UserService(user_repo, password_service)

    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = token_service.create_access_token(data={"sub": user.username})
    refresh_token = token_service.create_refresh_token(user)
    token_service.create_refresh_token(user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

