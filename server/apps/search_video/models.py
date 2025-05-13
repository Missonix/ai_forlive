from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, VARCHAR
from core.database import Base
import logging

logger = logging.getLogger(__name__)


class Video_search_history(Base):
    """
    对标视频搜索与推荐模型，用于定义对标视频搜索与推荐表
    """
    __tablename__ = 'video_search_history'
    
    id = Column(Integer, primary_key=True, index=True) # 主键
    phone = Column(VARCHAR(20), nullable=False) # 用户手机号
    product_name = Column(VARCHAR(255), nullable=False) # 商品名称
    category = Column(VARCHAR(255), nullable=False) # 商品类目
    country = Column(VARCHAR(255), nullable=False) # 销售国家
    scenes = Column(VARCHAR(255), nullable=False) # 场景
    style = Column(VARCHAR(255), nullable=False) # 风格
    lens_usage = Column(VARCHAR(255), nullable=False) # 镜头使用
    actor_selection = Column(VARCHAR(255), nullable=False) # 演员选择
    prop_matching = Column(VARCHAR(255), nullable=False) # 道具匹配

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
    country = Column(VARCHAR(255), nullable=False) # 国家
    video_name = Column(VARCHAR(255), nullable=False) # 视频名称
    video_url = Column(VARCHAR(255), nullable=False) # 视频链接
    product_title = Column(VARCHAR(255), nullable=False) # 商品标题
    product_url = Column(VARCHAR(255), nullable=False) # 商品链接
    product_image = Column(VARCHAR(255), nullable=False) # 商品图片
    max_real_price = Column(Integer, nullable=False) # 商品最高价
    min_real_price = Column(Integer, nullable=False) # 商品最低价
    views = Column(Integer, nullable=False) # 视频播放量
    duration = Column(Integer, nullable=False) # 视频时长
    revenue = Column(Integer, nullable=False) # 视频收益
    sales = Column(Integer, nullable=False) # 视频销量
    ad_view_ratio = Column(Integer, nullable=False) # 视频广告曝光率
    gpm = Column(Integer, nullable=False) # 千次曝光价值
    ad2Cost = Column(Integer, nullable=False) # 视频广告成本
    ad_revenue_ratio = Column(Integer, nullable=False) # 视频广告收益比
    created_at = Column(DateTime, default=datetime.utcnow) # 创建时间
    is_deleted = Column(Boolean, default=False) # 是否删除(逻辑删除)
    
    def __repr__(self):
        return (f"kalodata_data(id={self.id}, "
                f"country={self.country}, "
                f"video_name={self.video_name}, "
                f"video_url={self.video_url}, "
                f"product_title={self.product_title}, "
                f"product_url={self.product_url}, "
                f"product_image={self.product_image}, "
                f"max_real_price={self.max_real_price}, "
                f"min_real_price={self.min_real_price}, "
                f"views={self.views}, "
                f"duration={self.duration}, "
                f"revenue={self.revenue}, "
                f"sales={self.sales}, "
                f"ad_view_ratio={self.ad_view_ratio}, "
                f"gpm={self.gpm}, "
                f"ad2Cost={self.ad2Cost}, "
                f"ad_revenue_ratio={self.ad_revenue_ratio}, "
                f"created_at={self.created_at}, "
                f"is_deleted={self.is_deleted}")
    
    def to_dict(self):
        """转换为字典"""
        try:
            return {
                "id": self.id,
                "country": self.country,
                "video_name": self.video_name,
                "video_url": self.video_url,
                "product_title": self.product_title,
                "product_url": self.product_url,
                "product_image": self.product_image,
                "max_real_price": self.max_real_price,
                "min_real_price": self.min_real_price,
                "views": self.views,
                "duration": self.duration,
                "revenue": self.revenue,
                "sales": self.sales,
                "ad_view_ratio": self.ad_view_ratio,
                "gpm": self.gpm,
                "ad2Cost": self.ad2Cost,
                "ad_revenue_ratio": self.ad_revenue_ratio,
                "created_at": self.created_at.isoformat() if self.created_at else None
            }
        except Exception as e:
            logger.error(f"Error converting kalodata_data to dict: {str(e)}")
            return {}
            
    


