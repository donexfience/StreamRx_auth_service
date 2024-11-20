from datetime import datetime, timedelta
from jose import JWTError, jwt
from application.interface.token_service import TokenService
from configurations.config.config import get_settings
from domain.entities.user import User
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

settings = get_settings()


class JWTTokenService(TokenService):
    def create_access_token(self, user: User) -> str:
        data = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def create_refresh_token(self, user: User) -> str:
        data = {
            "sub": str(user.id),
            "exp": datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        }
        return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
