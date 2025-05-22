from robyn import Request, Response
from core.response import ApiResponse
from core.middleware import error_handler, request_logger
from core.logger import setup_logger
from core.database import AsyncSessionLocal
from apps.search_video import crud as video_search_crud
import asyncio
import random
from datetime import datetime, timedelta
import json

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
    

async def get_category_level1_service(request: Request) -> Response:
    """
    获取所有一级类目    
    """
    try:
        async with AsyncSessionLocal() as db:
            try:
                category_level1 = await video_search_crud.get_category_level1(db)
                return ApiResponse.success(
                    data=[category.to_dict() for category in category_level1],
                    message="获取所有一级类目成功"
                )
            except Exception as e:
                logger.error(f"获取所有一级类目失败: {str(e)}")
                return ApiResponse.error(
                    message="获取所有一级类目失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取所有一级类目服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取所有一级类目失败",
            status_code=500
        )

async def get_category_level2_service(request: Request) -> Response:
    """
    获取所有二级类目
    """
    try:
        async with AsyncSessionLocal() as db:
            try:
                category_level2 = await video_search_crud.get_category_level2(db)
                return ApiResponse.success(
                    data=[category.to_dict() for category in category_level2],
                    message="获取所有二级类目成功"
                )
            except Exception as e:
                logger.error(f"获取所有二级类目失败: {str(e)}")
                return ApiResponse.error(
                    message="获取所有二级类目失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取所有二级类目服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取所有二级类目失败",
            status_code=500
        )

async def get_category_level3_service(request: Request) -> Response:
    """
    获取所有三级类目
    """
    try:
        async with AsyncSessionLocal() as db:
            try:
                category_level3 = await video_search_crud.get_category_level3(db)
                return ApiResponse.success(
                    data=[category.to_dict() for category in category_level3],
                    message="获取所有三级类目成功"
                )
            except Exception as e:
                logger.error(f"获取所有三级类目失败: {str(e)}")
                return ApiResponse.error(
                    message="获取所有三级类目失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取所有三级类目服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取所有三级类目失败",
            status_code=500
        )


async def get_category_level2_by_level1_service(request: Request) -> Response:
    """
    查询指定一级类目下的所有二级类目
    """
    try:
        # 获取一级类目ID
        level1_id = request.path_params.get("level1_id")
        if not level1_id:
            return ApiResponse.validation_error("一级类目ID不能为空")

        # 获取二级类目
        filters = {
            "parent_value": level1_id
        }
        
        async with AsyncSessionLocal() as db:
            try:
                category_level2 = await video_search_crud.get_category_level2_by_filters(db, filters)
                return ApiResponse.success(
                    data=[category.to_dict() for category in category_level2],
                    message="获取指定一级类目下的所有二级类目成功"
                )
            except Exception as e:
                logger.error(f"获取指定一级类目下的所有二级类目失败: {str(e)}")
                return ApiResponse.error(
                    message="获取指定一级类目下的所有二级类目失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取指定一级类目下的所有二级类目服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取指定一级类目下的所有二级类目失败",
            status_code=500
        )


async def get_category_level3_by_level2_service(request: Request) -> Response:
    """
    查询指定二级类目下的所有三级类目
    """
    try:
        # 获取二级类目ID
        level2_id = request.path_params.get("level2_id")
        if not level2_id:
            return ApiResponse.validation_error("二级类目ID不能为空")

        # 获取三级类目
        filters = {
            "parent_value": level2_id
        }
        
        async with AsyncSessionLocal() as db:
            try:
                category_level3 = await video_search_crud.get_category_level3_by_filters(db, filters)
                return ApiResponse.success(
                    data=[category.to_dict() for category in category_level3],
                    message="获取指定二级类目下的所有三级类目成功"
                )
            except Exception as e:
                logger.error(f"获取指定二级类目下的所有三级类目失败: {str(e)}")
                return ApiResponse.error(
                    message="获取指定二级类目下的所有三级类目失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取指定二级类目下的所有三级类目服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取指定二级类目下的所有三级类目失败",
            status_code=500
        )
    

