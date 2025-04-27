from robyn import Request
from apps.users.api import (
    create_user_api,
    get_all_users_api,
    get_user_by_phone_api,
    get_users_api,
    get_user_api,
    update_user_api,
    delete_user_api,
    update_user_field_api,
    get_token_api,
    check_token_api
)
from core.middleware import error_handler, request_logger, auth_required, admin_required, rate_limit


def users_api_routes(app):
    """
    注册用户路由
    API 路由 - 用于后端接口
    路由层 应该专注于 处理请求 并 返回响应
    """
    @app.get("/api/users")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)  # 限制每分钟最多100次请求
    async def users_get(request):
        """
        获取所有用户
        """
        return await get_all_users_api(request)
    
    @app.get("/api/users/:user_id")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def user_get(request):
        """
        通过用户ID获取单个用户
        """
        return await get_user_api(request)
    
    
    @app.get("/api/users/phone/:phone")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def user_get_by_phone(request):
        """
        通过手机号获取单个用户
        """
        return await get_user_by_phone_api(request)

    @app.post("/api/users")
    @error_handler
    @request_logger
    @rate_limit(max_requests=20, time_window=60)  # 限制每分钟最多20次创建请求
    async def users_create(request):
        """
        创建用户
        """
        return await create_user_api(request)
    
    @app.put("/api/users/:user_id")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def user_update(request):
        """
        更新用户
        """
        return await update_user_api(request)
    
    @app.patch("/api/users/:user_id")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def user_update_field(request):
        """
        更新用户指定字段
        """
        return await update_user_field_api(request)
    
    @app.delete("/api/users/:user_id")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def user_delete(request):
        """
        删除用户
        """
        return await delete_user_api(request)
    
    @app.get("/api/users/token/:user_id")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def gettoken_byuserid(request):
        """
        获取token
        """
        return await get_token_api(request)
    
    @app.get("/api/users/check_token")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def check_token(request):
        """
        检查token状态
        """
        return await check_token_api(request)
    

    @app.post("/api/admins")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def create_admin(request):
        """
        创建管理员
        """
        from apps.users.api import create_admin_api
        return await create_admin_api(request)
    
    @app.patch("/api/admins/:admin_id")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def update_admin(request):
        """
        更新管理员
        """
        from apps.users.api import update_admin_api
        return await update_admin_api(request)
    
    @app.delete("/api/admins/:admin_id")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def delete_admin(request):
        """
        删除管理员
        """
        from apps.users.api import delete_admin_api
        return await delete_admin_api(request)
    
    @app.get("/api/admins/:admin_id")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def get_admin(request):
        """
        获取管理员
        """
        from apps.users.api import get_admin_api
        return await get_admin_api(request)
    
    @app.get("/api/admins")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def get_admins(request):
        """
        获取所有管理员
        """
        from apps.users.api import get_admins_api
        return await get_admins_api(request)
    
    @app.post("/api/admins/login")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def login_admin(request):
        """
        管理员登录
        """
        from apps.users.api import login_admin_api
        return await login_admin_api(request)
    
    @app.post("/api/admins/logout")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def logout_admin(request):
        """
        管理员登出
        """
        from apps.users.api import logout_admin_api
        return await logout_admin_api(request)
    
    @app.get("/api/users/count")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def get_user_count(request):
        """
        获取用户总数
        """
        from apps.users.api import get_user_count_api
        return await get_user_count_api(request)
    

    @app.post("/api/users/search")
    @error_handler
    @request_logger
    @rate_limit(max_requests=100, time_window=60)
    async def search_users_by_phone_prefix(request):
        """
        根据手机号前缀搜索用户
        """
        from apps.users.api import search_users_by_phone_prefix_api
        return await search_users_by_phone_prefix_api(request)