from enum import unique
from operator import index

from sqlalchemy import column, Integer, String, Boolean, DateTime, Column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)