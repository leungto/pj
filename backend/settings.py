"""
Application settings
"""
import os


class Settings:
    # JWT 设置
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # 数据库设置
    DATABASE_URL = "sqlite:///./app.db"


# 创建设置实例
settings = Settings()