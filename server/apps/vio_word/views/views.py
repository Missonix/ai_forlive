from robyn import Request, Response
from core.response import ApiResponse
from apps.vio_word.core import vio_word_check
from core.middleware import error_handler, request_logger, auth_required, admin_required, rate_limit, auth_userinfo
from core.logger import setup_logger
import json
from apps.users.crud import get_user, update_user
from core.database import AsyncSessionLocal
from apps.vio_word import crud as vio_word_crud
from apps.business import crud as business_crud

# 设置日志记录器
logger = setup_logger('vio_word_views')

@error_handler
@request_logger
@rate_limit(max_requests=5, time_window=60)  # 每分钟最多5次请求
async def vio_check(request: Request) -> Response:
    """传入话术，返回违规词检测结果"""
    request_data = request.json()
    input_text = request_data.get("input")
    # 判断输入字符长度
    if len(input_text) > 120:
        return Response(
            status_code=400,
            headers={"Content-Type": "application/json"},
            description=json.dumps({"code": 400, "message": "输入字符长度不要超过120哦"})
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

    result = await vio_word_check(input_text)  # 正确等待异步函数的结果
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
        # 处理 is_Violations 字段
        is_violation = result.get("is_Violations") == "是"
        
        vio_word_data = {
            "phone": phone,
            "input": input_text,
            "is_violation": is_violation,
            "words": result.get("words", ""),
            "reasons": result.get("reason", ""),  # 注意：API返回的是 reason，而不是 reasons
            "op": result.get("op", ""),
            "ideas": result.get("ideas", ""),
            "old_score": result.get("old_score", 0),
            "new_score": result.get("new_score", 0),
            "old_rating": result.get("old_rating", ""),
            "new_rating": result.get("new_rating", ""),
            "is_deleted": False
        }
        await vio_word_crud.create_vio_word(db, vio_word_data)
    except Exception as e:
        logger.error(f"保存违规词检测记录失败: {str(e)}")
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
# @auth_required
# @admin_required
async def get_vio_words(request: Request) -> Response:
    """
    获取所有违规词检测记录
    """
    from apps.vio_word.services import get_vio_words_service
    return await get_vio_words_service(request)

@error_handler
@request_logger
# @auth_required
# @admin_required
async def get_vio_word(request: Request) -> Response:
    """
    获取单个违规词检测记录
    """
    from apps.vio_word.services import get_vio_word_service
    return await get_vio_word_service(request)

@error_handler
@request_logger
# @auth_required
# @admin_required
async def get_vio_words_by_phone(request: Request) -> Response:
    """
    根据手机号搜索违规词检测记录
    """
    from apps.vio_word.services import get_vio_words_by_phone_service
    return await get_vio_words_by_phone_service(request)








