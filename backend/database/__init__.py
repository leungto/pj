"""
Database module initialization.
"""
from .connection import Base, engine, get_db
from .models import *  # Import all models

# 创建所有表
def create_tables():
    """
    创建数据库中的所有表
    """
    Base.metadata.create_all(bind=engine)
