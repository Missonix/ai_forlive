import requests
import json
import logging
import asyncio
from sqlalchemy import select

logger = logging.getLogger(__name__)

def query_video_list(cookie, country, startDate, endDate, cateIds):
    """
    向kalodata请求视频列表数据
    
    参数:
        cookie (str): 用户的Cookie值
        country (str): 国家代码，例如'MY'
        startDate (str): 开始日期，格式为YYYY-MM-DD
        endDate (str): 结束日期，格式为YYYY-MM-DD
        cateIds (list): 分类ID列表，例如["961032"]
    
    返回:
        dict: API响应的JSON数据
    """
    url = "https://www.kalodata.com/video/queryList"
    
    # 确保cateIds是列表格式
    if isinstance(cateIds, str):
        try:
            import json
            cateIds = json.loads(cateIds)
        except:
            cateIds = [cateIds]
    elif not isinstance(cateIds, list):
        cateIds = [str(cateIds)]

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "country": country,
        "currency": "CNY",
        "language": "zh-CN",
        "Origin": "https://www.kalodata.com",
        "Referer": "https://www.kalodata.com/video",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    
    data = {
        "country": country,
        "startDate": startDate, #  "2025-05-07",
        "endDate": endDate, # "2025-05-13",
        "cateIds": cateIds,
        "pageNo": 1,
        "pageSize": 10,
        "sort": [
            {
                "field": "revenue",
                "type": "DESC"
            }
        ],
        "video.filter.video_type": "WithProduct",
        "video.filter.ad.daily_roas": ""
    }
    
    logger.info(f"准备发送请求到 {url}")
    logger.info(f"请求头: {headers}")
    logger.info(f"请求数据: {data}")
    
    try:
        # 使用session来处理请求，这样可以更好地处理cookie
        with requests.Session() as session:
            response = session.post(url, headers=headers, json=data, timeout=30)
            logger.info(f"API响应状态码: {response.status_code}")
            logger.info(f"API响应内容: {response.text[:1000]}...")  # 只记录前1000个字符
            
            response.raise_for_status()  # 如果响应状态码不是200，将引发异常
            
            response_data = response.json()
            if not response_data.get('success'):
                logger.error(f"API返回错误: {response_data.get('message', '未知错误')}")
            return response_data
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"解析响应JSON失败: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        return None

