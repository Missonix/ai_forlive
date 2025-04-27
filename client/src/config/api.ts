import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // 处理未授权的情况
      localStorage.removeItem('userInfo')
      localStorage.removeItem('accessToken')
      window.location.href = '/user'
    } else if (error.response?.status === 404) {
      // 处理资源不存在的情况
      console.error('请求的资源不存在')
    } else if (error.response?.status === 500) {
      // 处理服务器错误
      console.error('服务器错误，请稍后重试')
    }
    return Promise.reject(error)
  }
)

// 添加请求重试机制
api.interceptors.response.use(undefined, async (err) => {
  const { config } = err
  if (!config || !config.retry) {
    return Promise.reject(err)
  }
  config.retryCount = config.retryCount || 0
  if (config.retryCount >= config.retry) {
    return Promise.reject(err)
  }
  config.retryCount += 1
  const backoff = new Promise((resolve) => {
    setTimeout(() => {
      resolve(null)
    }, config.retryDelay || 1000)
  })
  await backoff
  return api(config)
})

export default api 