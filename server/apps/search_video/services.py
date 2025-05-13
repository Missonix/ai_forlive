from robyn import Request, Response
from core.response import ApiResponse
from core.middleware import error_handler, request_logger
from core.logger import setup_logger
from core.database import AsyncSessionLocal
from apps.search_video import crud as video_search_crud

# 设置日志记录器
logger = setup_logger('video_search_services')
    

async def get_video_search_histories_service(request: Request) -> Response:
    """
    获取对标视频搜索与推荐记录服务
    """
    try:
        # 获取分页参数
        try:
            page = int(request.query_params.get("page", "1"))
            page_size = int(request.query_params.get("page_size", "10"))
        except ValueError:
            page = 1
            page_size = 10
        
        # 验证分页参数
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10
            
        # 获取过滤条件
        filters = {}
        if "phone" in request.query_params:
            filters["phone"] = request.query_params.get("phone")
        if "product_name" in request.query_params:
            filters["product_name"] = request.query_params.get("product_name")
        if "category" in request.query_params:
            filters["category"] = request.query_params.get("category")
        if "country" in request.query_params:
            filters["country"] = request.query_params.get("country")
            
        # 获取排序条件
        order_by = {"created_at": "desc"}  # 默认按创建时间倒序排序
            
        async with AsyncSessionLocal() as db:
            try:
                video_search_histories, total_count = await video_search_crud.get_videos_search_histories_by_filters(
                    db, 
                    filters=filters,
                    order_by=order_by,
                    page=page,
                    page_size=page_size
                )
                
                # 计算总页数
                total_pages = (total_count + page_size - 1) // page_size
                
                return ApiResponse.success(
                    data={
                        "items": [histories.to_dict() for histories in video_search_histories],
                        "total": total_count,
                        "page": page,
                        "page_size": page_size,
                        "total_pages": total_pages
                    },
                    message="获取对标视频搜索与推荐记录成功"
                )
            except Exception as e:
                logger.error(f"查询对标视频搜索与推荐记录失败: {str(e)}")
                return ApiResponse.error(
                    message="获取对标视频搜索与推荐记录失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取对标视频搜索与推荐记录服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取对标视频搜索与推荐记录失败",
            status_code=500
        )

async def get_video_search_history_service(request: Request) -> Response:
    """
    获取单个对标视频搜索与推荐记录服务
    """
    try:
        # 获取记录ID
        id = request.path_params.get("id")
        if not id:
            return ApiResponse.validation_error("记录ID不能为空")
            
        try:
            id = int(id)
        except ValueError:
            return ApiResponse.validation_error("记录ID必须是整数")
            
        async with AsyncSessionLocal() as db:
            try:
                video_history = await video_search_crud.get_video_search_history(db, id)
                if not video_history:
                    return ApiResponse.not_found("对标视频搜索与推荐记录不存在")
                    
                return ApiResponse.success(
                    data=video_history.to_dict(),
                    message="获取对标视频搜索与推荐记录成功"
                )
            except Exception as e:
                logger.error(f"查询对标视频搜索与推荐记录失败: {str(e)}")
                return ApiResponse.error(
                    message="获取对标视频搜索与推荐记录失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取对标视频搜索与推荐记录服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取对标视频搜索与推荐记录失败",
            status_code=500
        )

async def get_video_search_history_by_phone_service(request: Request) -> Response:
    """
    根据手机号搜索对标视频搜索与推荐记录服务
    """
    try:
        # 获取手机号
        phone = request.path_params.get("phone")
        if not phone:
            return ApiResponse.validation_error("手机号不能为空")
            
        # 获取分页参数
        try:
            page = int(request.query_params.get("page", "1"))
            page_size = int(request.query_params.get("page_size", "10"))
        except ValueError:
            page = 1
            page_size = 10
        
        # 验证分页参数
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10
            
        # 构建过滤条件
        filters = {
            "phone": phone,
            "is_deleted": False
        }
        
        # 获取排序条件
        order_by = {"created_at": "desc"}  # 默认按创建时间倒序排序
            
        async with AsyncSessionLocal() as db:
            try:
                video_search_histories, total_count = await video_search_crud.get_videos_search_histories_by_filters(
                    db, 
                    filters=filters,
                    order_by=order_by,
                    page=page,
                    page_size=page_size
                )
                
                # 计算总页数
                total_pages = (total_count + page_size - 1) // page_size
                
                return ApiResponse.success(
                    data={
                        "items": [histories.to_dict() for histories in video_search_histories],
                        "total": total_count,
                        "page": page,
                        "page_size": page_size,
                        "total_pages": total_pages
                    },
                    message="获取对标视频搜索与推荐记录成功"
                )
            except Exception as e:
                logger.error(f"查询对标视频搜索与推荐记录失败: {str(e)}")
                return ApiResponse.error(
                    message="获取对标视频搜索与推荐记录失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取对标视频搜索与推荐记录服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取对标视频搜索与推荐记录失败",
            status_code=500
        ) 
    




