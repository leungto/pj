"""
Database connection module.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import settings

# 创建SQLAlchemy引擎
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args= {
        "check_same_thread": False,  # 允许在多线程中使用同一连接
    }
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类，用于创建模型类
Base = declarative_base()

# 获取数据库会话
def get_db():
    """
    获取数据库会话的依赖函数，用于FastAPI路由依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 