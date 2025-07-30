from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost/codementor"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    
    # OpenAI配置
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 应用配置
    APP_NAME: str = "CodeMentor AI"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings() 