async def fetch_and_store_kalodata_service(request: Request) -> Response:
    """
    获取并存储kalodata视频数据服务
    """
    try:
        # 获取请求参数
        try:
            request_data = request.json()
            logger.info(f"接收到的请求数据: {request_data}")
        except Exception as e:
            logger.error(f"解析请求数据失败: {str(e)}")
            return ApiResponse.error(
                message="请求数据格式错误",
                status_code=400
            )

        cookie = request_data.get("cookie")
        country = request_data.get("country")
        start_date = request_data.get("start_date")
        end_date = request_data.get("end_date")
        
        # 处理cate_ids参数，确保它是列表格式
        try:
            cate_ids = request_data.get("cate_ids")
            if isinstance(cate_ids, str):
                import json
                cate_ids = json.loads(cate_ids)
            if not isinstance(cate_ids, list):
                return ApiResponse.validation_error("cate_ids必须是列表格式")
        except Exception as e:
            return ApiResponse.error(
                message="cate_ids格式错误",
                status_code=400
            )

        logger.info(f"处理后的参数: country={country}, start_date={start_date}, end_date={end_date}, cate_ids={cate_ids}")

        # 参数验证
        if not all([cookie, country, start_date, end_date]):
            missing_params = []
            if not cookie: missing_params.append("cookie")
            if not country: missing_params.append("country")
            if not start_date: missing_params.append("start_date")
            if not end_date: missing_params.append("end_date")
            return ApiResponse.validation_error(f"以下参数不能为空: {', '.join(missing_params)}")

        # 从kalodata获取数据
        try:
            from apps.search_video.utils import get_complete_video_data
            logger.info(f"开始从kalodata获取数据，参数：country={country}, start_date={start_date}, end_date={end_date}, cate_ids={cate_ids}")
            video_data = get_complete_video_data(cookie, country, start_date, end_date, cate_ids)
            logger.info(f"从kalodata获取到 {len(video_data) if video_data else 0} 条数据")
        except Exception as e:
            logger.error(f"从kalodata获取数据失败: {str(e)}")
            return ApiResponse.error(
                message=f"从kalodata获取数据失败: {str(e)}",
                status_code=500
            )

        if not video_data:
            return ApiResponse.error(
                message="从kalodata获取数据失败，返回数据为空",
                status_code=500
            )

        # 存储数据到数据库
        try:
            async with AsyncSessionLocal() as db:
                # 先获取当前请求的类目ID对应的类目名称
                # 只有当cate_ids不为空时进行查询
                category3_label = ""
                if cate_ids and len(cate_ids) > 0:
                    category_id = cate_ids[0]
                    from apps.search_video.utils import get_category3_label
                    category3_label = await get_category3_label(db, category_id)
                    logger.info(f"三级类目ID {category_id} 对应的名称: {category3_label}")
                
                success_count = 0
                skip_count = 0
                for video in video_data:
                    try:
                        # 构建数据模型
                        kalodata_data = {
                            "country": video.get("region", ""),
                            "has_ad": video.get("ad") == 1,
                            "video_name": video.get("description", ""),
                            "gpm": str(video.get("gpm", "")),
                            "cpm": str(video.get("ad_cpa", "")),
                            "ad_view_ratio": str(video.get("ad_view_ratio", "")),
                            "duration": str(video.get("duration", "")),
                            "revenue": str(video.get("revenue", "")),
                            "sales": str(video.get("sale", "")),
                            "roas": str(video.get("ad2Roas", "")),
                            "ad2Cost": str(video.get("ad2Cost", "")),
                            "views": str(video.get("views", "")),
                            "product_title": video.get("product_title", ""),
                            "product_price": str(video.get("product_price", "")),
                            "video_url": video.get("video_url", ""),
                            "tiktok_url": video.get("tiktok_url", ""),
                            "product_url": video.get("product_url", ""),
                            "product_image": "",  # 暂时为空，因为原始数据中没有这个字段
                            "username": video.get("username", video.get("handle", "")),
                            "follower_count": str(video.get("follower_count", "")),
                            "hashtags": ",".join(video.get("hashtags", [])),
                            "start_date": start_date,
                            "end_date": end_date,
                            "is_deleted": False
                        }
                        
                        # 处理API限制情况下的默认值
                        # 判断是否是API受限的情况 - 检查是否有关键字段为'unknown'
                        is_api_limited = (
                            video.get("product_title") == "unknown" or 
                            video.get("product_price") == "unknown" or 
                            video.get("follower_count") == "unknown" or
                            video.get("username") == "unknown"
                        )
                        
                        # 如果是API受限情况，确保所有必要字段都设置为'unknown'
                        if is_api_limited:
                            if kalodata_data["product_title"] == "":
                                kalodata_data["product_title"] = "unknown"
                            if kalodata_data["product_price"] == "":
                                kalodata_data["product_price"] = "unknown"
                            if kalodata_data["username"] == "":
                                kalodata_data["username"] = "unknown"
                            if kalodata_data["follower_count"] == "":
                                kalodata_data["follower_count"] = "unknown"
                        
                        # 处理类目字段
                        # 1. 获取原始类目ID
                        kalodata_data["category1"] = video.get("product_pri_cate_id", "")
                        kalodata_data["category2"] = video.get("product_sec_cate_id", "")
                        
                        # 2. 处理三级类目
                        ter_cate_id = video.get("product_ter_cate_id", "")
                        
                        # 如果三级类目ID不为空，但是API受限（无法获取产品详情）
                        if ter_cate_id and is_api_limited:
                            # 使用类目ID匹配到的名称
                            if category3_label and ter_cate_id == cate_ids[0]:
                                kalodata_data["category3"] = category3_label
                            else:
                                # 如果没有匹配到，尝试查询数据库获取类目名称
                                ter_category_label = await get_category3_label(db, ter_cate_id)
                                kalodata_data["category3"] = ter_category_label
                        else:
                            # 正常情况下，保留原始三级类目ID
                            kalodata_data["category3"] = ter_cate_id

                        # 检查数据是否已存在
                        exists = await video_search_crud.check_kalodata_exists(db, {
                            "country": kalodata_data["country"],
                            "video_name": kalodata_data["video_name"],
                            "product_title": kalodata_data["product_title"],
                            "start_date": kalodata_data["start_date"],
                            "end_date": kalodata_data["end_date"]
                        })

                        if exists:
                            logger.info(f"数据已存在，跳过: country={kalodata_data['country']}, video_name={kalodata_data['video_name']}, product_title={kalodata_data['product_title']}")
                            skip_count += 1
                            continue
                        
                        await video_search_crud.create_kalodata_data(db, kalodata_data)
                        success_count += 1
                    except Exception as e:
                        logger.error(f"存储单条kalodata数据失败: {str(e)}, 数据: {video}")
                        continue

                if success_count > 0 or skip_count > 0:
                    return ApiResponse.success(
                        message=f"成功获取并存储数据。新增: {success_count} 条，跳过: {skip_count} 条",
                        data={
                            "success_count": success_count,
                            "skip_count": skip_count,
                            "total_count": len(video_data)
                        }
                    )
                else:
                    return ApiResponse.error(
                        message="所有数据存储都失败了",
                        status_code=500
                    )
        except Exception as e:
            logger.error(f"存储kalodata数据过程中发生异常: {str(e)}")
            return ApiResponse.error(
                message=f"存储kalodata数据失败: {str(e)}",
                status_code=500
            )
    except Exception as e:
        logger.error(f"获取并存储kalodata数据服务发生未知异常: {str(e)}")
        return ApiResponse.error(
            message=f"获取并存储kalodata数据失败: {str(e)}",
            status_code=500
        )
    
