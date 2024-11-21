import uvicorn
from fastapi import FastAPI, Depends, Request
import logging

from starlette.exceptions import HTTPException

from domain.entities.user import User
from presentation.api import auth
from presentation.graphql.queries import get_current_user
from presentation.graphql.schema import graphql_app
from infrastructure.database.connection import get_db_session
from presentation.middlewares.auth_middleware import AuthMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    session = None
    try:
        session = await get_db_session().__anext__()
        request.state.db = session
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.error(f"Error in request: {exc}")
        raise
    finally:
        if session:
            await session.close()


app.add_middleware(AuthMiddleware, get_db_session=get_db_session)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(graphql_app, prefix="/graphql")


@app.get("/test")
async def test_route():
    return {"message": "The API is working!"}

@app.get("/secured-test")
async def secured_test_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome {current_user.email}, you have access."}


if __name__ == "__main__":
    logger.info("Starting server on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
