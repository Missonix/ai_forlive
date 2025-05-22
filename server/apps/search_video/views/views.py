from robyn import Request, Response
from core.response import ApiResponse
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
    try:
        request_data = request.json()
        product_name = request_data.get("product_name")
        category = request_data.get("category")
        country = request_data.get("country")
        phone = request_data.get("phone")
        ai_product_id = request_data.get("ai_product_id")

        # 判断必要参数是否存在
        if not all([product_name, category, country, phone, ai_product_id]):
            return ApiResponse.validation_error("缺少必要参数")

        # 判断输入字符长度
        if len(product_name) > 60:
            return ApiResponse.validation_error("输入的商品名称长度不要超过60哦")

        # 查询category是否在三级类目中
        from apps.search_video.services import get_category_level3_service
        category_list = await get_category_level3_service(request)
        if isinstance(category_list, Response):
            category_list = json.loads(category_list.description).get("data", [])
        
        # 获取类目ID和名称的映射
        category_map = {item.get("label"): item.get("value") for item in category_list}
        if category not in category_map:
            return ApiResponse.validation_error("输入的商品类目不支持哦")
            
        # 获取类目ID
        category_id = category_map[category]
        # 获取类目label
        
        print("##################################################")
        print(f'category_id:{category_id}')
        print("##################################################")

        # 国家名称到代码的映射
        country_dict = {
            "美国": "US",
            "印度尼西亚": "ID",
            "马来西亚": "MY",
            "泰国": "TH",
            "越南": "VN",
            "菲律宾": "PH",
            "英国": "GB",
            "新加坡": "SG",
            "墨西哥": "MX"
        }

        # 查询country是否在国家字典中
        if country not in country_dict:
            return ApiResponse.validation_error("输入的国家不支持哦")
            
        # 获取国家代码
        country_code = country_dict[country]
        print("##################################################")
        print(f'country_code:{country_code}')
        print("##################################################")


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
                return ApiResponse.error(
                    message="暂无权益",
                    status_code=403
                )

            # 获取最新的权益记录
            entitlement = entitlements[0]
            entitlement_id = entitlement.entitlement_id
            daily_remaining = entitlement.daily_remaining
            
            if daily_remaining == 0:
                return ApiResponse.error(
                    message="使用额度不足",
                    status_code=403
                )

            # 获取拍摄建议
            from apps.search_video.core import shooting_suggestions
            result = await shooting_suggestions(product_name, category, country)
            if not result:
                return ApiResponse.error(
                    message="获取拍摄建议失败",
                    status_code=500
                )

            # 更新用户权益使用次数
            daily_remaining -= 1
            await business_crud.update_user_entitlement(db, entitlement_id, {"daily_remaining": daily_remaining})

            # 根据category和country查询kalodata数据
            try:
                # 构造查询条件
                kalodata_filters = {
                    "country": country_code,  # 使用转换后的国家代码
                    "category3": category,  # 使用转换后的类目ID
                    "is_deleted": False
                }
                
                print("##################################################")
                print(f'country_code:{country_code}, category:{category}')
                print("##################################################")
                # 查询kalodata数据
                kalodata_items, total_count = await video_search_crud.get_kalodata_data_by_filters(
                    db,
                    filters=kalodata_filters,
                    order_by={"created_at": "desc"},
                    page=1,
                    page_size=5
                )
                print("##################################################")
                print(f'kalodata_items:{kalodata_items}')
                print("##################################################")
                
                # 转换kalodata数据为字典列表，并处理datetime字段
                kalodata_items_list = []
                if kalodata_items:
                    for item in kalodata_items:
                        try:
                            item_dict = item.to_dict()
                            kalodata_items_list.append(item_dict)
                        except Exception as e:
                            logger.error(f"转换kalodata数据项为字典失败: {str(e)}")
                            # 如果转换失败，尝试手动构建字典
                            try:
                                item_dict = {
                                    "id": item.id,
                                    "country": item.country,
                                    "has_ad": item.has_ad,
                                    "video_name": item.video_name,
                                    "gpm": item.gpm,
                                    "cpm": item.cpm,
                                    "ad_view_ratio": item.ad_view_ratio,
                                    "duration": item.duration,
                                    "revenue": item.revenue,
                                    "sales": item.sales,
                                    "roas": item.roas,
                                    "ad2Cost": item.ad2Cost,
                                    "views": item.views,
                                    "product_title": item.product_title,
                                    "category1": item.category1,
                                    "category2": item.category2,
                                    "category3": item.category3,
                                    "product_price": item.product_price,
                                    "video_url": item.video_url,
                                    "tiktok_url": item.tiktok_url,
                                    "product_url": item.product_url,
                                    "product_image": item.product_image,
                                    "username": item.username,
                                    "follower_count": item.follower_count,
                                    "hashtags": item.hashtags,
                                    # 安全处理日期字段
                                    "start_date": item.start_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(item.start_date, 'strftime') else item.start_date,
                                    "end_date": item.end_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(item.end_date, 'strftime') else item.end_date,
                                    "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(item.created_at, 'strftime') else item.created_at
                                }
                                kalodata_items_list.append(item_dict)
                            except Exception as inner_e:
                                logger.error(f"手动构建kalodata数据项字典失败: {str(inner_e)}")

                # 保存检测记录
                try:
                    from datetime import datetime
                    
                    # 检查并处理items字段长度
                    kalodata_items_json = json.dumps(kalodata_items_list)
                    # 如果json字符串长度超过10000（数据库字段定义的长度），则进行截断处理
                    if len(kalodata_items_json) > 10000:
                        logger.warning(f"kalodata_items_json长度超过限制: {len(kalodata_items_json)}，将进行截断")
                        # 截断为空列表或者少量数据
                        kalodata_items_json = json.dumps([])
                    
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
                        "items": kalodata_items_json,  # 使用处理后的JSON字符串
                        "created_at": datetime.now(),
                        "is_deleted": False
                    }
                    
                    # 确保所有文本字段不超过其列定义的长度限制
                    field_limits = {
                        "phone": 20, 
                        "product_name": 60,
                        "category": 60,
                        "country": 20,
                        "scenes": 255,
                        "style": 255,
                        "lens_usage": 255,
                        "actor_selection": 255,
                        "prop_matching": 255
                    }
                    
                    for field, limit in field_limits.items():
                        if field in video_search_data and isinstance(video_search_data[field], str) and len(video_search_data[field]) > limit:
                            logger.warning(f"字段 {field} 长度超过限制: {len(video_search_data[field])}，将进行截断")
                            video_search_data[field] = video_search_data[field][:limit]
                    
                    await video_search_crud.create_video_search_history(db, video_search_data)
                    
                    # 转换datetime为字符串用于返回
                    response_data = video_search_data.copy()
                    response_data["created_at"] = response_data["created_at"].strftime("%Y-%m-%d %H:%M:%S")
                    
                    return ApiResponse.success(
                        data={
                            "result": response_data,
                            "daily_remaining": daily_remaining
                        },
                        message="获取视频搜索结果成功"
                    )
                except Exception as e:
                    logger.error(f"保存对标视频搜索与推荐记录失败: {str(e)}")
                    return ApiResponse.error(
                        message="保存记录失败",
                        status_code=500
                    )
            except Exception as e:
                logger.error(f"查询kalodata数据失败: {str(e)}")
                return ApiResponse.error(
                    message="查询kalodata数据失败",
                    status_code=500
                )

    except Exception as e:
        logger.error(f"视频搜索服务异常: {str(e)}")
        return ApiResponse.error(
            message="服务器内部错误",
            status_code=500
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

@error_handler
@request_logger
async def get_category_level1(request: Request) -> Response:
    """
    获取所有一级类目
    """
    from apps.search_video.services import get_category_level1_service
    return await get_category_level1_service(request)

@error_handler
@request_logger
async def get_category_level2_by_level1(request: Request) -> Response:
    """
    查询指定一级类目下的所有二级类目
    """
    from apps.search_video.services import get_category_level2_by_level1_service
    return await get_category_level2_by_level1_service(request)

@error_handler
@request_logger
async def get_category_level3_by_level2(request: Request) -> Response:
    """
    查询指定二级类目下的所有三级类目
    """
    from apps.search_video.services import get_category_level3_by_level2_service
    return await get_category_level3_by_level2_service(request)

@error_handler
@request_logger
async def get_category_level2(request: Request) -> Response:
    """
    获取所有二级类目
    """
    from apps.search_video.services import get_category_level2_service
    return await get_category_level2_service(request)

@error_handler
@request_logger
async def get_category_level3(request: Request) -> Response:
    """
    获取所有三级类目
    """
    from apps.search_video.services import get_category_level3_service
    return await get_category_level3_service(request)

@error_handler
@request_logger
async def fetch_and_store_kalodata(request: Request) -> Response:
    """
    获取并存储kalodata数据
    """
    from apps.search_video.services import fetch_and_store_kalodata_service
    return await fetch_and_store_kalodata_service(request)

@error_handler
@request_logger
async def get_kalodata_data(request: Request) -> Response:
    """
    获取单个kalodata数据
    """
    from apps.search_video.services import get_kalodata_data_service
    return await get_kalodata_data_service(request)

@error_handler
@request_logger
async def get_kalodata_datas(request: Request) -> Response:
    """
    获取所有kalodata数据
    """
    from apps.search_video.services import get_all_kalodatas_service
    return await get_all_kalodatas_service(request)

@error_handler
@request_logger
async def get_kalodata_data_by_filters(request: Request) -> Response:
    """
    根据过滤条件获取kalodata数据
    """
    from apps.search_video.services import get_kalodata_data_by_filters_service
    return await get_kalodata_data_by_filters_service(request)

@error_handler
@request_logger
async def update_kalodata_data(request: Request) -> Response:
    """
    更新kalodata数据
    """
    from apps.search_video.services import update_kalodata_data_service
    return await update_kalodata_data_service(request)

@error_handler
@request_logger
async def delete_kalodata_data(request: Request) -> Response:
    """
    删除kalodata数据
    """
    from apps.search_video.services import delete_kalodata_data_service
    return await delete_kalodata_data_service(request)

@error_handler
@request_logger
async def fetch_and_store_kalodata_by_categories(request: Request) -> Response:
    """
    根据所有三级类目批量获取并存储kalodata数据
    """
    from apps.search_video.services import fetch_and_store_kalodata_by_categories_service
    return await fetch_and_store_kalodata_by_categories_service(request)


"""
根据类目和国家获取kalodata数据
"""
@error_handler
@request_logger
async def get_kalodata_data_by_category_country(request: Request) -> Response:
    """
    根据类目和国家获取kalodata数据
    """
    from apps.search_video.services import get_kalodata_data_by_category_country_service
    return await get_kalodata_data_by_category_country_service(request)

@error_handler
@request_logger
async def get_kalodata_data_statistics(request: Request) -> Response:
    """
    获取kalodata数据统计信息 - 返回指定country和category的记录总数和最新end_date
    """
    from apps.search_video.services import get_kalodata_data_statistics_service
    return await get_kalodata_data_statistics_service(request)

@error_handler
@request_logger
async def fetch_and_store_kalodata_by_category1(request: Request) -> Response:
    """
    根据一级类目批量获取并存储kalodata数据
    """
    from apps.search_video.services import fetch_and_store_kalodata_by_category1_service
    return await fetch_and_store_kalodata_by_category1_service(request)

@error_handler
@request_logger
async def fetch_and_store_kalodata_by_category2(request: Request) -> Response:
    """
    根据二级类目批量获取并存储kalodata数据
    """
    from apps.search_video.services import fetch_and_store_kalodata_by_category2_service
    return await fetch_and_store_kalodata_by_category2_service(request)



