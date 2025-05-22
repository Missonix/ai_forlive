<template>
  <div class="max-w-md mx-auto p-4 pb-16">
    <!-- 头部 -->
    <header class="py-4">
      <div class="flex items-center mb-4">
        <router-link to="/" class="text-indigo-600 hover:text-indigo-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-xl font-bold text-center flex-1 pr-6">对标视频AI搜索与推荐</h1>
        <button @click="showHistory = true" class="text-indigo-600 hover:text-indigo-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
      </div>
    </header>

    <!-- 主要内容区 -->
    <main class="space-y-6">
      <!-- 输入表单部分 -->
      <div class="bg-white rounded-lg p-4 shadow">
        <div class="space-y-4">
          <!-- 商品名称输入 -->
          <div>
            <label for="product-name" class="block text-sm font-medium text-gray-700 mb-1">商品名称</label>
            <input
              v-model="productName"
              id="product-name"
              type="text"
              class="w-full p-3 border rounded-lg"
              placeholder="请输入商品名称"
            />
          </div>

          <!-- 类目选择 - 一级类目 -->
          <div>
            <label for="category-level1" class="block text-sm font-medium text-gray-700 mb-1">一级类目</label>
            <select
              v-model="selectedLevel1"
              id="category-level1"
              class="w-full p-3 border rounded-lg bg-white"
              @change="handleLevel1Change"
            >
              <option value="" disabled>请选择一级类目</option>
              <option v-for="category in level1Categories" :key="category.id" :value="category.value">
                {{ category.label }}
              </option>
            </select>
          </div>

          <!-- 类目选择 - 二级类目 -->
          <div>
            <label for="category-level2" class="block text-sm font-medium text-gray-700 mb-1">二级类目</label>
            <select
              v-model="selectedLevel2"
              id="category-level2"
              class="w-full p-3 border rounded-lg bg-white"
              :disabled="!selectedLevel1"
              @change="handleLevel2Change"
            >
              <option value="" disabled>请选择二级类目</option>
              <option v-for="category in level2Categories" :key="category.id" :value="category.value">
                {{ category.label }}
              </option>
            </select>
          </div>

          <!-- 类目选择 - 三级类目 -->
          <div>
            <label for="category-level3" class="block text-sm font-medium text-gray-700 mb-1">三级类目</label>
            <select
              v-model="selectedLevel3"
              id="category-level3"
              class="w-full p-3 border rounded-lg bg-white"
              :disabled="!selectedLevel2"
            >
              <option value="" disabled>请选择三级类目</option>
              <option v-for="category in level3Categories" :key="category.id" :value="category.value" :data-label="category.label">
                {{ category.label }}
              </option>
            </select>
          </div>

          <!-- 国家选择 -->
          <div>
            <label for="country" class="block text-sm font-medium text-gray-700 mb-1">国家</label>
            <select
              v-model="selectedCountry"
              id="country"
              class="w-full p-3 border rounded-lg bg-white"
            >
              <option value="" disabled>请选择国家</option>
              <option v-for="country in Object.keys(countries)" :key="country" :value="country">
                {{ country }}
              </option>
            </select>
          </div>

          <button
            @click="startGenerate"
            :disabled="loading || !isFormValid"
            class="w-full mt-4 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {{ loading ? '生成中...' : '开始生成' }}
          </button>
          <p class="text-sm text-gray-500 text-center mt-2">
            AI生成拍摄建议，并为您推荐近期爆款视频
          </p>
        </div>
      </div>

      <!-- 生成结果部分 -->
      <div v-if="searchResult" class="bg-white rounded-lg p-4 shadow space-y-6">
        <h2 class="font-bold text-lg border-b pb-2">拍摄建议</h2>
        
        <!-- 拍摄建议信息 -->
        <div class="space-y-4">
          <div v-if="searchResult.scenes" class="space-y-2">
            <div class="font-medium">拍摄场景建议:</div>
            <div class="text-gray-600 text-sm whitespace-pre-line">{{ searchResult.scenes }}</div>
          </div>

          <div v-if="searchResult.style" class="space-y-2">
            <div class="font-medium">拍摄风格建议:</div>
            <div class="text-gray-600 text-sm whitespace-pre-line">{{ searchResult.style }}</div>
          </div>

          <div v-if="searchResult.lens_usage" class="space-y-2">
            <div class="font-medium">镜头运用建议:</div>
            <div class="text-gray-600 text-sm whitespace-pre-line">{{ searchResult.lens_usage }}</div>
          </div>

          <div v-if="searchResult.actor_selection" class="space-y-2">
            <div class="font-medium">演员选择建议:</div>
            <div class="text-gray-600 text-sm whitespace-pre-line">{{ searchResult.actor_selection }}</div>
          </div>

          <div v-if="searchResult.prop_matching" class="space-y-2">
            <div class="font-medium">道具搭配建议:</div>
            <div class="text-gray-600 text-sm whitespace-pre-line">{{ searchResult.prop_matching }}</div>
          </div>
        </div>

        <!-- 推荐视频列表 -->
        <div v-if="videoItems.length > 0" class="mt-8">
          <h2 class="font-bold text-lg border-b pb-2 mb-4">推荐视频</h2>
          <div class="space-y-4">
            <div 
              v-for="(item, index) in videoItems" 
              :key="index" 
              class="bg-gray-50 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
              @click="showVideoDetail(item)"
            >
              <div class="text-sm font-medium mb-2 line-clamp-2">{{ item.video_name }}</div>
              <div class="flex justify-between items-start mb-2">
                <div class="text-xs text-gray-500">
                  <div>用户: {{ item.username }}</div>
                  <div>粉丝: {{ item.follower_count }}</div>
                </div>
                <div class="text-xs text-gray-500">
                  <div>时长: {{ item.duration }}</div>
                  <div>观看量: {{ item.views }}</div>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-2 mb-2">
                <div class="text-xs">
                  <div class="text-gray-500">近7天GMV:</div>
                  <div class="font-medium">{{ item.revenue }}</div>
                </div>
                <div class="text-xs">
                  <div class="text-gray-500">近7天销量:</div>
                  <div class="font-medium">{{ item.sales }}</div>
                </div>
                <div class="text-xs">
                  <div class="text-gray-500">是否投广告:</div>
                  <div class="font-medium">{{ item.has_ad ? '是' : '否' }}</div>
                </div>
              </div>
              <div class="flex justify-between mt-2">
                <a 
                  :href="item.tiktok_url" 
                  target="_blank" 
                  class="text-indigo-600 text-xs hover:underline"
                  @click.stop
                >
                  查看原视频
                </a>
                <a 
                  :href="item.product_url" 
                  target="_blank" 
                  class="text-indigo-600 text-xs hover:underline"
                  @click.stop
                >
                  查看商品
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 历史报告弹窗 -->
    <div v-if="showHistory" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg w-full max-w-md max-h-[80vh] overflow-hidden">
        <div class="p-4 border-b flex justify-between items-center">
          <h2 class="text-lg font-bold">历史生成记录</h2>
          <button @click="showHistory = false" class="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-4 overflow-y-auto max-h-[calc(80vh-4rem)]">
          <div class="text-center py-4 text-gray-500">
            功能建设中...
          </div>
        </div>
      </div>
    </div>

    <!-- 视频详情模态框 -->
    <div v-if="selectedVideoItem" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg w-full max-w-md max-h-[80vh] overflow-hidden">
        <div class="p-4 border-b flex justify-between items-center">
          <h2 class="text-lg font-bold truncate pr-4">视频详情</h2>
          <button @click="selectedVideoItem = null" class="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-4 overflow-y-auto max-h-[calc(80vh-4rem)]">
          <div class="space-y-4" v-if="selectedVideoItem">
            <div v-if="selectedVideoItem.video_name" class="mb-4">
              <div class="font-medium text-gray-700">视频名称:</div>
              <div class="text-gray-600 break-words">{{ selectedVideoItem.video_name }}</div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div v-if="selectedVideoItem.country" class="text-sm">
                <div class="font-medium text-gray-700">国家:</div>
                <div class="text-gray-600">{{ selectedVideoItem.country }}</div>
              </div>
              
              <div v-if="selectedVideoItem.username" class="text-sm">
                <div class="font-medium text-gray-700">用户名:</div>
                <div class="text-gray-600">{{ selectedVideoItem.username }}</div>
              </div>
              
              <div v-if="selectedVideoItem.follower_count" class="text-sm">
                <div class="font-medium text-gray-700">粉丝数:</div>
                <div class="text-gray-600">{{ selectedVideoItem.follower_count }}</div>
              </div>
              
              <div v-if="selectedVideoItem.duration" class="text-sm">
                <div class="font-medium text-gray-700">时长:</div>
                <div class="text-gray-600">{{ selectedVideoItem.duration }}</div>
              </div>
              
              <div v-if="selectedVideoItem.views" class="text-sm">
                <div class="font-medium text-gray-700">观看量:</div>
                <div class="text-gray-600">{{ selectedVideoItem.views }}</div>
              </div>
              
              <div v-if="selectedVideoItem.has_ad !== undefined" class="text-sm">
                <div class="font-medium text-gray-700">是否投放广告:</div>
                <div class="text-gray-600">{{ selectedVideoItem.has_ad ? '是' : '否' }}</div>
              </div>
            </div>
            
            <div v-if="selectedVideoItem.hashtags" class="text-sm">
              <div class="font-medium text-gray-700">标签:</div>
              <div class="flex flex-wrap gap-1 mt-1">
                <span 
                  v-for="tag in selectedVideoItem.hashtags.split(',')" 
                  :key="tag"
                  class="bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full text-xs"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div v-if="selectedVideoItem.gpm" class="text-sm">
                <div class="font-medium text-gray-700">GPM:</div>
                <div class="text-gray-600">{{ selectedVideoItem.gpm }}</div>
              </div>
              
              <div v-if="selectedVideoItem.cpm" class="text-sm">
                <div class="font-medium text-gray-700">CPM:</div>
                <div class="text-gray-600">{{ selectedVideoItem.cpm }}</div>
              </div>
              
              <div v-if="selectedVideoItem.revenue" class="text-sm">
                <div class="font-medium text-gray-700">近7天GMV:</div>
                <div class="text-gray-600">{{ selectedVideoItem.revenue }}</div>
              </div>
              
              <div v-if="selectedVideoItem.sales" class="text-sm">
                <div class="font-medium text-gray-700">近7天销量:</div>
                <div class="text-gray-600">{{ selectedVideoItem.sales }}</div>
              </div>
              
              <div v-if="selectedVideoItem.roas" class="text-sm">
                <div class="font-medium text-gray-700">ROAS:</div>
                <div class="text-gray-600">{{ selectedVideoItem.roas }}</div>
              </div>
              
              <div v-if="selectedVideoItem.ad_view_ratio" class="text-sm">
                <div class="font-medium text-gray-700">广告浏览比例:</div>
                <div class="text-gray-600">{{ selectedVideoItem.ad_view_ratio }}</div>
              </div>
              
              <div v-if="selectedVideoItem.ad2Cost" class="text-sm">
                <div class="font-medium text-gray-700">广告成本:</div>
                <div class="text-gray-600">{{ selectedVideoItem.ad2Cost }}</div>
              </div>
            </div>
            
            <div class="grid grid-cols-3 gap-4">
              <div v-if="selectedVideoItem.category1" class="text-sm">
                <div class="font-medium text-gray-700">一级类目:</div>
                <div class="text-gray-600">{{ selectedVideoItem.category1 }}</div>
              </div>
              
              <div v-if="selectedVideoItem.category2" class="text-sm">
                <div class="font-medium text-gray-700">二级类目:</div>
                <div class="text-gray-600">{{ selectedVideoItem.category2 }}</div>
              </div>
              
              <div v-if="selectedVideoItem.category3" class="text-sm">
                <div class="font-medium text-gray-700">三级类目:</div>
                <div class="text-gray-600">{{ selectedVideoItem.category3 }}</div>
              </div>
            </div>
            
            <div v-if="selectedVideoItem.product_title" class="text-sm">
              <div class="font-medium text-gray-700">商品标题:</div>
              <div class="text-gray-600">{{ selectedVideoItem.product_title }}</div>
            </div>
            
            <div v-if="selectedVideoItem.product_price" class="text-sm">
              <div class="font-medium text-gray-700">商品价格:</div>
              <div class="text-gray-600">{{ selectedVideoItem.product_price }}</div>
            </div>
            
            <div v-if="selectedVideoItem.start_date && selectedVideoItem.end_date" class="text-sm">
              <div class="font-medium text-gray-700">统计周期:</div>
              <div class="text-gray-600">{{ selectedVideoItem.start_date.split(' ')[0] }} 至 {{ selectedVideoItem.end_date.split(' ')[0] }}</div>
            </div>
            
            <div class="flex space-x-4 mt-4">
              <a 
                :href="selectedVideoItem.tiktok_url" 
                target="_blank" 
                class="bg-indigo-600 text-white px-4 py-2 rounded text-sm hover:bg-indigo-700 flex-1 text-center"
              >
                查看原视频
              </a>
              <a 
                :href="selectedVideoItem.product_url" 
                target="_blank" 
                class="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700 flex-1 text-center"
              >
                查看商品
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 免责声明 -->
    <footer class="mt-8 text-xs text-gray-400 text-center px-4">
      提示：AI生成的内容仅供参考，实际效果可能因商品、平台政策或市场变化而有所不同。
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/config/api'
import { aiProducts, type AIProduct } from '@/config/aiProducts'

