from sqlalchemy import column, Integer, String, Boolean, DateTime, Column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base


class UserModel(Base):
    __tablename__ = 'users'

    id = column(Integer, primary_key=True, index=True)
    email = column(String,unique=True,index=True)
    hashed_password = column(String)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime,default=datetime.utcnow())
    updated_at = Column(DateTime,default=datetime.utcnow())

