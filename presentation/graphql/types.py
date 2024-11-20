import strawberry
from datetime import datetime


@strawberry.type
class UserType:
    id: int
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


@strawberry.type
class AuthResponse:
    access_token: str
    token_type: str = 'bearer'


@strawberry.input
class UserRegistrationInput:
    email: str
    password: str


@strawberry.input
class UserLoginInput:
    email: str
    password: str
