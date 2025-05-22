from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, VARCHAR, Float, ForeignKey
from core.database import Base
import logging
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)


class Video_search_history(Base):
    """
    对标视频搜索与推荐模型，用于定义对标视频搜索与推荐表
    """
    __tablename__ = 'video_search_history'
    
    id = Column(Integer, primary_key=True, index=True) # 主键
    phone = Column(VARCHAR(20), nullable=False) # 用户手机号
    product_name = Column(VARCHAR(60), nullable=False) # 商品名称
    category = Column(VARCHAR(60), nullable=False) # 商品类目
    country = Column(VARCHAR(20), nullable=False) # 销售国家
    scenes = Column(VARCHAR(255), nullable=False) # 场景
    style = Column(VARCHAR(255), nullable=False) # 风格
    lens_usage = Column(VARCHAR(255), nullable=False) # 镜头使用
    actor_selection = Column(VARCHAR(255), nullable=False) # 演员选择
    prop_matching = Column(VARCHAR(255), nullable=False) # 道具匹配

    items = Column(VARCHAR(10000), nullable=False) # 商品列表

    created_at = Column(DateTime, default=datetime.utcnow) # 创建时间
    is_deleted = Column(Boolean, default=False) # 是否删除(逻辑删除)
    
    def __repr__(self):
        return (f"Video_search_history(id={self.id}, "
                f"phone={self.phone}, "
                f"product_name={self.product_name}, "
                f"category={self.category}, "
                f"country={self.country}, "
                f"scenes={self.scenes}, "
                f"style={self.style}, "
                f"lens_usage={self.lens_usage}, "
                f"actor_selection={self.actor_selection}, "
                f"prop_matching={self.prop_matching}, "

                f"items={self.items}, "

                f"created_at={self.created_at}, "
                f"is_deleted={self.is_deleted}")
    
    def to_dict(self):
        """转换为字典"""
        try:
            return {
                "id": self.id,
                "phone": self.phone,
                "product_name": self.product_name,
                "category": self.category,
                "country": self.country,
                "scenes": self.scenes,
                "style": self.style,
                "lens_usage": self.lens_usage,
                "actor_selection": self.actor_selection,
                "prop_matching": self.prop_matching,

                "items": self.items,

                "created_at": self.created_at.isoformat() if self.created_at else None
            }
        except Exception as e:
            logger.error(f"Error converting video_search_history to dict: {str(e)}")
            return {}
        

