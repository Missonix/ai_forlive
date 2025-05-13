from robyn import Robyn, Request
from apps.search_video.views.views import search_video, get_all_video_search_histories, get_search_history, get_search_history_by_phone

def search_video_view_routes(app):
    """
     对标视频搜索与推荐记录 路由 
    路由层 应该专注于 处理请求 并 返回响应
    """
    
    app.add_route(route_type="POST", endpoint="/search_video", handler=search_video) # 对标视频搜索与推荐路由
    app.add_route(route_type="GET", endpoint="/search_video/histories", handler=get_all_video_search_histories) # 获取所有对标视频搜索与推荐记录路由
    app.add_route(route_type="GET", endpoint="/search_video/history/:id", handler=get_search_history) # 获取单个对标视频搜索与推荐记录路由
    app.add_route(route_type="GET", endpoint="/search_video/history/phone/:phone", handler=get_search_history_by_phone) # 根据手机号搜索对标视频搜索与推荐记录路由
