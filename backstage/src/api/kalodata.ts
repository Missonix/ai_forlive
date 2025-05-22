import axios from 'axios'

const BASE_URL = '/api'

export interface KalodataItem {
  id: number
  country: string
  has_ad: boolean
  video_name: string
  gpm: string
  cpm: string
  ad_view_ratio: string
  duration: string
  revenue: string
  sales: string
  roas: string
  ad2Cost: string
  views: string
  product_title: string
  category1: string
  category2: string
  category3: string
  product_price: string
  video_url: string
  tiktok_url: string
  product_url: string
  product_image: string
  username: string
  follower_count: string
  hashtags: string
  start_date: string
  end_date: string
  created_at: string
}

export interface FilterParams {
  country: string
  page?: number
  page_size?: number
  category?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface CategoryItem {
  id: number
  label: string
  value: string
  parent_value?: string
}

// 获取kalodata统计数据接口响应类型
export interface KalodataStatistics {
  total_count: number
  latest_date: string
  country: string
  category: string
}

// 获取最新数据接口参数
export interface FetchKalodataParams {
  cookie: string
  country: string
  start_date: string
  end_date: string
  cate_ids: string[]
}

// 批量获取一级类目数据的接口参数
export interface FetchByCategory1Params {
  country: string
  category1: string
  cookie: string
}

// 批量获取一级类目数据的响应类型
export interface FetchByCategory1Response {
  category1_value: string
  country: string
  total_category2: number
  total_category3: number
  start_date: string
  end_date: string
  success_count: number
  skip_count: number
  failed_categories_count: number
  category2_info: Array<{
    value: string
    label: string
  }>
  category3_info: Array<{
    category2_value: string
    category2_label: string
    category3_list: Array<{
      value: string
      label: string
    }>
    count: number
  }>
  failed_categories: Array<{
    category3_value: string
    category3_label: string
    error: string
  }>
  processed_categories: Array<{
    category3_value: string
    category3_label: string
    success_count: number
    skip_count: number
  }>
}

export const kalodataApi = {
  // 根据过滤条件获取kalodata数据
  getKalodataByFilters(params: FilterParams) {
    return axios.post<{ code: number; message: string; data: PaginatedResponse<KalodataItem> }>(
      `${BASE_URL}/search_video/kalodata/data/filters`,
      params,
    )
  },

  // 获取类目数据统计信息
  getKalodataStatistics(country: string, category: string) {
    return axios.post<{ code: number; message: string; data: KalodataStatistics }>(
      `${BASE_URL}/search_video/kalodata/statistics`,
      {
        country,
        category,
      },
    )
  },

  // 获取并存储最新的kalodata数据
  fetchAndStoreKalodata(params: FetchKalodataParams) {
    return axios.post<{ code: number; message: string; data: Record<string, any> }>(
      `${BASE_URL}/search_video/kalodata/fetch_and_store`,
      params,
    )
  },

  // 根据一级类目批量获取并存储kalodata数据
  fetchByCategoryLevel1(params: FetchByCategory1Params) {
    return axios.post<{ code: number; message: string; data: FetchByCategory1Response }>(
      `${BASE_URL}/search_video/kalodata/statistics/by_category`,
      params,
    )
  },

  // 获取所有一级类目
  getLevel1Categories() {
    return axios.get<{ code: number; message: string; data: CategoryItem[] }>(
      `${BASE_URL}/search_video/category/level1`,
    )
  },

  // 获取指定一级类目下的所有二级类目
  getLevel2Categories(level1Id: string) {
    return axios.get<{ code: number; message: string; data: CategoryItem[] }>(
      `${BASE_URL}/search_video/category/level2/${level1Id}`,
    )
  },

  // 获取指定二级类目下的所有三级类目
  getLevel3Categories(level2Id: string) {
    return axios.get<{ code: number; message: string; data: CategoryItem[] }>(
      `${BASE_URL}/search_video/category/level3/${level2Id}`,
    )
  },
}
