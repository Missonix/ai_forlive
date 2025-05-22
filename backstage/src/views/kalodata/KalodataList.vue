<template>
  <div class="kalodata-container">
    <el-card class="kalodata-card">
      <template #header>
        <div class="card-header">
          <div class="title-area">
            <h2>Kalodata 数据管理</h2>
            <el-button
              type="primary"
              size="small"
              @click="$router.push('/category-manage')"
              style="margin-left: 15px"
            >
              <el-icon><Files /></el-icon> 类目管理
            </el-button>
          </div>
          <div class="filter-container">
            <div class="country-filter">
              <span class="filter-label">选择国家:</span>
              <el-select
                v-model="selectedCountry"
                placeholder="请选择国家"
                @change="handleCountryChange"
                style="width: 160px"
                size="large"
              >
                <el-option
                  v-for="(code, name) in countryOptions"
                  :key="code"
                  :label="name"
                  :value="code"
                />
              </el-select>
            </div>
            <div class="category-filter">
              <span class="filter-label">选择类目:</span>
              <el-cascader
                v-model="selectedCategory"
                :options="level1Categories"
                :props="categoryProps"
                placeholder="请选择类目"
                style="width: 420px"
                @change="handleCategoryChange"
                clearable
                size="large"
              />
              <el-button
                type="primary"
                size="large"
                @click="handleClearCategory"
                style="margin-left: 10px"
              >
                <el-icon><Delete /></el-icon> 清空类目
              </el-button>
            </div>
          </div>
        </div>
      </template>

      <!-- 数据表格 -->
      <el-table
        :data="kalodataList"
        style="width: 100%"
        v-loading="loading"
        border
        stripe
        :header-cell-style="{ background: '#f0f6fc', color: '#333', fontWeight: 'bold' }"
        :cell-style="{ padding: '8px 0' }"
        highlight-current-row
      >
        <el-table-column prop="id" label="ID" width="70" align="center" />
        <el-table-column prop="country" label="国家" width="80" align="center" />
        <el-table-column prop="has_ad" label="是否有广告" width="110" align="center">
          <template #default="{ row }">
            <el-tag :type="row.has_ad ? 'success' : 'info'" effect="dark" size="small">
              {{ row.has_ad ? '有' : '无' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="video_name" label="视频名称" min-width="250" show-overflow-tooltip />
        <el-table-column prop="gpm" label="GPM" width="100" align="right" />
        <el-table-column prop="cpm" label="CPM" width="100" align="right" />
        <el-table-column prop="ad_view_ratio" label="广告观看率" width="120" align="right" />
        <el-table-column prop="duration" label="时长" width="80" align="center" />
        <el-table-column prop="revenue" label="收入" width="100" align="right" />
        <el-table-column prop="sales" label="销量" width="80" align="right">
          <template #default="{ row }">
            <span class="highlight-number">{{ row.sales }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="roas" label="ROAS" width="100" align="right" />
        <el-table-column prop="views" label="观看量" width="100" align="right">
          <template #default="{ row }">
            <span class="highlight-number">{{ row.views }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="follower_count" label="粉丝数" width="100" align="right" />
        <el-table-column
          prop="product_title"
          label="产品标题"
          min-width="250"
          show-overflow-tooltip
        />
        <el-table-column prop="category1" label="一级分类" width="120" />
        <el-table-column prop="category2" label="二级分类" width="140" />
        <el-table-column prop="category3" label="三级分类" width="150" />
        <el-table-column prop="product_price" label="产品价格" width="100" align="right" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                type="primary"
                size="small"
                @click="previewVideo(row)"
                :disabled="!row.video_url"
                link
                title="预览视频"
              >
                <el-icon><VideoPlay /></el-icon>
              </el-button>
              <el-button
                type="primary"
                size="small"
                @click="openTiktokUrl(row.tiktok_url)"
                :disabled="!row.tiktok_url"
                link
                title="打开TikTok"
              >
                <el-icon><Link /></el-icon>
              </el-button>
              <el-button
                type="success"
                size="small"
                @click="openProductUrl(row.product_url)"
                :disabled="!row.product_url"
                link
                title="查看商品"
              >
                <el-icon><ShoppingCart /></el-icon>
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          background
        />
      </div>
    </el-card>

    <!-- 视频预览对话框 -->
    <el-dialog
      v-model="videoDialogVisible"
      title="视频预览"
      width="700px"
      center
      destroy-on-close
      custom-class="video-dialog"
    >
      <div class="video-container">
        <video
          v-if="currentVideo"
          ref="videoPlayer"
          controls
          autoplay
          width="100%"
          :src="currentVideo"
          style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15)"
        ></video>
      </div>
      <div class="video-info" v-if="selectedVideoData">
        <h3>{{ selectedVideoData.video_name }}</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label"
              ><el-icon><User /></el-icon> 用户：</span
            >
            <span class="info-value"
              >{{ selectedVideoData.username }} ({{ selectedVideoData.follower_count }} 粉丝)</span
            >
          </div>
          <div class="info-item">
            <span class="info-label"
              ><el-icon><ShoppingCart /></el-icon> 产品：</span
            >
            <span class="info-value">{{ selectedVideoData.product_title }}</span>
          </div>
          <div class="info-item">
            <span class="info-label"
              ><el-icon><Money /></el-icon> 价格：</span
            >
            <span class="info-value">{{ selectedVideoData.product_price }}</span>
          </div>
          <div class="info-item">
            <span class="info-label"
              ><el-icon><DataAnalysis /></el-icon> 数据：</span
            >
            <span class="info-value">
              销量 {{ selectedVideoData.sales }}，观看 {{ selectedVideoData.views }}，ROAS
              {{ selectedVideoData.roas }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label"
              ><el-icon><Histogram /></el-icon> GPM/CPM：</span
            >
            <span class="info-value">
              GPM {{ selectedVideoData.gpm }}，CPM {{ selectedVideoData.cpm }}
            </span>
          </div>
        </div>
        <div class="video-actions">
          <el-button
            type="primary"
            @click="openTiktokUrl(selectedVideoData.tiktok_url)"
            v-if="selectedVideoData.tiktok_url"
          >
            <el-icon><Link /></el-icon> 打开TikTok
          </el-button>
          <el-button
            type="success"
            @click="openProductUrl(selectedVideoData.product_url)"
            v-if="selectedVideoData.product_url"
          >
            <el-icon><ShoppingCart /></el-icon> 查看商品
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { kalodataApi, type KalodataItem } from '@/api/kalodata'
import {
  Delete,
  Link,
  ShoppingCart,
  VideoPlay,
  Files,
  User,
  Money,
  DataAnalysis,
  Histogram,
} from '@element-plus/icons-vue'

// 定义类目项类型
interface CategoryNode {
  id: number
  label: string
  value: string
  parent_value?: string
  children?: CategoryNode[]
  leaf?: boolean
}

// 国家选项
const countryOptions = {
  美国: 'US',
  印度尼西亚: 'ID',
  马来西亚: 'MY',
  泰国: 'TH',
  越南: 'VN',
  菲律宾: 'PH',
  英国: 'GB',
  新加坡: 'SG',
  墨西哥: 'MX',
}

// 数据状态
const kalodataList = ref<KalodataItem[]>([])
const loading = ref(false)
const selectedCountry = ref('MY') // 默认马来西亚
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 类目筛选相关
const level1Categories = ref<CategoryNode[]>([]) // 一级类目列表
const selectedCategory = ref<string[]>([]) // 当前选中的类目
const selectedCategoryLabel = ref<string>('') // 存储三级类目名称
const categoryCache = ref<Record<string, CategoryNode[]>>({}) // 类目缓存

// 类目级联配置
const categoryProps = {
  label: 'label',
  value: 'value',
  children: 'children',
  checkStrictly: false,
  lazy: true,
  lazyLoad(node: { level: number; value: string }, resolve: (nodes: CategoryNode[]) => void) {
    const { level, value } = node

    if (level === 0) {
      // 已在mounted中加载一级类目
      resolve([])
      return
    }

    if (level === 1) {
      // 加载二级类目
      loadLevel2Categories(value, resolve)
    } else if (level === 2) {
      // 加载三级类目
      loadLevel3Categories(value, resolve)
    }
  },
}

// 加载一级类目
const loadLevel1Categories = async () => {
  try {
    const res = await kalodataApi.getLevel1Categories()
    if (res.data.code === 200) {
      const categories = res.data.data.map((item) => ({
        ...item,
        leaf: false, // 非叶子节点，有子类目
      })) as CategoryNode[]

      level1Categories.value = categories
      categoryCache.value['level1'] = categories
    } else {
      ElMessage.error(res.data.message || '获取类目失败')
    }
  } catch (error) {
    console.error('获取一级类目失败:', error)
    ElMessage.error('获取类目失败')
  }
}

// 加载二级类目
const loadLevel2Categories = async (level1Id: string, resolve: (nodes: CategoryNode[]) => void) => {
  try {
    // 检查缓存
    if (categoryCache.value[`level2_${level1Id}`]) {
      resolve(categoryCache.value[`level2_${level1Id}`])
      return
    }

    const res = await kalodataApi.getLevel2Categories(level1Id)
    if (res.data.code === 200) {
      const nodes = res.data.data.map((item) => ({
        ...item,
        leaf: false, // 非叶子节点，有子类目
      })) as CategoryNode[]

      // 存入缓存
      categoryCache.value[`level2_${level1Id}`] = nodes
      resolve(nodes)
    } else {
      ElMessage.error(res.data.message || '获取二级类目失败')
      resolve([])
    }
  } catch (error) {
    console.error('获取二级类目失败:', error)
    ElMessage.error('获取二级类目失败')
    resolve([])
  }
}

// 加载三级类目
const loadLevel3Categories = async (level2Id: string, resolve: (nodes: CategoryNode[]) => void) => {
  try {
    // 检查缓存
    if (categoryCache.value[`level3_${level2Id}`]) {
      resolve(categoryCache.value[`level3_${level2Id}`])
      return
    }

    const res = await kalodataApi.getLevel3Categories(level2Id)
    if (res.data.code === 200) {
      const nodes = res.data.data.map((item) => ({
        ...item,
        leaf: true, // 叶子节点，没有子类目
      })) as CategoryNode[]

      // 存入缓存
      categoryCache.value[`level3_${level2Id}`] = nodes
      resolve(nodes)
    } else {
      ElMessage.error(res.data.message || '获取三级类目失败')
      resolve([])
    }
  } catch (error) {
    console.error('获取三级类目失败:', error)
    ElMessage.error('获取三级类目失败')
    resolve([])
  }
}

// 处理类目变化
const handleCategoryChange = () => {
  if (selectedCategory.value && selectedCategory.value.length === 3) {
    // 当用户选择了三级类目，获取对应的名称
    const cacheKey = `level3_${selectedCategory.value[1]}`
    const level3Cache = categoryCache.value[cacheKey] || []

    const category = level3Cache.find((item) => item.value === selectedCategory.value[2])
    if (category) {
      selectedCategoryLabel.value = category.label
    } else {
      // 如果缓存中找不到，尝试从DOM中查找（级联选择器应该已加载了选项）
      console.warn('未在缓存中找到类目标签，使用空值')
      selectedCategoryLabel.value = ''
    }

    // 选择到了三级类目，重新加载数据
    currentPage.value = 1
    fetchKalodataByCountry()
  }
}

// 视频预览相关
const videoDialogVisible = ref(false)
const currentVideo = ref('')
const selectedVideoData = ref<KalodataItem | null>(null)
const videoPlayer = ref<HTMLVideoElement | null>(null)

// 根据国家获取数据
const fetchKalodataByCountry = async () => {
  try {
    loading.value = true

    // 创建符合FilterParams接口的参数对象
    const params = {
      country: selectedCountry.value,
      page: currentPage.value,
      page_size: pageSize.value,
    } as const

    // 如果选择了三级类目，添加类目筛选条件
    type QueryParams = {
      country: string
      page: number
      page_size: number
      category?: string
    }

    const queryParams: QueryParams = { ...params }
    if (
      selectedCategory.value &&
      selectedCategory.value.length === 3 &&
      selectedCategoryLabel.value
    ) {
      queryParams.category = selectedCategoryLabel.value // 使用三级类目名称进行查询
    }

    const response = await kalodataApi.getKalodataByFilters(queryParams)

    if (response.data.code === 200) {
      kalodataList.value = response.data.data.items
      total.value = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取Kalodata数据失败:', error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

// 国家切换
const handleCountryChange = () => {
  currentPage.value = 1 // 重置页码
  fetchKalodataByCountry()
}

// 分页处理
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  fetchKalodataByCountry()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1 // 重置页码
  fetchKalodataByCountry()
}

// 打开TikTok链接
const openTiktokUrl = (url: string) => {
  if (url) {
    window.open(url, '_blank')
  } else {
    ElMessage.warning('无效的TikTok链接')
  }
}

// 打开商品链接
const openProductUrl = (url: string) => {
  if (url) {
    window.open(url, '_blank')
  } else {
    ElMessage.warning('无效的商品链接')
  }
}

// 预览视频
const previewVideo = (row: KalodataItem) => {
  if (row.video_url) {
    videoDialogVisible.value = true
    currentVideo.value = row.video_url
    selectedVideoData.value = row
  } else {
    ElMessage.warning('无效的视频链接')
  }
}

// 清空类目
const handleClearCategory = () => {
  selectedCategory.value = []
  selectedCategoryLabel.value = ''
  currentPage.value = 1
  fetchKalodataByCountry()
}

// 初始化
onMounted(async () => {
  await loadLevel1Categories() // 加载一级类目
  fetchKalodataByCountry()
})
</script>

<style scoped>
.kalodata-container {
  padding: 20px;
}

.kalodata-card {
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  width: 100%;
  gap: 20px;
  padding: 16px 20px;
  background-color: #f5faff;
  border-bottom: 1px solid #ebeef5;
}

.title-area {
  display: flex;
  align-items: center;
}

.title-area h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
}

.title-area h2::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 22px;
  background-color: #409eff;
  margin-right: 12px;
  border-radius: 2px;
}

.filter-container {
  display: flex;
  gap: 24px;
  align-items: center;
  flex-wrap: wrap;
}

.country-filter,
.category-filter {
  display: flex;
  align-items: center;
  white-space: nowrap;
}

.filter-label {
  margin-right: 12px;
  font-weight: 600;
  color: #606266;
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 0 0 8px 8px;
}

.video-dialog :deep(.el-dialog__header) {
  padding: 16px 20px;
  margin-right: 0;
  background-color: #f5faff;
  border-bottom: 1px solid #ebeef5;
}

.video-dialog :deep(.el-dialog__title) {
  font-weight: 600;
  color: #303133;
}

.video-dialog :deep(.el-dialog__body) {
  padding: 20px;
}

.video-container {
  width: 100%;
  margin-bottom: 20px;
}

.video-info {
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.video-info h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  color: #303133;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}

.info-item {
  display: flex;
  margin-bottom: 8px;
}

.info-label {
  font-weight: 600;
  color: #606266;
  margin-right: 8px;
  min-width: 80px;
  display: flex;
  align-items: center;
}

.info-label .el-icon {
  margin-right: 5px;
}

.info-value {
  color: #333;
  flex: 1;
}

.video-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.video-actions .el-button {
  font-weight: 500;
}

.highlight-number {
  font-weight: 600;
  color: #409eff;
}

.action-buttons {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.action-buttons .el-button {
  margin: 0 4px;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 12px 16px;
  }

  .filter-container {
    width: 100%;
    margin-top: 10px;
    gap: 12px;
  }

  .country-filter,
  .category-filter {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>
