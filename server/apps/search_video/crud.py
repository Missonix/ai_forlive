from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import func
from core.database import AsyncSessionLocal
from core.logger import setup_logger
from apps.search_video.models import Video_search_history, Kalodata_data
from common.utils.dynamic_query import dynamic_query

# 设置日志记录器
logger = setup_logger('search_video_crud')

async def create_video_search_history(db: AsyncSession, video_search_history_data: dict):
    """创建对标视频搜索与推荐记录"""
    try:
        new_video_search_history = Video_search_history(**video_search_history_data)
        db.add(new_video_search_history)
        await db.commit()
        await db.refresh(new_video_search_history)
        return new_video_search_history
    except Exception as e:
        await db.rollback()
        raise e

async def get_video_search_history(db: AsyncSession, id: int):
    """获取单个对标视频搜索与推荐记录"""
    return await db.get(Video_search_history, id)

async def get_video_search_histories(db: AsyncSession):
    """获取所有对标视频搜索与推荐记录"""
    try:
        query = select(Video_search_history).where(Video_search_history.is_deleted == False)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        logger.error(f"获取对标视频搜索与推荐记录失败: {str(e)}")
        raise

async def get_video_search_history_by_filters(db: AsyncSession, filters: dict):
    """根据条件查询对标视频搜索与推荐记录"""
    query = await dynamic_query(db, Video_search_history, filters)
    result = await db.execute(query)
    history = result.scalar_one_or_none()
    return history

async def get_videos_search_histories_by_filters(db: AsyncSession, filters=None, order_by=None, page: int = 1, page_size: int = 10):
    """
    批量查询对标视频搜索与推荐记录，支持分页
    :param db: 数据库会话
    :param filters: 过滤条件
    :param order_by: 排序条件，如 {"created_at": "desc"}
    :param page: 页码，从1开始
    :param page_size: 每页数量
    :return: (用户权益列表, 总记录数)
    """
    try:
        # 构建基础查询
        query = await dynamic_query(db, Video_search_history, filters, order_by)
        
        # 计算总记录数
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.execute(count_query)
        total_count = total.scalar()
        
        # 添加分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # 执行查询
        result = await db.execute(query)
        video_search_histories = result.scalars().all()
        
        return video_search_histories, total_count
    except Exception as e:
        logger.error(f"查询对标视频搜索与推荐记录列表失败: {str(e)}")
        raise
        
        

async def update_video_search_history(db: AsyncSession, id: int, update_data: dict):
    """更新对标视频搜索与推荐记录"""
    try:
        video_search_history = await db.get(Video_search_history, id)
        if video_search_history:
            for key, value in update_data.items():
                setattr(video_search_history, key, value)
            await db.commit()
            await db.refresh(video_search_history)
        return video_search_history
    except Exception as e:
        await db.rollback()
        raise e

async def delete_video_search_history(db: AsyncSession, id: int):
    """删除对标视频搜索与推荐记录（软删除）"""
    try:
        video_search_history = await db.get(Video_search_history, id)
        if video_search_history:
            video_search_history.is_deleted = True
            await db.commit()
        return video_search_history
    except Exception as e:
        await db.rollback()
        raise e 
    


async def create_kalodata_data(db: AsyncSession, kalodata_data_data: dict):
    """创建爆款视频数据"""
    try:
        new_kalodata_data = Kalodata_data(**kalodata_data_data)
        db.add(new_kalodata_data)
        await db.commit()
        await db.refresh(new_kalodata_data)
        return new_kalodata_data
    except Exception as e:
        await db.rollback()
        raise e

async def get_kalodata_data(db: AsyncSession, id: int):
    """获取单个爆款视频数据"""
    return await db.get(Kalodata_data, id)

async def get_kalodata_datas(db: AsyncSession):
    """获取所有爆款视频数据"""
    try:
        query = select(Kalodata_data).where(Kalodata_data.is_deleted == False)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        logger.error(f"获取爆款视频数据失败: {str(e)}")
        raise

async def get_kalodata_data_by_filters(db: AsyncSession, filters: dict):
    """根据条件查询爆款视频数据"""
    query = await dynamic_query(db, Kalodata_data, filters)
    result = await db.execute(query)
    kalodata_data = result.scalar_one_or_none()
    return kalodata_data

async def update_kalodata_data(db: AsyncSession, id: int, update_data: dict):
    """更新爆款视频数据"""
    try:
        kalodata_data = await db.get(Kalodata_data, id)
        if kalodata_data:
            for key, value in update_data.items():
                setattr(kalodata_data, key, value)
            await db.commit()
            await db.refresh(kalodata_data)
        return kalodata_data
    except Exception as e:
        await db.rollback()
        raise e

async def delete_kalodata_data(db: AsyncSession, id: int):
    """删除爆款视频数据（软删除）"""
    try:
        kalodata_data = await db.get(Kalodata_data, id)
        if kalodata_data:
            kalodata_data.is_deleted = True
            await db.commit()
        return kalodata_data
    except Exception as e:
        await db.rollback()
        raise e
    
    
    
