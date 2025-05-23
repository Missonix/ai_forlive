import os
from robyn import Request, Response, Robyn, status_codes, HttpMethod
from apps.users.api_routes import users_api_routes # 导入用户接口路由
from apps.users.views.view_routes import users_view_routes # 导入用户视图路由
from apps.vio_word.views.view_routes import vio_word_view_routes # 导入违规词检测视图路由
from pathlib import Path
from settings import configure_cors
from core.cache import Cache
from core.logger import setup_logger
import asyncio
from apps.business.api_routes import business_api_routes # 导入业务接口路由
from core.scheduler import start_scheduler
from apps.search_video.views.view_routes import search_video_view_routes # 导入对标视频搜索与推荐视图路由
# 设置日志记录器
logger = setup_logger('main')

# 创建 Robyn 实例
app = Robyn(__file__)

# 配置CORS
configure_cors(app)

# # 配置静态资源
# serve_static_files(app)


# 注册用户服务接口路由
users_api_routes(app)

# 注册业务服务接口路由
business_api_routes(app)

# 注册用户服务视图路由
users_view_routes(app)

# 注册违规词检测视图路由
vio_word_view_routes(app)

# 注册对标视频搜索与推荐视图路由
search_video_view_routes(app)

# 初始化Redis连接的路由
@app.get("/initialize")
async def initialize(request: Request) -> Response:
    """初始化应用的路由"""
    try:
        await Cache.init()
        logger.info("Application initialized successfully")
        return Response(status_code=status_codes.HTTP_200_OK, description="Initialization successful")
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        return Response(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            description="Failed to initialize"
        )

# 关闭Redis连接的路由
@app.get("/shutdown")
async def shutdown(request: Request) -> Response:
    """关闭应用的路由"""
    try:
        await Cache.close()
        logger.info("Application shutdown completed")
        return Response(status_code=status_codes.HTTP_200_OK, description="Shutdown successful")
    except Exception as e:
        logger.error(f"Error during application shutdown: {str(e)}")
        return Response(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            description="Failed to shutdown"
        )

# 启动调度器函数
async def init_scheduler():
    try:
        # 启动调度器
        await start_scheduler()
        logger.info("调度器启动成功")
    except Exception as e:
        logger.error(f"调度器启动失败: {str(e)}")
        raise

if __name__ == "__main__":
    # 创建并设置事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # 启动调度器
    loop.run_until_complete(init_scheduler())
    
    # 直接启动Robyn实例，让Robyn框架接管应用生命周期
    app.start(port=8080, host="0.0.0.0")
