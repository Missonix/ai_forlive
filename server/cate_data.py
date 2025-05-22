import json
from typing import List, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from apps.search_video.models import Base, CategoryLevel1, CategoryLevel2, CategoryLevel3
from core.database import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def get_database_url():
    """获取数据库连接URL"""
    return f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

def create_tables(engine):
    """创建所有表"""
    Base.metadata.create_all(engine)

def insert_categories(session, categories: List[Dict[str, Any]]):
    """插入品类数据到数据库"""
    try:
        for level1_data in categories:
            # 创建一级类目
            level1 = CategoryLevel1(
                label=level1_data['label'],
                value=level1_data['value']
            )
            session.add(level1)
            
            # 处理二级类目
            for level2_data in level1_data.get('children', []):
                level2 = CategoryLevel2(
                    label=level2_data['label'],
                    value=level2_data['value'],
                    parent_value=level1.value
                )
                session.add(level2)
                
                # 处理三级类目
                for level3_data in level2_data.get('children', []):
                    level3 = CategoryLevel3(
                        label=level3_data['label'],
                        value=level3_data['value'],
                        parent_value=level2.value
                    )
                    session.add(level3)
        
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"数据导入错误: {str(e)}")
        return False

def main():
    # 读取类目数据
    with open('cates.txt', 'r', encoding='utf-8') as f:
        categories = json.load(f)
    
    # 创建数据库引擎
    engine = create_engine(get_database_url(), echo=True)
    
    # 创建表
    create_tables(engine)
    
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 插入数据
        success = insert_categories(session, categories)
        
        if success:
            # 验证数据
            level1_count = session.query(CategoryLevel1).count()
            level2_count = session.query(CategoryLevel2).count()
            level3_count = session.query(CategoryLevel3).count()
            
            print("数据导入完成，验证结果：")
            print(f"一级类目数量: {level1_count}")
            print(f"二级类目数量: {level2_count}")
            print(f"三级类目数量: {level3_count}")
        else:
            print("数据导入失败")
            
    finally:
        session.close()

if __name__ == '__main__':
    main()