interface Category {
  id: number
  label: string
  value: string
  parent_value?: string
}

interface VideoItem {
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

interface SearchResult {
  phone: string
  product_name: string
  category: string
  country: string
  scenes: string
  style: string
  lens_usage: string
  actor_selection: string
  prop_matching: string
  items: string
  created_at: string
  is_deleted: boolean
}

const router = useRouter()
const productName = ref('')
const selectedLevel1 = ref('')
const selectedLevel2 = ref('')
const selectedLevel3 = ref('')
const selectedCountry = ref('')
const loading = ref(false)
const showHistory = ref(false)
const level1Categories = ref<Category[]>([])
const level2Categories = ref<Category[]>([])
const level3Categories = ref<Category[]>([])
const searchResult = ref<SearchResult | null>(null)
const videoItems = ref<VideoItem[]>([])
const selectedVideoItem = ref<VideoItem | null>(null)

// 国家字典
const countries = {
  '美国': '美国',
  '印度尼西亚': '印度尼西亚',
  '马来西亚': '马来西亚',
  '泰国': '泰国',
  '越南': '越南',
  '菲律宾': '菲律宾',
  '英国': '英国',
  '新加坡': '新加坡',
  '墨西哥': '墨西哥'
}

// 表单验证
const isFormValid = computed(() => {
  return productName.value && selectedLevel3.value && selectedCountry.value
})

// 获取一级类目
const fetchLevel1Categories = async () => {
  try {
    const response = await api.get('search_video/category/level1')
    if (response.data.code === 200) {
      level1Categories.value = response.data.data
    } else {
      throw new Error(response.data.message || '获取一级类目失败')
    }
  } catch (error: any) {
    alert(error.response?.data?.message || '获取一级类目失败，请稍后重试')
  }
}

// 处理一级类目变化
const handleLevel1Change = async () => {
  selectedLevel2.value = ''
  selectedLevel3.value = ''
  level2Categories.value = []
  level3Categories.value = []
  
  if (!selectedLevel1.value) return
  
  try {
    const response = await api.get(`/search_video/category/level2/${selectedLevel1.value}`)
    if (response.data.code === 200) {
      level2Categories.value = response.data.data
    } else {
      throw new Error(response.data.message || '获取二级类目失败')
    }
  } catch (error: any) {
    alert(error.response?.data?.message || '获取二级类目失败，请稍后重试')
  }
}

// 处理二级类目变化
const handleLevel2Change = async () => {
  selectedLevel3.value = ''
  level3Categories.value = []
  
  if (!selectedLevel2.value) return
  
  try {
    const response = await api.get(`/search_video/category/level3/${selectedLevel2.value}`)
    if (response.data.code === 200) {
      level3Categories.value = response.data.data
    } else {
      throw new Error(response.data.message || '获取三级类目失败')
    }
  } catch (error: any) {
    alert(error.response?.data?.message || '获取三级类目失败，请稍后重试')
  }
}

// 开始生成
const startGenerate = async () => {
  // 检查是否登录
  const userInfo = localStorage.getItem('userInfo')
  if (!userInfo) {
    alert('请先登录后使用此功能')
    router.push('/user')
    return
  }

  if (!isFormValid.value) {
    alert('请填写完整的表单信息')
    return
  }

  loading.value = true
  try {
    const userData = JSON.parse(userInfo)
    // 验证用户信息格式
    if (!userData.phone || !userData.entitlements || userData.entitlements.length === 0) {
      throw new Error('用户信息不完整，请重新登录')
    }

    // 获取当前产品的ai_product_id
    const currentProduct = aiProducts.find((p: AIProduct) => p.id === 'video_search_recommendation')
    if (!currentProduct) {
      throw new Error('产品配置错误')
    }

    // 查找用户是否有该产品的权限
    const activeEntitlement = userData.entitlements.find(
      (ent: any) => ent.is_active && ent.ai_product_id === currentProduct.ai_product_id
    )
    if (!activeEntitlement) {
      throw new Error('您暂无使用此功能的权限')
    }

    // 获取选中三级类目的label
    const selectedCategory = level3Categories.value.find(cat => cat.value === selectedLevel3.value)
    if (!selectedCategory) {
      throw new Error('类目信息错误')
    }

    const response = await api.post('/search_video', {
      product_name: productName.value,
      category: selectedCategory.label,
      country: selectedCountry.value,
      phone: userData.phone,
      ai_product_id: currentProduct.ai_product_id
    })

    if (response.data.code === 200) {
      if (!response.data.data || !response.data.data.result) {
        throw new Error('响应数据格式错误')
      }
      
      searchResult.value = response.data.data.result
      
      // 解析视频列表
      if (searchResult.value && searchResult.value.items) {
        try {
          videoItems.value = JSON.parse(searchResult.value.items)
        } catch (err) {
          console.error('解析视频列表失败', err)
          videoItems.value = []
        }
      }
      
      // 更新用户信息中的daily_remaining
      const updatedUserInfo = JSON.parse(userInfo)
      const entitlementIndex = updatedUserInfo.entitlements.findIndex(
        (ent: any) => ent.entitlement_id === activeEntitlement.entitlement_id
      )
      if (entitlementIndex !== -1) {
        updatedUserInfo.entitlements[entitlementIndex].daily_remaining = 
          response.data.data.daily_remaining
        localStorage.setItem('userInfo', JSON.stringify(updatedUserInfo))
      }
    } else if (response.data.code === 403) {
      // 处理权限不足的情况
      if (response.data.message === '暂无权益') {
        alert('您暂无使用此功能的权限，请联系管理员')
      } else if (response.data.message === '使用额度不足') {
        alert('今日使用额度已用完，请明天再试')
      } else {
        alert(response.data.message || '权限不足')
      }
    } else {
      throw new Error(response.data.message || '生成失败')
    }
  } catch (error: any) {
    if (error.message === '用户信息不完整，请重新登录' || 
        error.message === '您暂无使用此功能的权限' ||
        error.message === '产品配置错误' ||
        error.message === '响应数据格式错误' ||
        error.message === '类目信息错误') {
      alert(error.message)
      if (error.message === '用户信息不完整，请重新登录') {
        router.push('/user')
      }
    } else if (error.message.includes('timeout')) {
      alert('请求超时，请稍后重试')
    } else {
      alert(error.response?.data?.message || '生成失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

// 显示视频详情
const showVideoDetail = (item: VideoItem) => {
  selectedVideoItem.value = item
}

// 页面加载完成后获取一级类目
onMounted(() => {
  fetchLevel1Categories()
})
</script>

<style scoped>
.pb-16 {
  padding-bottom: 4rem;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 