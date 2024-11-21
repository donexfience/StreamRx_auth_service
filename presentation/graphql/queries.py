import  strawberry
from typing import Optional

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.jwt_token_service import JWTTokenService
from infrastructure.database.connection import get_db_session
from presentation.graphql.schema import UserType

async def get_current_user(
        info,
        session: AsyncSession = Depends(get_db_session),
        token_service: JWTTokenService = Depends()
):
    request = info.context["request"]
    authorization: str = request.headers.get("Authorization")
    if authorization is None:
        return None
    token = authorization.split(" ")[1]
    payload = token_service.decode_access_token(token)
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        return None
    user = await session.get(UserType, user_id)
    return user
