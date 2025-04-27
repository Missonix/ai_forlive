from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import AsyncSessionLocal
from core.logger import setup_logger
from apps.speech_gen.models import Speech_gen

# 设置日志记录器
logger = setup_logger('speech_gen_crud')

async def create_speech_gen(db: AsyncSession, speech_gen_data: dict):
    """创建话术生成记录"""
    try:
        new_speech_gen = Speech_gen(**speech_gen_data)
        db.add(new_speech_gen)
        await db.commit()
        await db.refresh(new_speech_gen)
        return new_speech_gen
    except Exception as e:
        await db.rollback()
        raise e

async def get_speech_gen(db: AsyncSession, id: int):
    """获取单个话术生成记录"""
    return await db.get(Speech_gen, id)

async def get_speech_gens_by_filters(db: AsyncSession, filters: dict = None, order_by: dict = None, page: int = 1, page_size: int = 10):
    """根据条件查询话术生成记录"""
    try:
        # 构建基础查询
        query = select(Speech_gen).where(Speech_gen.is_deleted == False)
        
        # 添加过滤条件
        if filters:
            if "phone" in filters:
                query = query.where(Speech_gen.phone == filters["phone"])
            if "product_name" in filters:
                query = query.where(Speech_gen.product_name == filters["product_name"])
            if "product_category" in filters:
                query = query.where(Speech_gen.product_category == filters["product_category"])
            if "selling_points" in filters:
                query = query.where(Speech_gen.selling_points == filters["selling_points"])
            if "crowd" in filters:
                query = query.where(Speech_gen.crowd == filters["crowd"])
            if "created_at" in filters:
                query = query.where(Speech_gen.created_at == filters["created_at"])
        
        # 添加排序条件
        if order_by:
            for key, value in order_by.items():
                if value.lower() == "desc":
                    query = query.order_by(getattr(Speech_gen, key).desc())
                else:
                    query = query.order_by(getattr(Speech_gen, key))
        
        # 执行查询
        result = await db.execute(query)
        speech_gens = result.scalars().all()
        
        # 计算总记录数
        total_count = len(speech_gens)
        
        # 手动分页
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_speech_gens = speech_gens[start_idx:end_idx]
        
        return paginated_speech_gens, total_count
    except Exception as e:
        logger.error(f"查询话术生成记录失败: {str(e)}")
        raise

async def update_speech_gen(db: AsyncSession, id: int, update_data: dict):
    """更新话术生成记录"""
    try:
        speech_gen = await db.get(Speech_gen, id)
        if speech_gen:
            for key, value in update_data.items():
                setattr(speech_gen, key, value)
            await db.commit()
            await db.refresh(speech_gen)
        return speech_gen
    except Exception as e:
        await db.rollback()
        raise e

async def delete_speech_gen(db: AsyncSession, id: int):
    """删除话术生成记录（软删除）"""
    try:
        speech_gen = await db.get(Speech_gen, id)
        if speech_gen:
            speech_gen.is_deleted = True 
            await db.commit()
        return speech_gen
    except Exception as e:
        await db.rollback()
        raise e 