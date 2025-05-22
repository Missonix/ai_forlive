from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, desc, asc
from sqlalchemy.sql import func
from core.database import AsyncSessionLocal
from core.logger import setup_logger
from apps.search_video.models import Video_search_history, Kalodata_data, CategoryLevel1, CategoryLevel2, CategoryLevel3
from common.utils.dynamic_query import dynamic_query
import logging

# 设置日志记录器
logger = logging.getLogger(__name__)

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
    


async def create_kalodata_data(db: AsyncSession, data: dict):
    """
    创建kalodata数据记录
    """
    try:
        # 字段长度限制检查
        field_length_limits = {
            "country": 20,
            "video_name": 255,
            "gpm": 255,
            "cpm": 255,
            "ad_view_ratio": 255,
            "duration": 255,
            "revenue": 255,
            "sales": 255,
            "roas": 255,
            "ad2Cost": 255,
            "views": 255,
            "product_title": 255,
            "category1": 40,
            "category2": 40,
            "category3": 40,
            "product_price": 255,
            "video_url": 255,
            "tiktok_url": 255,
            "product_url": 255,
            "product_image": 255,
            "username": 255,
            "follower_count": 255,
            "hashtags": 255
        }
        
        # 截断超长字段
        for field, limit in field_length_limits.items():
            if field in data and isinstance(data[field], str) and len(data[field]) > limit:
                logger.warning(f"字段 {field} 超出长度限制 {limit}，进行截断处理")
                data[field] = data[field][:limit]
                
        # 确保日期字段格式正确
        date_fields = ["start_date", "end_date"]
        for field in date_fields:
            if field in data and data[field] is not None:
                if isinstance(data[field], str):
                    try:
                        from datetime import datetime
                        # 尝试解析日期字符串，这有助于确保格式一致
                        data[field] = datetime.strptime(data[field], "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try:
                            # 尝试不同的日期格式
                            data[field] = datetime.strptime(data[field], "%Y-%m-%d")
                        except ValueError as e:
                            logger.error(f"无法解析日期字段 {field}: {data[field]}, 错误: {str(e)}")
                            raise e
        
        # 创建记录
        kalodata_data = Kalodata_data(**data)
        db.add(kalodata_data)
        await db.commit()
        await db.refresh(kalodata_data)
        return kalodata_data
    except Exception as e:
        await db.rollback()
        logger.error(f"创建kalodata数据记录失败: {str(e)}")
        raise e

async def get_kalodata_data(db: AsyncSession, id: int):
    """获取单个kalodata数据"""
    return await db.get(Kalodata_data, id)

async def get_kalodata_datas(db: AsyncSession):
    """获取所有kalodata数据"""
    try:
        query = select(Kalodata_data).where(Kalodata_data.is_deleted == False)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        logger.error(f"获取爆款视频数据失败: {str(e)}")
        raise

async def get_kalodata_data_by_filters(db: AsyncSession, filters: dict, order_by: dict = None, page: int = 1, page_size: int = 10):
    """根据条件查询kalodata数据"""
    try:
        # 构建基础查询
        query = select(Kalodata_data)
        
        # 添加过滤条件
        for key, value in filters.items():
            if hasattr(Kalodata_data, key):
                if value is not None:  # 只添加非空值的过滤条件
                    query = query.where(getattr(Kalodata_data, key) == value)
                
        # 添加排序条件
        if order_by:
            for key, direction in order_by.items():
                if hasattr(Kalodata_data, key):
                    if direction.lower() == "desc":
                        query = query.order_by(desc(getattr(Kalodata_data, key)))
                    else:
                        query = query.order_by(asc(getattr(Kalodata_data, key)))
                        
        # 计算总数
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        # 添加分页
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        # 执行查询
        result = await db.execute(query)
        items = result.scalars().all()
        
        return items, total
    except Exception as e:
        logger.error(f"根据条件查询kalodata数据失败: {str(e)}")
        raise

async def update_kalodata_data(db: AsyncSession, id: int, update_data: dict):
    """更新kalodata数据"""
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
    """删除kalodata数据（软删除）"""
    try:
        kalodata_data = await db.get(Kalodata_data, id)
        if kalodata_data:
            kalodata_data.is_deleted = True
            await db.commit()
        return kalodata_data
    except Exception as e:
        await db.rollback()
        raise e
    

async def get_category_level1(db: AsyncSession):
    """获取一级类目"""
    query = select(CategoryLevel1)
    result = await db.execute(query)
    return result.scalars().all()

async def get_category_level2(db: AsyncSession):
    """获取二级类目"""
    query = select(CategoryLevel2)
    result = await db.execute(query)
    return result.scalars().all()

async def get_category_level3(db: AsyncSession):
    """获取三级类目"""
    query = select(CategoryLevel3)
    result = await db.execute(query)
    return result.scalars().all()


async def get_category_level1_by_filters(db: AsyncSession, filters: dict):
    """根据条件查询一级类目"""
    query = await dynamic_query(db, CategoryLevel1, filters)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_category_level2_by_filters(db: AsyncSession, filters: dict):
    """根据条件查询二级类目"""
    query = await dynamic_query(db, CategoryLevel2, filters)
    result = await db.execute(query)
    return result.scalars().all()

async def get_category_level3_by_filters(db: AsyncSession, filters: dict):
    """根据条件查询三级类目"""
    query = await dynamic_query(db, CategoryLevel3, filters)
    result = await db.execute(query)
    return result.scalars().all()

async def get_category_level2_by_value(db: AsyncSession, value: str):
    """
    根据value获取单个二级类目
    """
    try:
        query = select(CategoryLevel2).where(CategoryLevel2.value == value)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"根据value获取单个二级类目失败: {str(e)}")
        raise e

async def check_kalodata_exists(db: AsyncSession, data: dict) -> bool:
    """
    检查kalodata数据是否已存在
    
    参数:
        db: 数据库会话
        data: 要检查的数据，包含 country、video_name、product_title、start_date、end_date
    
    返回:
        bool: True 表示数据已存在，False 表示数据不存在
    """
    try:
        query = select(Kalodata_data).where(
            Kalodata_data.country == data["country"],
            Kalodata_data.video_name == data["video_name"],
            Kalodata_data.product_title == data["product_title"],
            Kalodata_data.start_date == data["start_date"],
            Kalodata_data.end_date == data["end_date"],
            Kalodata_data.is_deleted == False
        )
        result = await db.execute(query)
        existing_data = result.scalar_one_or_none()
        return existing_data is not None
    except Exception as e:
        logger.error(f"检查kalodata数据是否存在时发生错误: {str(e)}")
        raise






