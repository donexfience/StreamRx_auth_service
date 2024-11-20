from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    is_active: bool = True