class Kalodata_data(Base):
    """
    从kalodata获取的爆款视频数据模型，用于定义爆款视频数据表
    """
    __tablename__ = 'kalodata_data'
    
    id = Column(Integer, primary_key=True, index=True) # 主键
    country = Column(VARCHAR(20), nullable=False) # 国家
    has_ad = Column(Boolean, default=False) # 是否投放广告
    video_name = Column(VARCHAR(255), nullable=False) # 视频名称
    gpm = Column(VARCHAR(255), nullable=False) # 每千次播放收入 
    cpm = Column(VARCHAR(255), nullable=False) # 广告单次获客成本
    ad_view_ratio = Column(VARCHAR(255), nullable=False) # 广告观看比例
    duration = Column(VARCHAR(255), nullable=False) # 视频时长
    revenue = Column(VARCHAR(255), nullable=False) # 视频收益
    sales = Column(VARCHAR(255), nullable=False) # 视频销量
    roas = Column(VARCHAR(255), nullable=False) # 广告投资回报率
    ad2Cost = Column(VARCHAR(255), nullable=False) # 视频广告成本
    views = Column(VARCHAR(255), nullable=False) # 视频播放量
    product_title = Column(VARCHAR(255), nullable=False) # 商品标题
    category1 = Column(VARCHAR(40), nullable=False) # 商品一级类目
    category2 = Column(VARCHAR(40), nullable=False) # 商品二级类目
    category3 = Column(VARCHAR(40), nullable=False) # 商品三级类目
    product_price = Column(VARCHAR(255), nullable=False) # 商品价格
    video_url = Column(VARCHAR(255), nullable=False) # 视频链接
    tiktok_url = Column(VARCHAR(255), nullable=False) # tiktok链接
    product_url = Column(VARCHAR(255), nullable=False) # 商品链接
    product_image = Column(VARCHAR(255), nullable=False) # 商品图片
    username = Column(VARCHAR(255), nullable=False) # 用户名
    follower_count = Column(VARCHAR(255), nullable=False) # 粉丝数
    hashtags = Column(VARCHAR(255), nullable=False) # 标签
    start_date = Column(DateTime, nullable=False) # 开始日期
    end_date = Column(DateTime, nullable=False) # 结束日期
    created_at = Column(DateTime, default=func.now()) # 创建时间
    is_deleted = Column(Boolean, default=False) # 是否删除(逻辑删除)
    
    
    def __repr__(self):
        return (f"kalodata_data(id={self.id}, "
                f"country={self.country}, "
                f"has_ad={self.has_ad}, "
                f"video_name={self.video_name}, "
                f"gpm={self.gpm}, "
                f"cpm={self.cpm}, "
                f"ad_view_ratio={self.ad_view_ratio}, "
                f"duration={self.duration}, "
                f"revenue={self.revenue}, "
                f"sales={self.sales}, "
                f"roas={self.roas}, "
                f"ad2Cost={self.ad2Cost}, "
                f"views={self.views}, "
                f"product_title={self.product_title}, "
                f"category1={self.category1}, "
                f"category2={self.category2}, "
                f"category3={self.category3}, "
                f"product_price={self.product_price}, "
                f"video_url={self.video_url}, "
                f"tiktok_url={self.tiktok_url}, "
                f"product_url={self.product_url}, "
                f"product_image={self.product_image}, "
                f"username={self.username}, "
                f"follower_count={self.follower_count}, "
                f"hashtags={self.hashtags}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"created_at={self.created_at}, "
                f"is_deleted={self.is_deleted}")
    
    def to_dict(self):
        """转换为字典"""
        try:
            date_fields = {
                "start_date": self.start_date,
                "end_date": self.end_date,
                "created_at": self.created_at
            }
            
            # 处理日期字段
            formatted_dates = {}
            for field_name, date_value in date_fields.items():
                try:
                    if date_value is not None:
                        if hasattr(date_value, 'strftime'):
                            formatted_dates[field_name] = date_value.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            formatted_dates[field_name] = str(date_value)
                    else:
                        formatted_dates[field_name] = None
                except Exception as e:
                    logger.error(f"格式化日期字段 {field_name} 失败: {str(e)}")
                    formatted_dates[field_name] = str(date_value) if date_value is not None else None
            
            return {
                "id": self.id,
                "country": self.country,
                "has_ad": self.has_ad,
                "video_name": self.video_name,
                "gpm": self.gpm,
                "cpm": self.cpm,
                "ad_view_ratio": self.ad_view_ratio,
                "duration": self.duration,
                "revenue": self.revenue,
                "sales": self.sales,
                "roas": self.roas,
                "ad2Cost": self.ad2Cost,
                "views": self.views,
                "product_title": self.product_title,
                "category1": self.category1,
                "category2": self.category2,
                "category3": self.category3,
                "product_price": self.product_price,
                "video_url": self.video_url,
                "tiktok_url": self.tiktok_url,
                "product_url": self.product_url,
                "product_image": self.product_image,
                "username": self.username,
                "follower_count": self.follower_count,
                "hashtags": self.hashtags,
                "start_date": formatted_dates["start_date"],
                "end_date": formatted_dates["end_date"],
                "created_at": formatted_dates["created_at"]
            }
        except Exception as e:
            logger.error(f"Error converting kalodata_data to dict: {str(e)}")
            return {}
            
    


class CategoryLevel1(Base):
    """一级类目模型"""
    __tablename__ = 'category_level1'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(100), nullable=False)
    value = Column(String(50), unique=True, nullable=False)
    
    # 关联关系
    children = relationship("CategoryLevel2", back_populates="parent")
    
    def __repr__(self):
        return f"<CategoryLevel1(label='{self.label}', value='{self.value}')>"
        
    def to_dict(self):
        """转换为字典"""
        try:
            return {
                "id": self.id,
                "label": self.label,
                "value": self.value
            }
        except Exception as e:
            logger.error(f"Error converting CategoryLevel1 to dict: {str(e)}")
            return {}

class CategoryLevel2(Base):
    """二级类目模型"""
    __tablename__ = 'category_level2'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(100), nullable=False)
    value = Column(String(50), unique=True, nullable=False)
    parent_value = Column(String(50), ForeignKey('category_level1.value'), nullable=False)
    
    # 关联关系
    parent = relationship("CategoryLevel1", back_populates="children")
    children = relationship("CategoryLevel3", back_populates="parent")
    
    def __repr__(self):
        return f"<CategoryLevel2(label='{self.label}', value='{self.value}')>"

    def to_dict(self):
        """转换为字典"""
        try:
            return {
                "id": self.id,
                "label": self.label,
                "value": self.value,
                "parent_value": self.parent_value
            }
        except Exception as e:
            logger.error(f"Error converting CategoryLevel2 to dict: {str(e)}")
            return {}

class CategoryLevel3(Base):
    """三级类目模型"""
    __tablename__ = 'category_level3'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(100), nullable=False)
    value = Column(String(50), unique=True, nullable=False)
    parent_value = Column(String(50), ForeignKey('category_level2.value'), nullable=False)
    
    # 关联关系
    parent = relationship("CategoryLevel2", back_populates="children")
    
    def __repr__(self):
        return f"<CategoryLevel3(label='{self.label}', value='{self.value}')>" 

    def to_dict(self):
        """转换为字典"""
        try:
            return {
                "id": self.id,
                "label": self.label,
                "value": self.value,
                "parent_value": self.parent_value
            }
        except Exception as e:
            logger.error(f"Error converting CategoryLevel2 to dict: {str(e)}")
            return {}