def get_video_detail(cookie, country, video_id, startDate, endDate):
    """
    获取视频的详细信息
    
    参数:
        cookie (str): 用户的Cookie值
        country (str): 国家代码
        video_id (str): 视频ID
        startDate (str): 开始日期
        endDate (str): 结束日期
    
    返回:
        dict: 包含视频详情的响应数据
    """
    url = "https://www.kalodata.com/video/detail"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "country": country,
        "Origin": "https://www.kalodata.com",
        "Referer": "https://www.kalodata.com/video",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    
    data = {
        "id": video_id,
        "startDate": startDate,
        "endDate": endDate,
        "authority": True
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        
        # 检查是否存在API调用次数限制错误
        if not response_data.get('success') and response_data.get('message'):
            error_message = response_data.get('message')
            if isinstance(error_message, str) and "Today's detail times has been used up" in error_message:
                logger.warning(f"获取视频详情失败: video_id={video_id}, response={response_data}")
                return {"success": False, "message": error_message, "data": None, "is_limit_error": True, "cause": "DETAIL.ACCESS_TIMES"}
        
        return response_data
    except requests.exceptions.RequestException as e:
        logger.error(f"请求视频详情出错: {e}")
        return None

def enrich_video_data(cookie, country, startDate, endDate, cateIds, video_ids):
    """
    获取视频的产品ID信息
    
    参数:
        cookie (str): 用户的Cookie值
        country (str): 国家代码
        startDate (str): 开始日期
        endDate (str): 结束日期
        cateIds (list): 分类ID列表
        video_ids (list): 视频ID列表
    
    返回:
        dict: 包含产品ID的响应数据
    """
    url = "https://www.kalodata.com/video/enrich"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "country": country,
        "Origin": "https://www.kalodata.com",
        "Referer": "https://www.kalodata.com/video",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    
    data = {
        "ids": video_ids,
        "country": country,
        "startDate": startDate,
        "endDate": endDate,
        "cateIds": cateIds
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求product_id出错: {e}")
        return None

def get_product_detail(cookie, country, product_id, startDate, endDate):
    """
    获取产品详细信息
    
    参数:
        cookie (str): 用户的Cookie值
        country (str): 国家代码
        product_id (str): 产品ID
        startDate (str): 开始日期
        endDate (str): 结束日期
    
    返回:
        dict: 包含产品详情的响应数据
    """
    url = "https://www.kalodata.com/product/detail"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "country": country,
        "Origin": "https://www.kalodata.com",
        "Referer": "https://www.kalodata.com/video",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    
    data = {
        "id": product_id,
        "startDate": startDate,
        "endDate": endDate,
        "authority": True
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        
        # 检查是否存在API调用次数限制错误
        if not response_data.get('success') and response_data.get('message'):
            error_message = response_data.get('message')
            if isinstance(error_message, str) and "Today's detail times has been used up" in error_message:
                logger.warning(f"获取产品详情失败: product_id={product_id}, response={response_data}")
                return {"success": False, "message": error_message, "data": None, "is_limit_error": True, "cause": "DETAIL.ACCESS_TIMES"}
            
        return response_data
    except requests.exceptions.RequestException as e:
        logger.error(f"请求产品详情出错: {e}")
        return None

# 添加获取类目名称的函数
async def get_category3_label(db, category_value):
    """
    从数据库中获取三级类目的标签名称
    
    参数：
        db: 数据库会话
        category_value: 三级类目ID
        
    返回：
        str: 三级类目的标签名称，如果未找到则返回类目ID
    """
    from apps.search_video.models import CategoryLevel3
    
    try:
        # 查询指定value的三级类目
        query = select(CategoryLevel3).where(CategoryLevel3.value == category_value)
        result = await db.execute(query)
        category = result.scalar_one_or_none()
        
        if category:
            return category.label
        return category_value  # 如果未找到，返回原始ID值
    except Exception as e:
        logger.error(f"获取三级类目标签失败: {str(e)}")
        return category_value  # 出错时返回原始ID值

def get_complete_video_data(cookie, country, startDate, endDate, cateIds):
    """
    获取完整的视频数据，包括产品详情和URL
    
    参数:
        cookie (str): 用户的Cookie值
        country (str): 国家代码
        startDate (str): 开始日期
        endDate (str): 结束日期
        cateIds (list): 分类ID列表，例如["961032"]
    
    返回:
        list: 包含全部信息的数据列表
    """
    logger.info(f"开始获取视频列表数据: country={country}, startDate={startDate}, endDate={endDate}, cateIds={cateIds}")
    
    # 1. 获取视频列表数据
    video_data = query_video_list(cookie, country, startDate, endDate, cateIds)
    if not video_data:
        logger.error("获取视频列表失败: API返回为空")
        return []
    if not video_data.get('success'):
        logger.error(f"获取视频列表失败: {video_data.get('message', '未知错误')}")
        return []
    
    logger.info(f"成功获取视频列表数据: {video_data}")
    
    # 2. 提取视频ID列表
    videos = video_data.get('data', [])
    video_ids = [video.get('id') for video in videos if 'id' in video]
    
    if not video_ids:
        logger.error("没有找到有效的视频ID")
        return []
    
    logger.info(f"提取到的视频ID列表: {video_ids}")
    
    # 3. 获取每个视频的详细信息
    video_details = {}
    is_detail_api_limited = False
    
    for video_id in video_ids:
        try:
            detail = get_video_detail(cookie, country, video_id, startDate, endDate)
            if detail and detail.get('is_limit_error'):
                logger.warning("视频详情API调用受限")
                is_detail_api_limited = True
                break
            elif detail and detail.get('success') and 'data' in detail:
                video_details[video_id] = detail.get('data', {})
                logger.info(f"成功获取视频详情: video_id={video_id}")
            else:
                logger.warning(f"获取视频详情失败: video_id={video_id}, response={detail}")
        except Exception as e:
            logger.error(f"获取视频详情异常: video_id={video_id}, error={str(e)}")
    
    # 4. 获取产品ID
    try:
        product_id_data = enrich_video_data(cookie, country, startDate, endDate, cateIds, video_ids)
        logger.info(f"产品ID数据获取结果: {product_id_data}")
    except Exception as e:
        logger.error(f"获取产品ID数据异常: {str(e)}")
        return []
    
    if not product_id_data or not product_id_data.get('success'):
        logger.error("获取产品ID失败")
        return []
    
    # 创建视频ID到产品ID的映射
    product_map = {item.get('id'): {'product_id': item.get('product_id')} 
                  for item in product_id_data.get('data', []) if 'id' in item and 'product_id' in item}
    
    logger.info(f"视频ID到产品ID的映射: {product_map}")
    
    # 5. 获取每个产品的详细信息
    unique_product_ids = list(set(item.get('product_id') for item in product_id_data.get('data', []) 
                             if 'product_id' in item))
    
    product_details = {}
    is_product_api_limited = False
    
    for product_id in unique_product_ids:
        try:
            detail = get_product_detail(cookie, country, product_id, startDate, endDate)
            if detail and detail.get('is_limit_error'):
                logger.warning("产品详情API调用受限")
                is_product_api_limited = True
                break
            elif detail and detail.get('success') and 'data' in detail:
                product_details[product_id] = detail.get('data', {})
                logger.info(f"成功获取产品详情: product_id={product_id}")
            else:
                logger.warning(f"获取产品详情失败: product_id={product_id}, response={detail}")
        except Exception as e:
            logger.error(f"获取产品详情异常: product_id={product_id}, error={str(e)}")
    
    # 6. 构建完整数据，传入API限制标志
    complete_data = build_complete_data(
        video_data, 
        product_map, 
        product_details, 
        video_details, 
        country, 
        is_detail_api_limited or is_product_api_limited,
        cateIds
    )
    
    logger.info(f"构建完成的数据条数: {len(complete_data)}")
    
    return complete_data

def build_complete_data(video_data, product_map, product_details, video_details, country, is_api_limited=False, cateIds=None):
    """
    构建完整的视频和产品信息
    
    参数:
        video_data (dict): 原始视频数据
        product_map (dict): 视频ID到产品ID的映射
        product_details (dict): 产品ID到产品详情的映射
        video_details (dict): 视频ID到视频详情的映射
        country (str): 国家代码
        is_api_limited (bool): API是否受到调用次数限制
        cateIds (list): 类目ID列表
    
    返回:
        list: 包含全部信息的数据列表
    """
    if not video_data or not video_data.get('success'):
        return []
    
    videos = video_data.get('data', [])
    result = []
    
    # 记录当前请求的类目ID，用于后续填充
    current_category_id = cateIds[0] if cateIds and isinstance(cateIds, list) and len(cateIds) > 0 else ""
    
    for video in videos:
        video_id = video.get('id')
        product_id = product_map.get(video_id, {}).get('product_id', '')
        
        # 构建新的字典，包含所有原始字段
        enriched_video = video.copy()
        
        enriched_video['region'] = country

        # 添加新字段
        enriched_video['video_url'] = f"https://live.kalowave.cn/video/{video_id}.mp4"
        enriched_video['tiktok_url'] = f"https://www.tiktok.com/@{video_details.get(video_id, {}).get('handle', '')}/video/{video_id}"
        enriched_video['product_url'] = f"https://shop.tiktok.com/view/product/{product_id}?region={country}&locale=zh-CN"
        
        # 添加产品标题和类目
        if not is_api_limited and product_id and product_id in product_details:
            product_detail = product_details[product_id]
            enriched_video['product_title'] = product_detail.get('product_title', '')
            
            # 添加产品类目信息
            enriched_video['product_pri_cate_id'] = product_detail.get('pri_cate_id', '')
            enriched_video['product_sec_cate_id'] = product_detail.get('sec_cate_id', '')
            enriched_video['product_ter_cate_id'] = product_detail.get('ter_cate_id', '')
            enriched_video['product_price'] = product_detail.get('min_original_price', '')
        else:
            # API受限或无产品详情时使用默认值
            enriched_video['product_title'] = "unknown" if is_api_limited else ""
            enriched_video['product_price'] = "unknown" if is_api_limited else ""
            
            # 如果API受限，但我们有类目ID，则使用当前请求的类目ID
            if is_api_limited and current_category_id:
                enriched_video['product_pri_cate_id'] = ""
                enriched_video['product_sec_cate_id'] = ""
                enriched_video['product_ter_cate_id'] = current_category_id
            else:
                enriched_video['product_pri_cate_id'] = ""
                enriched_video['product_sec_cate_id'] = ""
                enriched_video['product_ter_cate_id'] = ""

        # 添加视频详情字段
        if not is_api_limited and video_id in video_details:
            enriched_video['hashtags'] = video_details[video_id].get('hashtags', [])
            enriched_video['follower_count'] = video_details[video_id].get('follower_count', '')
            enriched_video['handle'] = video_details[video_id].get('handle', '')
        else:
            enriched_video['hashtags'] = []
            enriched_video['follower_count'] = "unknown" if is_api_limited else ""
            enriched_video['handle'] = "unknown" if is_api_limited else ""
            enriched_video['username'] = "unknown" if is_api_limited else ""
        
        result.append(enriched_video)
    
    return result

def parse_video_data(response_data):
    """
    解析视频数据响应，提取并打印指定字段
    
    参数:
        response_data (dict): API返回的响应数据
    """
    if not response_data or not isinstance(response_data, list):
        print("响应数据无效")
        return
    
    print(f"共获取到 {len(response_data)} 条视频数据")
    print("-" * 80)
    
    for index, video in enumerate(response_data, 1):
        print(f"视频 {index}:")
        print(f"ID: {video.get('id', '未知')}")
        print(f"region: {video.get('region', '未知')}")
        print(f"是否广告: {'是' if video.get('ad') == 1 else '否'}")
        print(f"描述: {video.get('description', '无')}")
        print(f"广告状态: {'是' if video.get('ad') == 1 else '否'}")
        print(f"每千次播放收入(GPM): {video.get('gpm', '未知')}")
        print(f"广告单次获客成本(CPA): {video.get('ad_cpa', '未知')}")
        print(f"广告观看比例: {video.get('ad_view_ratio', '未知')}")
        print(f"视频时长: {video.get('duration', '未知')}")
        print(f"收入: {video.get('revenue', '未知')}")
        print(f"销售量: {video.get('sale', '未知')}")
        print(f"广告投资回报率(ROAS): {video.get('ad2Roas', '未知')}")
        print(f"广告成本: {video.get('ad2Cost', '未知')}")
        print(f"观看量: {video.get('views', '未知')}")
        print(f"产品标题: {video.get('product_title', '未知')}")
        print(f"产品一级类目: {video.get('product_pri_cate_id', '未知')}")
        print(f"产品二级类目: {video.get('product_sec_cate_id', '未知')}")
        print(f"产品三级类目: {video.get('product_ter_cate_id', '未知')}")
        print(f"产品价格: {video.get('product_price', '未知')}")
        print(f"视频URL: {video.get('video_url', '未知')}")
        print(f"TikTok URL: {video.get('tiktok_url', '未知')}")
        print(f"产品URL: {video.get('product_url', '未知')}")
        print(f"用户名: {video.get('handle', '未知')}")
        print(f"粉丝数: {video.get('follower_count', '未知')}")
        print(f"标签: {', '.join(video.get('hashtags', []))}")
        print("-" * 80)

# 使用示例
if __name__ == "__main__":
    # 请替换为实际的cookie和country值
    test_cookie = "page_session=f5c23109-f00a-44f9-baef-acd44cf30920; Hm_lvt_8aa1693861618ac63989ae373e684811=1746503923; HMACCOUNT=F92EEE8A7B2DF701; AGL_USER_ID=ba4cd824-1ae6-4671-b676-5a1494f65c26; appVersion=2.0; _gcl_aw=GCL.1746503923.Cj0KCQjww-HABhCGARIsALLO6XzvZy4WhVjIsxtBnH8vUxT9VXFKLuerVe-h-HFhq876EPqe8PDniVUaArcDEALw_wcB; _gcl_gs=2.1.k1$i1746503921$u134601579; _ga=GA1.1.1966752816.1746503923; _gcl_au=1.1.2054049858.1746503923; _bl_uid=U2mvXawtbLLz8pcOvcnq17d99nCj; _fbp=fb.1.1746503923927.913525883506004015; deviceId=b50fad717579643e3a95ec8e1975f15c; _tt_enable_cookie=1; _ttp=01JTHVXYBXVSBQRXKK8KV414S8_.tt.1; deviceType=pc; SESSION=ZmY0MGIwMGYtZGUzNi00NTEwLTk1NWMtN2QxZjJkZThmNGM2; _c_WBKFRo=gquS3n92AYQsWcEzQZoRsAbYQL1UP2OUCwMy8r8r; _nb_ioWEgULi=; _clck=d2mt7j%7C2%7Cfvw%7C0%7C1952; Hm_lpvt_8aa1693861618ac63989ae373e684811=1747201992; _uetsid=31c95ed02eed11f0afe4c525af41f480; _uetvid=66df53d02a2e11f08bff35fb2bfbc29d; _ga_Q21FRKKG88=GS2.1.s1747201514$o26$g1$t1747201992$j0$l0$h0; ttcsid=1747201525197::7R-_E-xd1CHj5Q5BS5YJ.15.1747201992972; ttcsid_CM9SHDBC77U4KJBR96OG=1747201525197::0ofmrgYTzF5f9H82R1iW.15.1747201993332"
    test_country = "MY"
    test_startDate = "2025-05-07"
    test_endDate = "2025-05-13"
    test_cateIds = ["602165"]  # 添加分类ID参数
    
    

    # 获取完整的视频数据
    complete_data = get_complete_video_data(test_cookie, test_country, test_startDate, test_endDate, test_cateIds)
    
    # 解析并打印结果中的关键字段
    parse_video_data(complete_data)
    
    # 示例TikTok视频URL
    # https://www.tiktok.com/@hlovatee/video/7452904748358896914




