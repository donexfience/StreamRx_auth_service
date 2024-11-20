from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass()
class User:
    id: Optional[int]
    email: str
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow();
