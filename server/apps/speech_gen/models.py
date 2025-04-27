from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, VARCHAR
from core.database import Base
import logging

logger = logging.getLogger(__name__)

class Speech_gen(Base):
    """
    AI话术生成模型，用于定义AI话术生成表
    """
    __tablename__ = 'speech_gen'
    
    id = Column(Integer, primary_key=True, index=True) # 主键
    phone = Column(VARCHAR(20), nullable=False) # 用户手机号
    input = Column(VARCHAR(255), nullable=False) # 输入内容
    product_name = Column(VARCHAR(255), nullable=False) # 产品名称
    product_category = Column(VARCHAR(255), nullable=False) # 产品类目
    selling_points = Column(VARCHAR(255), nullable=False) # 核心卖点
    discount = Column(VARCHAR(255), nullable=False) # 价格策略
    crowd = Column(VARCHAR(255), nullable=False) # 目标人群
    output = Column(VARCHAR(1000), nullable=False) # 输出话术
    created_at = Column(DateTime, default=datetime.utcnow) # 创建时间
    is_deleted = Column(Boolean, default=False) # 是否删除(逻辑删除)
    
    def __repr__(self):
        return (f"Speech_gen(id={self.id}, "
                f"phone={self.phone}, "
                f"input={self.input}, "
                f"product_name={self.product_name}, "
                f"product_category={self.product_category}, "
                f"selling_points={self.selling_points}, "
                f"discount={self.discount}, "
                f"crowd={self.crowd}, "
                f"output={self.output}, "
                f"created_at={self.created_at}, "
                f"is_deleted={self.is_deleted}")
    
    def to_dict(self):
        """转换为字典"""
        try:
            return {
                "id": self.id,
                "phone": self.phone,
                "input": self.input,
                "product_name": self.product_name,
                "product_category": self.product_category,
                "selling_points": self.selling_points,
                "discount": self.discount,
                "crowd": self.crowd,
                "output": self.output,
                "created_at": self.created_at.isoformat() if self.created_at else None
            }
        except Exception as e:
            logger.error(f"Error converting speech_gen to dict: {str(e)}")
            return {}
        
