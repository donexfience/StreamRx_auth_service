from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from configurations.config.config import get_settings
from infrastructure.repositories.user_repository import UserRepositoryImpl

settings = get_settings()


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, get_db_session):
        super().__init__(app)
        self.get_db_session = get_db_session

    async def dispatch(self, request: Request, call_next):
        session = None
        try:
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split("Bearer ")[1]
                session = await self.get_db_session().__anext__()
                try:
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                    user_id = payload.get("sub")
                    user_repo = UserRepositoryImpl(session)
                    user = await user_repo.get_by_id(user_id, session)
                    if not user:
                        raise HTTPException(status_code=401, detail="Invalid user.")
                    request.state.current_user = user
                except JWTError:
                    raise HTTPException(status_code=401, detail="Invalid token.")

            response = await call_next(request)
            return response
        finally:
            if session:
                await session.close()