async def get_kalodata_data_service(request: Request) -> Response:
    """
    获取单个kalodata数据服务
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
                kalodata_data = await video_search_crud.get_kalodata_data(db, id)
                if not kalodata_data:
                    return ApiResponse.not_found("kalodata数据不存在")
                
                return ApiResponse.success(
                    data=kalodata_data.to_dict(),
                    message="获取kalodata数据成功"
                )
            except Exception as e:
                logger.error(f"获取kalodata数据失败: {str(e)}")
                return ApiResponse.error(
                    message="获取kalodata数据失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取kalodata数据服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取kalodata数据失败",
            status_code=500
        )

async def get_all_kalodatas_service(request: Request) -> Response:
    """
    获取所有kalodata数据服务
    """
    try:
        async with AsyncSessionLocal() as db:
            try:
                kalodata_data = await video_search_crud.get_kalodata_datas(db)
                return ApiResponse.success(
                    data=[data.to_dict() for data in kalodata_data],
                    message="获取所有kalodata数据成功"
                )
            except Exception as e:
                logger.error(f"获取所有kalodata数据失败: {str(e)}")
                return ApiResponse.error(
                    message="获取所有kalodata数据失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取所有kalodata数据服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取所有kalodata数据失败",
            status_code=500
        )

async def get_kalodata_data_by_filters_service(request: Request) -> Response:
    """
    根据过滤条件获取kalodata数据服务
    """
    json_data = request.json()
    try:
        # 获取过滤条件
        filters = {
            "is_deleted": False  # 基础过滤条件
        }
        
        # 添加其他过滤条件
        if "country" in json_data:
            filters["country"] = json_data.get("country")
        if "category1" in json_data:
            filters["category1"] = json_data.get("category1")
        if "category2" in json_data:
            filters["category2"] = json_data.get("category2")
        if "category3" in json_data:
            filters["category3"] = json_data.get("category3")
        if "category" in json_data:
            filters["category3"] = json_data.get("category")
        if "start_date" in json_data:
            filters["start_date"] = json_data.get("start_date")
        if "end_date" in json_data:
            filters["end_date"] = json_data.get("end_date")

        # 获取排序条件
        order_by = {"created_at": "desc"}  # 默认按创建时间倒序排序
        
        # 获取分页参数
        try:
            page = int(json_data.get("page", "1"))
            page_size = int(json_data.get("page_size", "10"))
        except ValueError:
            page = 1
            page_size = 10
            
        # 验证分页参数
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10
            
        async with AsyncSessionLocal() as db:
            try:
                kalodata_data, total_count = await video_search_crud.get_kalodata_data_by_filters(
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
                        "items": [data.to_dict() for data in kalodata_data],
                        "total": total_count,
                        "page": page,
                        "page_size": page_size,
                        "total_pages": total_pages
                    },
                    message="根据过滤条件获取kalodata数据成功"
                )
            except Exception as e:
                logger.error(f"根据过滤条件获取kalodata数据失败: {str(e)}")
                return ApiResponse.error(
                    message="根据过滤条件获取kalodata数据失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"根据过滤条件获取kalodata数据服务异常: {str(e)}")
        return ApiResponse.error(
            message="根据过滤条件获取kalodata数据失败",
            status_code=500
        )
    

async def get_kalodata_data_by_category_country_service(request: Request) -> Response:
    """
    根据类目和国家获取kalodata数据服务
    """
    json_data = request.json()
    try:
        # 获取过滤条件
        filters = {
            "is_deleted": False  # 基础过滤条件
        }
        
        # 添加其他过滤条件
        if "country" in json_data:
            filters["country"] = json_data.get("country")
        if "category3" in json_data:  # 使用category3名称而不是ID
            filters["category3"] = json_data.get("category3")  # 这里直接使用category3的名称

        # 获取排序条件
        order_by = {"created_at": "desc"}  # 默认按创建时间倒序排序
        
        # 获取分页参数
        try:
            page = int(json_data.get("page", "1"))
            page_size = int(json_data.get("page_size", "5"))
        except ValueError:
            page = 1
            page_size = 5
            
        # 验证分页参数
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 5
            
        async with AsyncSessionLocal() as db:
            try:
                # 记录当前查询条件
                logger.info(f"查询参数: filters={filters}, order_by={order_by}, page={page}, page_size={page_size}")
                
                kalodata_data, total_count = await video_search_crud.get_kalodata_data_by_filters(
                    db,
                    filters=filters,
                    order_by=order_by,
                    page=page,
                    page_size=page_size
                )
                
                if not kalodata_data:  # 如果没有数据，返回空列表
                    return ApiResponse.success(
                        data={
                            "items": [],
                            "total": 0,
                            "page": page,
                            "page_size": page_size,
                            "total_pages": 0
                        },
                        message="根据类目和国家获取kalodata数据成功"
                    )
                
                # 计算总页数
                total_pages = (total_count + page_size - 1) // page_size

                return ApiResponse.success(
                    data={
                        "items": [data.to_dict() for data in kalodata_data],
                        "total": total_count,
                        "page": page,
                        "page_size": page_size,
                        "total_pages": total_pages
                    },
                    message="根据类目和国家获取kalodata数据成功"
                )
            except Exception as e:
                logger.error(f"根据类目和国家获取kalodata数据失败: {str(e)}")
                return ApiResponse.error(
                    message="根据类目和国家获取kalodata数据失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"根据类目和国家获取kalodata数据服务异常: {str(e)}")
        return ApiResponse.error(
            message="根据类目和国家获取kalodata数据失败",
            status_code=500
        )



async def update_kalodata_data_service(request: Request) -> Response:
    """
    更新kalodata数据服务
    """
    try:
        # 获取请求参数
        try:
            request_data = request.json()
            logger.info(f"接收到的请求数据: {request_data}")
        except Exception as e:
            logger.error(f"解析请求数据失败: {str(e)}")
            return ApiResponse.error(
                message="请求数据格式错误",
                status_code=400
            )

        id = request_data.get("id")
        if not id:
            return ApiResponse.validation_error("记录ID不能为空")
            
        try:
            id = int(id)
        except ValueError:
            return ApiResponse.validation_error("记录ID必须是整数")
        
        async with AsyncSessionLocal() as db:
            try:
                kalodata_data = await video_search_crud.get_kalodata_data(db, id)
                if not kalodata_data:
                    return ApiResponse.not_found("kalodata数据不存在")
                
                # 更新数据
                kalodata_data.update(request_data)
                await video_search_crud.update_kalodata_data(db, kalodata_data)
                
                return ApiResponse.success(
                    message="kalodata数据更新成功",
                    data=kalodata_data.to_dict()
                )
            except Exception as e:
                logger.error(f"更新kalodata数据失败: {str(e)}")
                return ApiResponse.error(
                    message="更新kalodata数据失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"更新kalodata数据服务异常: {str(e)}")
        return ApiResponse.error(
            message="更新kalodata数据失败",
            status_code=500
        )

async def delete_kalodata_data_service(request: Request) -> Response:
    """
    删除kalodata数据服务
    """
    try:
        # 获取请求参数
        try:
            id = request.path_params.get("id")
            logger.info(f"接收到的请求数据: {id}")
        except Exception as e:
            logger.error(f"解析请求数据失败: {str(e)}")
            return ApiResponse.error(
                message="请求数据格式错误",
                status_code=400
            )

        if not id:
            return ApiResponse.validation_error("记录ID不能为空")
            
        try:
            id = int(id)
        except ValueError:
            return ApiResponse.validation_error("记录ID必须是整数")
        
        async with AsyncSessionLocal() as db:
            try:
                await video_search_crud.delete_kalodata_data(db, id)
                
                return ApiResponse.success(
                    message="kalodata数据删除成功"
                )
            except Exception as e:
                logger.error(f"删除kalodata数据失败: {str(e)}")
                return ApiResponse.error(
                    message="删除kalodata数据失败",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"删除kalodata数据服务异常: {str(e)}")
        return ApiResponse.error(
            message="删除kalodata数据失败",
            status_code=500
        )
    

async def fetch_and_store_kalodata_by_categories_service(request: Request) -> Response:
    """
    根据所有三级类目批量获取并存储kalodata数据服务
    """
    try:
        # 获取请求参数
        try:
            request_data = request.json()
            logger.info(f"接收到的请求数据: {request_data}")
        except Exception as e:
            logger.error(f"解析请求数据失败: {str(e)}")
            return ApiResponse.error(
                message="请求数据格式错误",
                status_code=400
            )

        # 获取必要参数
        cookie = request_data.get("cookie")
        country = request_data.get("country")
        
        # 设置日期范围（默认为最近7天）
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        # 参数验证
        if not all([cookie, country]):
            missing_params = []
            if not cookie: missing_params.append("cookie")
            if not country: missing_params.append("country")
            return ApiResponse.validation_error(f"以下参数不能为空: {', '.join(missing_params)}")

        # 获取所有三级类目
        async with AsyncSessionLocal() as db:
            try:
                category_level3 = await video_search_crud.get_category_level3(db)
                if not category_level3:
                    return ApiResponse.error(
                        message="未找到任何三级类目数据",
                        status_code=404
                    )
                
                # 提取所有value值
                category_values = [category.value for category in category_level3]
                logger.info(f"获取到 {len(category_values)} 个三级类目")

                # 统计结果
                total_success = 0
                total_skip = 0
                total_fail = 0
                failed_categories = []
                processed_categories = []

                # 遍历每个类目值进行数据获取和存储
                for category_value in category_values:
                    try:
                        logger.info(f"开始处理类目 {category_value}")
                        
                        # 构造请求数据
                        fetch_data = {
                            "cookie": cookie,
                            "country": country,
                            "start_date": start_date,
                            "end_date": end_date,
                            "cate_ids": [category_value]
                        }
                        
                        # 调用现有的获取存储函数
                        mock_request = type('MockRequest', (), {'json': lambda: fetch_data})()
                        result = await fetch_and_store_kalodata_service(mock_request)
                        
                        # 检查结果
                        if result.status_code == 200:
                            result_data = json.loads(result.description)
                            if result_data.get("code") == 200:
                                success_count = result_data.get("data", {}).get("success_count", 0)
                                skip_count = result_data.get("data", {}).get("skip_count", 0)
                                total_success += success_count
                                total_skip += skip_count
                                
                                processed_categories.append({
                                    "category": category_value,
                                    "success_count": success_count,
                                    "skip_count": skip_count
                                })
                                
                                logger.info(f"类目 {category_value} 数据处理完成: 新增 {success_count} 条，跳过 {skip_count} 条")
                            else:
                                total_fail += 1
                                failed_categories.append({
                                    "category": category_value,
                                    "error": result_data.get("message", "未知错误")
                                })
                                logger.error(f"类目 {category_value} 数据获取存储失败: {result_data.get('message')}")
                        else:
                            total_fail += 1
                            failed_categories.append({
                                "category": category_value,
                                "error": "请求返回非200状态码",
                                "status_code": result.status_code
                            })
                            logger.error(f"类目 {category_value} 数据获取存储失败: 状态码 {result.status_code}")
                        
                        # 随机等待3-5秒
                        await asyncio.sleep(random.uniform(3, 5))
                        
                    except Exception as e:
                        total_fail += 1
                        failed_categories.append({
                            "category": category_value,
                            "error": str(e)
                        })
                        logger.error(f"处理类目 {category_value} 时发生错误: {str(e)}")
                        await asyncio.sleep(random.uniform(3, 5))  # 即使失败也等待，避免请求过快
                        continue

                # 返回处理结果
                return ApiResponse.success(
                    message=f"批量获取存储完成。新增: {total_success} 条，跳过: {total_skip} 条，失败类目: {total_fail} 个",
                    data={
                        "total_categories": len(category_values),
                        "success_count": total_success,
                        "skip_count": total_skip,
                        "failed_categories_count": total_fail,
                        "failed_categories": failed_categories,
                        "processed_categories": processed_categories
                    }
                )

            except Exception as e:
                logger.error(f"获取三级类目数据失败: {str(e)}")
                return ApiResponse.error(
                    message="获取三级类目数据失败",
                    status_code=500
                )
                
    except Exception as e:
        logger.error(f"批量获取并存储kalodata数据服务发生未知异常: {str(e)}")
        return ApiResponse.error(
            message=f"批量获取并存储kalodata数据失败: {str(e)}",
            status_code=500
        )
    

async def get_kalodata_data_statistics_service(request: Request) -> Response:
    """
    获取kalodata数据统计信息服务 - 返回指定country和category3的记录总数和最新end_date
    """
    json_data = request.json()
    try:
        # 获取过滤条件
        filters = {
            "is_deleted": False  # 基础过滤条件
        }
        
        # 添加其他过滤条件
        if "country" in json_data:
            filters["country"] = json_data.get("country")
        else:
            return ApiResponse.validation_error("country参数不能为空")
            
        if "category" in json_data:
            filters["category3"] = json_data.get("category")
        else:
            return ApiResponse.validation_error("category参数不能为空")

        async with AsyncSessionLocal() as db:
            try:
                # 查询记录总数
                from sqlalchemy import func, desc, select
                from apps.search_video.models import Kalodata_data
                
                # 构建基础查询
                query = select(Kalodata_data)
                
                # 添加过滤条件
                for key, value in filters.items():
                    if hasattr(Kalodata_data, key):
                        if value is not None:  # 只添加非空值的过滤条件
                            query = query.where(getattr(Kalodata_data, key) == value)
                
                # 计算总数
                count_query = select(func.count()).select_from(query.subquery())
                total = await db.scalar(count_query)
                
                # 查询最新日期 - 使用MAX函数
                formatted_date = None
                if total > 0:  # 只有当有记录时才查询最新日期
                    # 直接查询最大日期值
                    max_date_query = select(func.max(Kalodata_data.end_date)).select_from(Kalodata_data)
                    
                    # 添加过滤条件
                    for key, value in filters.items():
                        if hasattr(Kalodata_data, key):
                            if value is not None:
                                max_date_query = max_date_query.where(getattr(Kalodata_data, key) == value)
                    
                    # 执行查询获取最大日期
                    max_date_result = await db.execute(max_date_query)
                    latest_date = max_date_result.scalar_one_or_none()
                    
                    # 格式化日期
                    if latest_date:
                        try:
                            if hasattr(latest_date, 'strftime'):
                                formatted_date = latest_date.strftime("%Y-%m-%d %H:%M:%S")
                            else:
                                formatted_date = str(latest_date)
                        except Exception as date_error:
                            logger.error(f"格式化日期时出错: {str(date_error)}")
                            formatted_date = str(latest_date)
                            
                    # 记录调试信息
                    logger.info(f"查询参数: country={filters.get('country')}, category3={filters.get('category3')}")
                    logger.info(f"找到记录数: {total}, 最新日期: {formatted_date}")

                return ApiResponse.success(
                    data={
                        "total_count": total,
                        "latest_date": formatted_date,
                        "country": filters.get("country"),
                        "category": filters.get("category3")
                    },
                    message="获取kalodata数据统计信息成功"
                )
            except Exception as e:
                logger.error(f"获取kalodata数据统计信息失败: {str(e)}")
                return ApiResponse.error(
                    message=f"获取kalodata数据统计信息失败: {str(e)}",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"获取kalodata数据统计信息服务异常: {str(e)}")
        return ApiResponse.error(
            message="获取kalodata数据统计信息失败",
            status_code=500
        )


async def fetch_and_store_kalodata_service2(request: Request) -> Response:
    """
    获取并存储kalodata视频数据服务
    """
    try:
        # 获取请求参数
        try:
            # 检查请求类型
            if isinstance(request, dict):
                # 直接传入字典，最简单的情况
                request_data = request
                logger.info("请求对象是字典，直接使用")
            elif hasattr(request, 'json') and callable(request.json):
                # 标准Request对象，需要调用json()方法
                request_data = await request.json()
                logger.info("请求对象是标准Request，调用json()方法获取数据")
            elif hasattr(request, 'json') and isinstance(request.json, dict):
                # 自定义对象，json已经是字典
                request_data = request.json
                logger.info("请求对象有json属性且是字典，直接使用")
            else:
                # 未知类型，尝试获取属性或调用方法
                logger.warning(f"未知请求类型: {type(request)}, 尝试获取json数据")
                try:
                    if hasattr(request, 'json'):
                        if callable(request.json):
                            request_data = await request.json()
                        else:
                            request_data = request.json
                    elif hasattr(request, '__dict__'):
                        # 尝试将对象属性转为字典
                        request_data = request.__dict__
                    else:
                        # 最后尝试将整个请求对象当作字典处理
                        request_data = dict(request)
                except Exception as inner_e:
                    logger.error(f"尝试获取请求数据失败: {str(inner_e)}")
                    raise Exception(f"无法获取请求数据: {str(inner_e)}")
            
            logger.info(f"接收到的请求数据: {request_data}")
        except Exception as e:
            logger.error(f"解析请求数据失败: {str(e)}, 请求类型: {type(request)}")
            if hasattr(request, '__dict__'):
                logger.debug(f"请求对象属性: {request.__dict__}")
            return ApiResponse.error(
                message=f"请求数据格式错误: {str(e)}",
                status_code=400
            )

        # 提取并验证基本参数
        cookie = request_data.get("cookie")
        country = request_data.get("country")
        start_date = request_data.get("start_date")
        end_date = request_data.get("end_date")
        
        logger.info(f"基本参数: cookie长度={len(cookie) if cookie else 0}, country={country}, start_date={start_date}, end_date={end_date}")
        
        # 处理cate_ids参数，确保它是列表格式
        try:
            cate_ids = request_data.get("cate_ids")
            logger.debug(f"原始cate_ids: {cate_ids}, 类型: {type(cate_ids)}")
            
            if isinstance(cate_ids, str):
                import json
                try:
                    cate_ids = json.loads(cate_ids)
                    logger.debug(f"从JSON字符串解析cate_ids: {cate_ids}")
                except:
                    # 如果不是有效的JSON字符串，尝试单值转列表
                    cate_ids = [cate_ids]
                    logger.debug(f"将字符串转为列表: {cate_ids}")
            
            # 如果是单个值（非列表），转换为列表
            if cate_ids and not isinstance(cate_ids, list):
                cate_ids = [cate_ids]
                logger.debug(f"将非列表值转为列表: {cate_ids}")
                
            # 如果是空值，设置为空列表
            if not cate_ids:
                cate_ids = []
                logger.debug("cate_ids为空，设置为空列表")
                
            logger.info(f"处理后的cate_ids: {cate_ids}")
        except Exception as e:
            logger.error(f"处理cate_ids参数时出错: {str(e)}")
            cate_ids = []
            logger.debug("处理cate_ids出错，设置为空列表")

        logger.info(f"处理后的参数: country={country}, start_date={start_date}, end_date={end_date}, cate_ids={cate_ids}")

        # 参数验证
        missing_params = []
        if not cookie: missing_params.append("cookie")
        if not country: missing_params.append("country")
        if not start_date: missing_params.append("start_date")
        if not end_date: missing_params.append("end_date")
        if not cate_ids: missing_params.append("cate_ids")
            
        if missing_params:
            error_msg = f"以下参数不能为空: {', '.join(missing_params)}"
            logger.error(error_msg)
            return ApiResponse.validation_error(error_msg)

        # 从kalodata获取数据
        try:
            from apps.search_video.utils import get_complete_video_data
            logger.info(f"开始从kalodata获取数据，参数：country={country}, start_date={start_date}, end_date={end_date}, cate_ids={cate_ids}")
            video_data = get_complete_video_data(cookie, country, start_date, end_date, cate_ids)
            logger.info(f"从kalodata获取到 {len(video_data) if video_data else 0} 条数据")
        except Exception as e:
            logger.error(f"从kalodata获取数据失败: {str(e)}")
            return ApiResponse.error(
                message=f"从kalodata获取数据失败: {str(e)}",
                status_code=500
            )

        if not video_data:
            return ApiResponse.error(
                message="从kalodata获取数据失败，返回数据为空",
                status_code=500
            )

        # 存储数据到数据库
        try:
            async with AsyncSessionLocal() as db:
                # 先获取当前请求的类目ID对应的类目名称
                # 只有当cate_ids不为空时进行查询
                category3_label = ""
                if cate_ids and len(cate_ids) > 0:
                    category_id = cate_ids[0]
                    from apps.search_video.utils import get_category3_label
                    category3_label = await get_category3_label(db, category_id)
                    logger.info(f"三级类目ID {category_id} 对应的名称: {category3_label}")
                
                success_count = 0
                skip_count = 0
                for video in video_data:
                    try:
                        # 构建数据模型
                        kalodata_data = {
                            "country": video.get("region", ""),
                            "has_ad": video.get("ad") == 1,
                            "video_name": video.get("description", ""),
                            "gpm": str(video.get("gpm", "")),
                            "cpm": str(video.get("ad_cpa", "")),
                            "ad_view_ratio": str(video.get("ad_view_ratio", "")),
                            "duration": str(video.get("duration", "")),
                            "revenue": str(video.get("revenue", "")),
                            "sales": str(video.get("sale", "")),
                            "roas": str(video.get("ad2Roas", "")),
                            "ad2Cost": str(video.get("ad2Cost", "")),
                            "views": str(video.get("views", "")),
                            "product_title": video.get("product_title", ""),
                            "product_price": str(video.get("product_price", "")),
                            "video_url": video.get("video_url", ""),
                            "tiktok_url": video.get("tiktok_url", ""),
                            "product_url": video.get("product_url", ""),
                            "product_image": "",  # 暂时为空，因为原始数据中没有这个字段
                            "username": video.get("username", video.get("handle", "")),
                            "follower_count": str(video.get("follower_count", "")),
                            "hashtags": ",".join(video.get("hashtags", [])),
                            "start_date": start_date,
                            "end_date": end_date,
                            "is_deleted": False
                        }
                        
                        # 处理API限制情况下的默认值
                        # 判断是否是API受限的情况 - 检查是否有关键字段为'unknown'
                        is_api_limited = (
                            video.get("product_title") == "unknown" or 
                            video.get("product_price") == "unknown" or 
                            video.get("follower_count") == "unknown" or
                            video.get("username") == "unknown"
                        )
                        
                        # 如果是API受限情况，确保所有必要字段都设置为'unknown'
                        if is_api_limited:
                            if kalodata_data["product_title"] == "":
                                kalodata_data["product_title"] = "unknown"
                            if kalodata_data["product_price"] == "":
                                kalodata_data["product_price"] = "unknown"
                            if kalodata_data["username"] == "":
                                kalodata_data["username"] = "unknown"
                            if kalodata_data["follower_count"] == "":
                                kalodata_data["follower_count"] = "unknown"
                        
                        # 处理类目字段
                        # 1. 获取原始类目ID
                        kalodata_data["category1"] = video.get("product_pri_cate_id", "")
                        kalodata_data["category2"] = video.get("product_sec_cate_id", "")
                        
                        # 2. 处理三级类目
                        ter_cate_id = video.get("product_ter_cate_id", "")
                        
                        # 如果三级类目ID不为空，但是API受限（无法获取产品详情）
                        if ter_cate_id and is_api_limited:
                            # 使用类目ID匹配到的名称
                            if category3_label and ter_cate_id == cate_ids[0]:
                                kalodata_data["category3"] = category3_label
                            else:
                                # 如果没有匹配到，尝试查询数据库获取类目名称
                                ter_category_label = await get_category3_label(db, ter_cate_id)
                                kalodata_data["category3"] = ter_category_label
                        else:
                            # 正常情况下，保留原始三级类目ID
                            kalodata_data["category3"] = ter_cate_id

                        # 检查数据是否已存在
                        exists = await video_search_crud.check_kalodata_exists(db, {
                            "country": kalodata_data["country"],
                            "video_name": kalodata_data["video_name"],
                            "product_title": kalodata_data["product_title"],
                            "start_date": kalodata_data["start_date"],
                            "end_date": kalodata_data["end_date"]
                        })

                        if exists:
                            logger.info(f"数据已存在，跳过: country={kalodata_data['country']}, video_name={kalodata_data['video_name']}, product_title={kalodata_data['product_title']}")
                            skip_count += 1
                            continue
                        
                        await video_search_crud.create_kalodata_data(db, kalodata_data)
                        success_count += 1
                    except Exception as e:
                        logger.error(f"存储单条kalodata数据失败: {str(e)}, 数据: {video}")
                        continue

                if success_count > 0 or skip_count > 0:
                    return ApiResponse.success(
                        message=f"成功获取并存储数据。新增: {success_count} 条，跳过: {skip_count} 条",
                        data={
                            "success_count": success_count,
                            "skip_count": skip_count,
                            "total_count": len(video_data)
                        }
                    )
                else:
                    return ApiResponse.error(
                        message="所有数据存储都失败了",
                        status_code=500
                    )
        except Exception as e:
            logger.error(f"存储kalodata数据过程中发生异常: {str(e)}")
            return ApiResponse.error(
                message=f"存储kalodata数据失败: {str(e)}",
                status_code=500
            )
    except Exception as e:
        logger.error(f"获取并存储kalodata数据服务发生未知异常: {str(e)}")
        return ApiResponse.error(
            message=f"获取并存储kalodata数据失败: {str(e)}",
            status_code=500
        )

async def fetch_and_store_kalodata_by_category1_service(request: Request) -> Response:
    """
    根据一级类目和国家批量获取并存储kalodata数据服务
    使用树形遍历思路：获取一级类目下的二级类目列表->获取所有二级类目下的三级类目->批量获取并存储所有三级类目的数据
    """
    try:
        # 获取请求参数
        try:
            request_data = request.json()
            logger.info(f"接收到的请求数据: {request_data}")
        except Exception as e:
            logger.error(f"解析请求数据失败: {str(e)}")
            return ApiResponse.error(
                message="请求数据格式错误",
                status_code=400
            )

        # 获取必要参数
        cookie = request_data.get("cookie")
        country = request_data.get("country")
        category1_value = request_data.get("category1")  # 一级类目的value值
        
        # 设置日期范围（默认为前一天和前7天）
        from datetime import datetime, timedelta
        end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        # 参数验证
        if not all([cookie, country, category1_value]):
            missing_params = []
            if not cookie: missing_params.append("cookie")
            if not country: missing_params.append("country")
            if not category1_value: missing_params.append("category1")
            return ApiResponse.validation_error(f"以下参数不能为空: {', '.join(missing_params)}")

        # 统计结果
        total_success = 0
        total_skip = 0
        total_fail = 0
        failed_categories = []
        processed_categories = []
        category2_info = []
        category3_info = []

        async with AsyncSessionLocal() as db:
            try:
                # 1. 获取指定一级类目下的所有二级类目
                logger.info(f"开始获取一级类目 {category1_value} 下的所有二级类目")
                category2_list = await video_search_crud.get_category_level2_by_filters(db, {"parent_value": category1_value})
                if not category2_list:
                    return ApiResponse.error(
                        message=f"未找到一级类目 {category1_value} 下的任何二级类目数据",
                        status_code=404
                    )
                
                logger.info(f"获取到 {len(category2_list)} 个二级类目")
                
                # 2. 遍历每个二级类目，获取其下的所有三级类目
                all_category3 = []
                for category2 in category2_list:
                    category2_value = category2.value
                    category2_info.append({
                        "value": category2_value,
                        "label": category2.label
                    })
                    
                    logger.info(f"获取二级类目 {category2_value} 下的所有三级类目")
                    category3_list = await video_search_crud.get_category_level3_by_filters(db, {"parent_value": category2_value})
                    
                    if category3_list:
                        # 记录二级类目下有多少三级类目
                        current_category3_info = []
                        for category3 in category3_list:
                            all_category3.append(category3)
                            current_category3_info.append({
                                "value": category3.value,
                                "label": category3.label
                            })
                        
                        category3_info.append({
                            "category2_value": category2_value,
                            "category2_label": category2.label,
                            "category3_list": current_category3_info,
                            "count": len(current_category3_info)
                        })
                
                if not all_category3:
                    return ApiResponse.error(
                        message=f"未找到一级类目 {category1_value} 下的任何三级类目数据",
                        status_code=404
                    )
                
                logger.info(f"共找到 {len(all_category3)} 个三级类目")
                
                # 3. 遍历每个三级类目，获取并存储数据
                for category3 in all_category3:
                    # 随机等待3-5秒，避免请求过快
                    await asyncio.sleep(random.uniform(1, 3))
                    try:
                        category3_value = category3.value
                        category3_label = category3.label
                        
                        logger.info(f"开始处理三级类目 {category3_label}({category3_value})")
                        
                        # 构造请求数据
                        fetch_data = {
                            "cookie": cookie,
                            "country": country,
                            "start_date": start_date,
                            "end_date": end_date,
                            "cate_ids": [category3_value]
                        }
                        
                        # 调用现有的获取存储函数
                        try:
                            # 直接将数据字典传递给服务函数
                            logger.info(f"调用fetch_and_store_kalodata_service2获取数据，参数: {fetch_data}")
                            result = await fetch_and_store_kalodata_service2(fetch_data)
                            
                            # 检查结果
                            if result.status_code == 200:
                                try:
                                    # 检查结果类型
                                    if hasattr(result, 'description') and isinstance(result.description, str):
                                        # ApiResponse类型
                                        try:
                                            result_data = json.loads(result.description)
                                        except json.JSONDecodeError:
                                            # 如果不是JSON字符串，直接使用
                                            result_data = {"code": 200, "message": result.description}
                                    elif isinstance(result, dict):
                                        # 已经是字典格式
                                        result_data = result
                                    else:
                                        # 其他格式，尝试获取数据
                                        result_data = {"code": 200, "message": "数据处理成功但无法解析结果"}
                                    
                                    logger.info(f"服务返回的处理结果: {result_data}")
                                    
                                    if result_data.get("code") == 200:
                                        # 提取成功和跳过计数，兼容不同数据结构
                                        if "data" in result_data and isinstance(result_data["data"], dict):
                                            success_count = result_data.get("data", {}).get("success_count", 0)
                                            skip_count = result_data.get("data", {}).get("skip_count", 0)
                                        else:
                                            # 数据不符合预期结构，尝试其他位置
                                            success_count = result_data.get("success_count", 0)
                                            skip_count = result_data.get("skip_count", 0)
                                        
                                        total_success += success_count
                                        total_skip += skip_count
                                        
                                        processed_categories.append({
                                            "category3_value": category3_value,
                                            "category3_label": category3_label,
                                            "success_count": success_count,
                                            "skip_count": skip_count
                                        })
                                        
                                        # 添加到category3_info
                                        category3_info.append({
                                            "value": category3_value,
                                            "label": category3_label,
                                            "success_count": success_count,
                                            "skip_count": skip_count
                                        })
                                        
                                        logger.info(f"三级类目 {category3_label}({category3_value}) 数据处理完成: 新增 {success_count} 条，跳过 {skip_count} 条")
                                    else:
                                        # 结果返回非成功状态码
                                        raise Exception(f"返回码不为200: {result_data.get('message', '未知错误')}")
                                except Exception as parse_error:
                                    logger.error(f"解析结果数据失败: {str(parse_error)}")
                                    raise
                            else:
                                # 处理非200状态码
                                error_message = f"请求返回非200状态码: {result.status_code}"
                                if hasattr(result, 'description'):
                                    try:
                                        error_data = json.loads(result.description)
                                        if 'message' in error_data:
                                            error_message = error_data['message']
                                    except:
                                        pass
                                raise Exception(error_message)
                                
                        except Exception as service_error:
                            logger.error(f"调用fetch_and_store_kalodata_service失败: {str(service_error)}")
                            total_fail += 1
                            failed_categories.append({
                                "category3_value": category3_value,
                                "category3_label": category3_label,
                                "error": str(service_error)
                            })
                            logger.error(f"三级类目 {category3_label}({category3_value}) 数据获取存储失败: {str(service_error)}")
                            
                        # 随机等待3-5秒，避免请求过快
                        await asyncio.sleep(random.uniform(3, 5))
                        
                    except Exception as e:
                        total_fail += 1
                        failed_categories.append({
                            "category3_value": category3_value,
                            "category3_label": category3_label,
                            "error": str(e)
                        })
                        logger.error(f"处理三级类目 {category3_label}({category3_value}) 时发生错误: {str(e)}")
                        await asyncio.sleep(random.uniform(3, 5))  # 即使失败也等待，避免请求过快
                        continue

                # 返回处理结果
                return ApiResponse.success(
                    message=f"根据一级类目和国家批量获取存储完成。新增: {total_success} 条，跳过: {total_skip} 条，失败类目: {total_fail} 个",
                    data={
                        "category1_value": category1_value,
                        "country": country,
                        "total_category2": len(category2_list),
                        "total_category3": len(all_category3),
                        "start_date": start_date,
                        "end_date": end_date,
                        "success_count": total_success,
                        "skip_count": total_skip,
                        "failed_categories_count": total_fail,
                        "category2_info": category2_info,
                        "category3_info": category3_info,
                        "failed_categories": failed_categories,
                        "processed_categories": processed_categories
                    }
                )
            except Exception as e:
                logger.error(f"获取类目数据失败: {str(e)}")
                return ApiResponse.error(
                    message=f"获取类目数据失败: {str(e)}",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"根据一级类目和国家批量获取并存储kalodata数据服务发生未知异常: {str(e)}")
        return ApiResponse.error(
            message=f"根据一级类目和国家批量获取并存储kalodata数据失败: {str(e)}",
            status_code=500
        )

async def fetch_and_store_kalodata_by_category2_service(request: Request) -> Response:
    """
    根据二级类目和国家批量获取并存储kalodata数据服务
    获取指定二级类目下的所有三级类目->批量获取并存储所有三级类目的数据
    """
    try:
        # 获取请求参数
        try:
            request_data = request.json()
            logger.info(f"接收到的请求数据: {request_data}")
        except Exception as e:
            logger.error(f"解析请求数据失败: {str(e)}")
            return ApiResponse.error(
                message="请求数据格式错误",
                status_code=400
            )

        # 获取必要参数
        cookie = request_data.get("cookie")
        country = request_data.get("country")
        category2_value = request_data.get("category2")  # 二级类目的value值
        
        # 设置日期范围（默认为前一天和前7天）
        from datetime import datetime, timedelta
        end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        # 自定义日期范围
        if "start_date" in request_data and request_data["start_date"]:
            start_date = request_data["start_date"]
        if "end_date" in request_data and request_data["end_date"]:
            end_date = request_data["end_date"]

        # 参数验证
        if not all([cookie, country, category2_value]):
            missing_params = []
            if not cookie: missing_params.append("cookie")
            if not country: missing_params.append("country")
            if not category2_value: missing_params.append("category2")
            return ApiResponse.validation_error(f"以下参数不能为空: {', '.join(missing_params)}")

        # 统计结果
        total_success = 0
        total_skip = 0
        total_fail = 0
        failed_categories = []
        processed_categories = []
        category3_info = []

        async with AsyncSessionLocal() as db:
            try:
                # 1. 获取指定二级类目信息
                logger.info(f"开始获取二级类目 {category2_value} 信息")
                category2_query = await video_search_crud.get_category_level2_by_value(db, category2_value)
                if not category2_query:
                    return ApiResponse.error(
                        message=f"未找到二级类目 {category2_value}",
                        status_code=404
                    )
                
                category2_label = category2_query.label
                
                # 2. 获取指定二级类目下的所有三级类目
                logger.info(f"获取二级类目 {category2_value} 下的所有三级类目")
                category3_list = await video_search_crud.get_category_level3_by_filters(db, {"parent_value": category2_value})
                
                if not category3_list:
                    return ApiResponse.error(
                        message=f"未找到二级类目 {category2_value} 下的任何三级类目数据",
                        status_code=404
                    )
                
                logger.info(f"获取到 {len(category3_list)} 个三级类目")
                
                # 3. 遍历每个三级类目，获取并存储数据
                for category3 in category3_list:
                    # 随机等待1-3秒，避免请求过快
                    await asyncio.sleep(random.uniform(1, 3))
                    try:
                        category3_value = category3.value
                        category3_label = category3.label
                        
                        logger.info(f"开始处理三级类目 {category3_label}({category3_value})")
                        
                        # 构造请求数据
                        fetch_data = {
                            "cookie": cookie,
                            "country": country,
                            "start_date": start_date,
                            "end_date": end_date,
                            "cate_ids": [category3_value]
                        }
                        
                        # 调用现有的获取存储函数
                        try:
                            # 直接将数据字典传递给服务函数
                            logger.info(f"调用fetch_and_store_kalodata_service2获取数据，参数: {fetch_data}")
                            result = await fetch_and_store_kalodata_service2(fetch_data)
                            
                            # 检查结果
                            if result.status_code == 200:
                                try:
                                    # 检查结果类型
                                    if hasattr(result, 'description') and isinstance(result.description, str):
                                        # ApiResponse类型
                                        try:
                                            result_data = json.loads(result.description)
                                        except json.JSONDecodeError:
                                            # 如果不是JSON字符串，直接使用
                                            result_data = {"code": 200, "message": result.description}
                                    elif isinstance(result, dict):
                                        # 已经是字典格式
                                        result_data = result
                                    else:
                                        # 其他格式，尝试获取数据
                                        result_data = {"code": 200, "message": "数据处理成功但无法解析结果"}
                                    
                                    logger.info(f"服务返回的处理结果: {result_data}")
                                    
                                    if result_data.get("code") == 200:
                                        # 提取成功和跳过计数，兼容不同数据结构
                                        if "data" in result_data and isinstance(result_data["data"], dict):
                                            success_count = result_data.get("data", {}).get("success_count", 0)
                                            skip_count = result_data.get("data", {}).get("skip_count", 0)
                                        else:
                                            # 数据不符合预期结构，尝试其他位置
                                            success_count = result_data.get("success_count", 0)
                                            skip_count = result_data.get("skip_count", 0)
                                        
                                        total_success += success_count
                                        total_skip += skip_count
                                        
                                        processed_categories.append({
                                            "category3_value": category3_value,
                                            "category3_label": category3_label,
                                            "success_count": success_count,
                                            "skip_count": skip_count
                                        })
                                        
                                        # 添加到category3_info
                                        category3_info.append({
                                            "value": category3_value,
                                            "label": category3_label,
                                            "success_count": success_count,
                                            "skip_count": skip_count
                                        })
                                        
                                        logger.info(f"三级类目 {category3_label}({category3_value}) 数据处理完成: 新增 {success_count} 条，跳过 {skip_count} 条")
                                    else:
                                        # 结果返回非成功状态码
                                        raise Exception(f"返回码不为200: {result_data.get('message', '未知错误')}")
                                except Exception as parse_error:
                                    logger.error(f"解析结果数据失败: {str(parse_error)}")
                                    raise
                            else:
                                # 处理非200状态码
                                error_message = f"请求返回非200状态码: {result.status_code}"
                                if hasattr(result, 'description'):
                                    try:
                                        error_data = json.loads(result.description)
                                        if 'message' in error_data:
                                            error_message = error_data['message']
                                    except:
                                        pass
                                raise Exception(error_message)
                                
                        except Exception as service_error:
                            logger.error(f"调用fetch_and_store_kalodata_service失败: {str(service_error)}")
                            total_fail += 1
                            failed_categories.append({
                                "category3_value": category3_value,
                                "category3_label": category3_label,
                                "error": str(service_error)
                            })
                            logger.error(f"三级类目 {category3_label}({category3_value}) 数据获取存储失败: {str(service_error)}")
                            
                        # 随机等待3-5秒，避免请求过快
                        await asyncio.sleep(random.uniform(3, 5))
                        
                    except Exception as e:
                        total_fail += 1
                        failed_categories.append({
                            "category3_value": category3_value,
                            "category3_label": category3_label,
                            "error": str(e)
                        })
                        logger.error(f"处理三级类目 {category3_label}({category3_value}) 时发生错误: {str(e)}")
                        await asyncio.sleep(random.uniform(3, 5))  # 即使失败也等待，避免请求过快
                        continue

                # 返回处理结果
                return ApiResponse.success(
                    message=f"根据二级类目和国家批量获取存储完成。新增: {total_success} 条，跳过: {total_skip} 条，失败类目: {total_fail} 个",
                    data={
                        "category2_value": category2_value,
                        "category2_label": category2_label,
                        "country": country,
                        "total_category3": len(category3_list),
                        "start_date": start_date,
                        "end_date": end_date,
                        "success_count": total_success,
                        "skip_count": total_skip,
                        "failed_categories_count": total_fail,
                        "category3_info": category3_info,
                        "failed_categories": failed_categories,
                        "processed_categories": processed_categories
                    }
                )
            except Exception as e:
                logger.error(f"获取类目数据失败: {str(e)}")
                return ApiResponse.error(
                    message=f"获取类目数据失败: {str(e)}",
                    status_code=500
                )
    except Exception as e:
        logger.error(f"根据二级类目和国家批量获取并存储kalodata数据服务发生未知异常: {str(e)}")
        return ApiResponse.error(
            message=f"根据二级类目和国家批量获取并存储kalodata数据失败: {str(e)}",
            status_code=500
        )

