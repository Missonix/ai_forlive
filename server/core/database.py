from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from pathlib import Path
from dotenv import load_dotenv

"""
异步数据库配置
"""

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载环境变量
load_dotenv(os.path.join(BASE_DIR, "robyn.env"))

# MySQL配置
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '!Jgpy88888888')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'ai_data')

# 创建异步数据库引擎
engine = create_async_engine(
    f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}",
    echo=True,  # 设置为 True 可以看到 SQL 语句
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 最大溢出连接数
    pool_timeout=30,  # 连接池超时时间
    pool_recycle=1800,  # 连接回收时间
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 创建异步基类
class Base(DeclarativeBase):
    pass

# 获取异步数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()