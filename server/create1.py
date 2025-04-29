# reset_db.py
import pymysql
from sqlalchemy import create_engine
from core.database import Base
from apps.users.models import User, Admin
from apps.business.models import Courses, Entitlement_rules, Orders, User_entitlements, Ai_products, Upload_error_orders, Batch_generate_entitlements_error
from apps.vio_word.models import Vio_word

def reset_database():
    """删除并重建数据库"""
    # 连接到MySQL服务器（不指定数据库）
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='!Jgpy88888888',
        port=3306
    )
    
    try:
        with connection.cursor() as cursor:
            # 删除数据库（如果存在）
            cursor.execute("DROP DATABASE IF EXISTS ai_data")
            # 新建数据库
            cursor.execute(
                "CREATE DATABASE ai_data "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.commit()
        print("✅ 数据库 ai_data 已重建")
    except Exception as e:
        connection.rollback()
        print(f"❌ 数据库操作失败：{str(e)}")
    finally:
        connection.close()

def create_tables():
    """根据模型创建表结构"""
    # 使用同步引擎
    engine = create_engine(
        "mysql+pymysql://root:!Jgpy88888888@localhost:3306/ai_data",
        echo=True
    )
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 所有表结构已创建")
    except Exception as e:
        print(f"❌ 创建表失败：{str(e)}")

if __name__ == "__main__":
    reset_database()
    create_tables()