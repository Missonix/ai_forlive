from robyn import Robyn, Request
from apps.search_video.views.views import (
    search_video, 
    get_all_video_search_histories, 
    get_search_history, 
    get_search_history_by_phone,
    get_category_level1, 
    get_category_level2_by_level1, 
    get_category_level3_by_level2, 
    get_category_level2, 
    get_category_level3,
    fetch_and_store_kalodata,
    get_kalodata_data,
    get_kalodata_datas,
    get_kalodata_data_by_filters,
    update_kalodata_data,
    delete_kalodata_data,
    fetch_and_store_kalodata_by_categories,
    get_kalodata_data_statistics,
    fetch_and_store_kalodata_by_category1,
    fetch_and_store_kalodata_by_category2,
    get_kalodata_data_by_category_country
)

def search_video_view_routes(app):
    """
     对标视频搜索与推荐记录 路由 
    路由层 应该专注于 处理请求 并 返回响应
    """
    
    app.add_route(route_type="POST", endpoint="/api/search_video", handler=search_video) # 对标视频搜索与推荐路由
    app.add_route(route_type="POST", endpoint="/search_video", handler=search_video) # 对标视频搜索与推荐路由
    app.add_route(route_type="GET", endpoint="/api/search_video/histories", handler=get_all_video_search_histories) # 获取所有对标视频搜索与推荐记录路由
    app.add_route(route_type="GET", endpoint="/api/search_video/history/:id", handler=get_search_history) # 获取单个对标视频搜索与推荐记录路由
    app.add_route(route_type="GET", endpoint="/search_video/history/phone/:phone", handler=get_search_history_by_phone) # 根据手机号搜索对标视频搜索与推荐记录路由

    app.add_route(route_type="GET", endpoint="/api/search_video/category/level1", handler=get_category_level1) # 后台：获取所有一级类目路由
    app.add_route(route_type="GET", endpoint="/api/search_video/category/level2/:level1_id", handler=get_category_level2_by_level1) # 后台：查询指定一级类目下的所有二级类目路由
    app.add_route(route_type="GET", endpoint="/api/search_video/category/level3/:level2_id", handler=get_category_level3_by_level2) # 后台：查询指定二级类目下的所有三级类目路由

    app.add_route(route_type="GET", endpoint="/search_video/category/level1", handler=get_category_level1) # 前台：获取所有一级类目路由
    app.add_route(route_type="GET", endpoint="/search_video/category/level2/:level1_id", handler=get_category_level2_by_level1) # 前台：查询指定一级类目下的所有二级类目路由
    app.add_route(route_type="GET", endpoint="/search_video/category/level3/:level2_id", handler=get_category_level3_by_level2) # 前台：查询指定二级类目下的所有三级类目路由

    app.add_route(route_type="GET", endpoint="/search_video/category/level2", handler=get_category_level2) # 获取所有二级类目路由
    app.add_route(route_type="GET", endpoint="/search_video/category/level3", handler=get_category_level3) # 获取所有三级类目路由

    app.add_route(route_type="POST", endpoint="/api/search_video/kalodata/fetch_and_store", handler=fetch_and_store_kalodata) # 获取并存储kalodata数据路由
    app.add_route(route_type="POST", endpoint="/api/search_video/kalodata/fetch_and_store_by_categories", handler=fetch_and_store_kalodata_by_categories) # 根据所有三级类目批量获取并存储kalodata数据路由

    app.add_route(route_type="GET", endpoint="/api/search_video/kalodata/data/:id", handler=get_kalodata_data) # 获取单个kalodata数据路由
    app.add_route(route_type="GET", endpoint="/api/search_video/kalodata/datas", handler=get_kalodata_datas) # 获取所有kalodata数据路由
    app.add_route(route_type="POST", endpoint="/api/search_video/kalodata/data/filters", handler=get_kalodata_data_by_filters) # 根据过滤条件获取kalodata数据路由
    app.add_route(route_type="POST", endpoint="/api/search_video/kalodata/data/by_category_country", handler=get_kalodata_data_by_category_country) # 根据类目和国家获取kalodata数据路由
    app.add_route(route_type="PATCH", endpoint="/api/search_video/kalodata/data/:id", handler=update_kalodata_data) # 更新kalodata数据路由
    app.add_route(route_type="DELETE", endpoint="/api/search_video/kalodata/data/:id", handler=delete_kalodata_data) # 删除kalodata数据路由

    app.add_route(route_type="POST", endpoint="/api/search_video/kalodata/statistics", handler=get_kalodata_data_statistics) # 获取kalodata数据统计信息路由
    app.add_route(route_type="POST", endpoint="/api/search_video/kalodata/statistics/by_category", handler=fetch_and_store_kalodata_by_category1) # 根据一级类目获取所有三级类目kalodata数据路由
    app.add_route(route_type="POST", endpoint="/api/search_video/kalodata/statistics/by_category2", handler=fetch_and_store_kalodata_by_category2) # 根据二级类目获取所有三级类目kalodata数据路由

