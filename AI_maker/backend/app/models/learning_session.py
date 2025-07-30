from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

Base = declarative_base()

class LearningSession(Base):
    __tablename__ = "learning_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_type = Column(String(50))  # code_review, practice, project_guidance
    language = Column(String(50))  # python, javascript, java, etc.
    topic = Column(String(100))
    code_content = Column(Text)
    ai_feedback = Column(Text)
    score = Column(Float, default=0.0)
    duration_minutes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联关系
    user = relationship("User", back_populates="sessions")

class CodeAnalysis(Base):
    __tablename__ = "code_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"))
    analysis_type = Column(String(50))  # syntax, logic, style, performance
    issue_description = Column(Text)
    suggestion = Column(Text)
    severity = Column(String(20))  # low, medium, high
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LearningSessionCreate(BaseModel):
    session_type: str
    language: str
    topic: str
    code_content: Optional[str] = None

class LearningSessionResponse(BaseModel):
    id: int
    session_type: str
    language: str
    topic: str
    code_content: Optional[str]
    ai_feedback: Optional[str]
    score: float
    duration_minutes: int
    created_at: datetime
    
    class Config:
        from_attributes = True 