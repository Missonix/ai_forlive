from robyn.robyn import Request
from apps.users.queries import get_user, get_user_by_id, get_users_service
from apps.users.services import create_user_service, delete_user_service, get_user_by_phone, update_user_field_service, update_user_service, get_token, check_token, get_user_count_service

"""
    定义用户API接口
    接口层 应该专注于 处理基础的数据库操作 并 返回成功的状态码及数据内容
    接口层避免直接暴露在外,应该由服务层调用
"""

# 查询
async def get_all_users_api(request: Request):
    """
    获取所有用户 接口
    """
    return await get_users_service(request)

async def get_user_api(request: Request):
    """
    通过用户ID获取单个用户 接口
    """
    return await get_user_by_id(request)


async def get_user_by_phone_api(request: Request):
    """
    通过手机号获取单个用户 接口
    """
    phone = request.path_params.get("phone")  # 从路径参数获取phone
    return await get_user_by_phone(phone)
    

async def get_users_api(request: Request):
    """
    通过用户ID、手机号查询用户 接口
    """
    userdata = request.path_params.get("userdata")  # 从路径参数获取userdata
    return await get_user(userdata)

async def create_user_api(request: Request):
    """
    创建用户
    """
    return await create_user_service(request) 

async def update_user_api(request: Request):
    """
    更新用户
    """
    return await update_user_service(request)


# @app.patch("/user/:user_id")
async def update_user_field_api(request: Request):
    """
    更新用户指定字段
    """
    return await update_user_field_service(request)


async def delete_user_api(request: Request):
    """
    删除用户
    """
    return await delete_user_service(request)

async def get_token_api(request: Request):
    """
    获取token
    """
    return await get_token(request)

async def check_token_api(request: Request):
    """
    检查token状态
    """
    return await check_token(request)


async def create_admin_api(request: Request):
    """
    创建管理员
    """
    from apps.users.services import create_admin_service
    return await create_admin_service(request)

async def update_admin_api(request: Request):
    """
    更新管理员
    """
    from apps.users.services import update_admin_service
    return await update_admin_service(request)

async def delete_admin_api(request: Request):
    """
    删除管理员
    """
    from apps.users.services import delete_admin_service
    return await delete_admin_service(request)

async def get_admin_api(request: Request):
    """
    获取管理员
    """
    from apps.users.services import get_admin_service
    return await get_admin_service(request)

async def get_admins_api(request: Request):
    """
    获取所有管理员
    """
    from apps.users.services import get_admins_service
    return await get_admins_service(request)

async def login_admin_api(request: Request):
    """
    管理员登录
    """
    from apps.users.services import login_admin_service
    return await login_admin_service(request)

async def logout_admin_api(request: Request):
    """
    管理员登出
    """
    from apps.users.services import logout_admin_service
    return await logout_admin_service(request)

async def get_user_count_api(request: Request):
    """
    获取用户总数
    """
    from apps.users.services import get_user_count_service
    return await get_user_count_service(request)
    
async def search_users_by_phone_prefix_api(request: Request):
    """
    根据手机号前缀搜索用户
    """
    from apps.users.services import search_users_by_phone_prefix_service
    return await search_users_by_phone_prefix_service(request)

