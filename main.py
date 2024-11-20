from fastapi import FastAPI, Request
from fastapi.params import Depends
from starlette.middleware.base import BaseHTTPMiddleware

from domain.entities.user import User
from presentation.api import auth
from presentation.graphql.queries import get_current_user
from presentation.graphql.schema import graphql_app
from infrastructure.database.connection import get_db_session
from presentation.middlewares.auth_middleware import AuthMiddleware

app = FastAPI()
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.add_middleware(AuthMiddleware, get_db_session=get_db_session)

app.include_router(graphql_app, prefix="/graphql")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.session = await get_db_session().__anext__()
    response = await call_next(request)
    await request.state.session.close()
    return response


@app.get("/test")
async def test_route():
    return {"message": "The API is working!"}


@app.get("/secured-test")
async def secured_test_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome {current_user.email}, you have access."}
