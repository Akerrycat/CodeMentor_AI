from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(100))
    skill_level = Column(String(20), default="beginner")  # beginner, intermediate, advanced
    programming_languages = Column(Text, default="[]")  # JSON字符串
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    skill_level: str = "beginner"
    programming_languages: list = []

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    skill_level: Optional[str] = None
    programming_languages: Optional[list] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    skill_level: str
    programming_languages: list
    created_at: datetime
    
    class Config:
        from_attributes = True 