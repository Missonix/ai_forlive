from robyn import Request, Response
from core.response import ApiResponse
from apps.search_video.core import video_search_check
from core.middleware import error_handler, request_logger, auth_required, admin_required, rate_limit, auth_userinfo
from core.logger import setup_logger
import json
from apps.users.crud import get_user, update_user
from core.database import AsyncSessionLocal
from apps.search_video import crud as video_search_crud
from apps.business import crud as business_crud

# 设置日志记录器
logger = setup_logger('video_search_views')


@error_handler
@request_logger
@rate_limit(max_requests=5, time_window=60)  # 每分钟最多5次请求
async def search_video(request: Request) -> Response:
    """对标视频搜索与推荐核心功能"""
    request_data = request.json()
    product_name = request_data.get("product_name")
    category = request_data.get("category")
    country = request_data.get("country")

    # 判断输入字符长度
    if len(product_name) > 60:
        return Response(
            status_code=400,
            headers={"Content-Type": "application/json"},
            description=json.dumps({"code": 400, "message": "输入的商品名称长度不要超过60哦"})
        )
    import os
    category_list = os.getenv("category")
    country_list = os.getenv("country")
    if category not in category_list:
        return Response(
            status_code=400,
            headers={"Content-Type": "application/json"},
            description=json.dumps({"code": 400, "message": "输入的商品类目不支持哦"})
        )
    
    if country not in country_list:
        return Response(
            status_code=400,
            headers={"Content-Type": "application/json"},
            description=json.dumps({"code": 400, "message": "输入的国家不支持哦"})
        )
    

    phone = request_data.get("phone")
    ai_product_id = request_data.get("ai_product_id")
    
    try:
        async with AsyncSessionLocal() as db:
            filters = {
                "phone": phone,
                "ai_product_id": ai_product_id,
                "is_deleted": False
            }
            
            entitlements, total_count = await business_crud.get_user_entitlements_by_filters(
                db, 
                filters=filters,
                order_by={"created_at": "desc"},
                page=1,
                page_size=1
            )
            if not entitlements:
                return ApiResponse.success(
                    message="暂无权益",
                    status_code=403
                )
    except Exception as e:
        logger.error(f"查询用户权益服务异常: {str(e)}")
        return ApiResponse.error(
            message="查询用户权益失败",
            status_code=500
        )

    # 获取最新的权益记录
    entitlement = entitlements[0]
    entitlement_id = entitlement.entitlement_id
    daily_remaining = entitlement.daily_remaining 
    
    if daily_remaining == 0:
        return Response(
            status_code=403,
            headers={"Content-Type": "application/json"},
            description=json.dumps({"code": 403, "message": "使用额度不足"})
        )

    from apps.search_video.core import shooting_suggestions
    result = await shooting_suggestions(product_name, category, country)  # 正确等待异步函数的结果
    if result == False:
        response_data = {
            "code": 500,
            "message": "fail",
            "data": {
                "result": "检测失败"
            }
        }
        return Response(
            status_code=500,
            headers={"Content-Type": "application/json"},
            description=json.dumps(response_data)
        )
    
    # 更新用户权益使用次数
    daily_remaining -= 1
    await business_crud.update_user_entitlement(db, entitlement_id, {"daily_remaining": daily_remaining})

    # 保存检测记录
    try:
        video_search_data = {
            "phone": phone,
            "product_name": product_name,
            "category": category,
            "country": country,
            "scenes": result.get("scenes", ""),
            "style": result.get("style", ""),
            "lens_usage": result.get("lens_usage", ""),
            "actor_selection": result.get("actor_selection", ""),
            "prop_matching": result.get("prop_matching", ""),
            "is_deleted": False
        }
        await video_search_crud.create_video_search_history(db, video_search_data)
    except Exception as e:
        logger.error(f"保存对标视频搜索与推荐记录失败: {str(e)}")
        # 继续执行，不影响返回结果

    # 构建标准响应格式
    response_data = {
        "code": 200,
        "message": "success",
        "data": {
            "result": result,
            "daily_remaining": daily_remaining
        }
    }
    
    return Response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        description=json.dumps(response_data)
    )

@error_handler
@request_logger
@rate_limit(max_requests=5, time_window=60)  # 每分钟最多5次请求
async def get_all_video_search_histories(request: Request) -> Response:
    """获取对标视频搜索与推荐记录"""
    from apps.search_video.services import get_video_search_histories_service
    return await get_video_search_histories_service(request)

@error_handler
@request_logger
# @auth_required
# @admin_required
async def get_search_history(request: Request) -> Response:
    """
    获取单个对标视频搜索与推荐记录
    """
    from apps.search_video.services import get_video_search_history_service
    return await get_video_search_history_service(request)

@error_handler
@request_logger
# @auth_required
# @admin_required
async def get_search_history_by_phone(request: Request) -> Response:
    """
    根据手机号搜索对标视频搜索与推荐记录
    """
    from apps.search_video.services import get_video_search_history_by_phone_service
    return await get_video_search_history_by_phone_service(request)








