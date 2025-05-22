<template>
  <div class="category-manage-container">
    <el-card class="category-card">
      <template #header>
        <div class="card-header">
          <div class="title-area">
            <h2>类目管理</h2>
          </div>
          <div class="header-actions">
            <div class="country-selector">
              <span class="selector-label">选择国家:</span>
              <el-select
                v-model="selectedCountry"
                placeholder="请选择国家"
                @change="handleCountryChange"
                size="large"
                style="width: 160px"
              >
                <el-option
                  v-for="(code, name) in countryOptions"
                  :key="code"
                  :label="name"
                  :value="code"
                />
              </el-select>
            </div>
            <div class="cookie-config">
              <el-button type="primary" @click="openCookieConfigDialog" size="large">
                <el-icon><Setting /></el-icon> 配置Cookie
              </el-button>
            </div>
          </div>
        </div>
      </template>

      <!-- 统计信息区域 -->
      <div class="quick-stats-panel" v-if="showStatistics">
        <div class="quick-stats-content">
          <div class="selected-info">
            <span class="info-tag country-tag">
              <el-icon><Flag /></el-icon> 国家: {{ statistics.country }}
            </span>
            <span class="info-tag category-tag">
              <el-icon><Document /></el-icon> 类目: {{ statistics.category }}
            </span>
          </div>
          <div class="stats-data">
            <div class="stat-box">
              <div class="stat-label">数据总数</div>
              <div class="stat-value">{{ statistics.total_count }}</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">最新数据时间</div>
              <div class="stat-value">{{ formatDate(statistics.latest_date) }}</div>
            </div>
          </div>
          <div class="stats-actions">
            <el-button
              type="primary"
              @click="handleFetchLatestData"
              :disabled="!currentCategory"
              :loading="fetchingLatestData"
            >
              <el-icon><Refresh /></el-icon> 获取最新数据
            </el-button>
          </div>
        </div>
      </div>

      <div class="category-content">
        <div class="category-tree">
          <!-- 一级类目列表 -->
          <div class="level-column">
            <div class="level-title">
              <el-icon><Folder /></el-icon> 一级类目
            </div>
            <div class="category-list" v-loading="loading.level1">
              <div
                v-for="item in categories.level1"
                :key="item.id"
                class="category-item"
                :class="{ active: selectedCategories.level1 === item.value }"
              >
                <div class="category-item-content" @click="selectLevel1Category(item)">
                  {{ item.label }}
                </div>
                <el-button
                  type="primary"
                  size="small"
                  class="fetch-category-btn"
                  @click="openFetchByCategory1Dialog(item)"
                  :loading="item.value === processingCategory1"
                  title="批量获取该类目下所有三级类目数据"
                >
                  <el-icon><Download /></el-icon>
                </el-button>
              </div>
              <el-empty v-if="categories.level1.length === 0" description="暂无数据" />
            </div>
          </div>

          <!-- 二级类目列表 -->
          <div class="level-column">
            <div class="level-title">
              <el-icon><FolderOpened /></el-icon> 二级类目
            </div>
            <div class="category-list" v-loading="loading.level2">
              <div
                v-for="item in categories.level2"
                :key="item.id"
                class="category-item"
                :class="{ active: selectedCategories.level2 === item.value }"
                @click="selectLevel2Category(item)"
              >
                {{ item.label }}
              </div>
              <el-empty
                v-if="categories.level2.length === 0"
                description="请先选择一级类目"
                :image-size="80"
              />
            </div>
          </div>

          <!-- 三级类目列表 -->
          <div class="level-column">
            <div class="level-title">
              <el-icon><Document /></el-icon> 三级类目
            </div>
            <div class="category-list" v-loading="loading.level3">
              <div
                v-for="item in categories.level3"
                :key="item.id"
                class="category-item"
                :class="{ active: selectedCategories.level3 === item.value }"
                @click="selectLevel3Category(item)"
              >
                {{ item.label }}
              </div>
              <el-empty
                v-if="categories.level3.length === 0"
                description="请先选择二级类目"
                :image-size="80"
              />
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- Cookie配置对话框 -->
    <el-dialog v-model="cookieConfigDialogVisible" title="配置Cookie" width="600px" center>
      <div class="cookie-config-form">
        <el-form>
          <el-form-item label="Kalodata Cookie" label-width="120px">
            <el-input
              v-model="cookieValue"
              type="textarea"
              :rows="6"
              placeholder="请输入Kalodata Cookie"
            ></el-input>
            <div class="form-tip">Cookie将被安全地存储在浏览器的本地存储中，以便下次使用。</div>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cookieConfigDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveCookie">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 获取最新数据结果对话框 -->
    <el-dialog v-model="fetchResultDialogVisible" title="获取结果" width="500px">
      <div class="fetch-result-content">
        <el-result icon="success" title="数据获取成功" :sub-title="fetchResultMessage"></el-result>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="fetchResultDialogVisible = false">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 批量获取一级类目数据对话框 -->
    <el-dialog
      v-model="fetchByCategory1DialogVisible"
      :title="`批量获取 ${selectedCategory1?.label || ''} 类目数据`"
      width="650px"
      destroy-on-close
    >
      <template v-if="!fetchByCategory1Result">
        <div class="fetch-category1-form">
          <p class="form-desc">
            此操作将获取 <strong>{{ selectedCategory1?.label }}</strong> 类目下所有三级类目的数据。
            <br />请确保您有足够的权限和正确的Cookie。
          </p>

          <el-form label-position="top">
            <el-form-item label="Cookie" required>
              <el-input
                v-model="category1CookieValue"
                type="textarea"
                :rows="4"
                placeholder="请输入Kalodata Cookie"
              ></el-input>
            </el-form-item>

            <el-form-item>
              <el-alert
                type="info"
                :closable="false"
                title="数据将使用最近7天的范围进行获取"
                description="获取过程可能需要几分钟时间，请耐心等待。"
                show-icon
              />
            </el-form-item>
          </el-form>
        </div>
      </template>

      <template v-else>
        <el-result
          :icon="fetchByCategory1Result.code === 200 ? 'success' : 'error'"
          :title="fetchByCategory1Result.code === 200 ? '批量获取成功' : '批量获取失败'"
          :sub-title="fetchByCategory1Result.message"
        >
          <template v-if="fetchByCategory1Result.code === 200">
            <div class="result-summary">
              <div class="summary-item">
                <div class="summary-label">成功获取</div>
                <div class="summary-value success">
                  {{ fetchByCategory1Result.data.success_count }}
                </div>
              </div>
              <div class="summary-item">
                <div class="summary-label">已存在跳过</div>
                <div class="summary-value info">{{ fetchByCategory1Result.data.skip_count }}</div>
              </div>
              <div class="summary-item">
                <div class="summary-label">失败</div>
                <div class="summary-value error">
                  {{ fetchByCategory1Result.data.failed_categories_count }}
                </div>
              </div>
              <div class="summary-item">
                <div class="summary-label">二级类目数</div>
                <div class="summary-value">{{ fetchByCategory1Result.data.total_category2 }}</div>
              </div>
              <div class="summary-item">
                <div class="summary-label">三级类目数</div>
                <div class="summary-value">{{ fetchByCategory1Result.data.total_category3 }}</div>
              </div>
              <div class="summary-item">
                <div class="summary-label">日期范围</div>
                <div class="summary-value">
                  {{ fetchByCategory1Result.data.start_date }} 至
                  {{ fetchByCategory1Result.data.end_date }}
                </div>
              </div>
            </div>

            <template v-if="fetchByCategory1Result.data.failed_categories.length > 0">
              <h4 class="failed-title">失败的类目:</h4>
              <el-table
                :data="fetchByCategory1Result.data.failed_categories"
                style="width: 100%"
                size="small"
                :border="true"
              >
                <el-table-column
                  prop="category3_label"
                  label="类目名称"
                  width="180"
                ></el-table-column>
                <el-table-column prop="error" label="错误原因"></el-table-column>
              </el-table>
            </template>
          </template>
        </el-result>
      </template>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="fetchByCategory1DialogVisible = false">关闭</el-button>
          <el-button
            v-if="!fetchByCategory1Result"
            type="primary"
            @click="fetchDataByCategory1"
            :loading="fetchingCategory1Data"
            :disabled="!category1CookieValue || !selectedCategory1"
          >
            确认获取
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { kalodataApi, type KalodataStatistics, type FetchByCategory1Response } from '@/api/kalodata'
import {
  Download,
  Setting,
  Refresh,
  Folder,
  FolderOpened,
  Document,
  Flag,
} from '@element-plus/icons-vue'

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

// 类目项类型
interface CategoryItem {
  id: number
  label: string
  value: string
  parent_value?: string
}

// 类目数据
const categories = reactive({
  level1: [] as CategoryItem[],
  level2: [] as CategoryItem[],
  level3: [] as CategoryItem[],
})

// 加载状态
const loading = reactive({
  level1: false,
  level2: false,
  level3: false,
  statistics: false,
})

// 选中的国家
const selectedCountry = ref('MY') // 默认马来西亚

// 选中的类目
const selectedCategories = reactive({
  level1: '',
  level2: '',
  level3: '',
})

// 当前选中类目名称（用于统计接口）
const selectedCategoryName = ref('')

// 数据统计信息
const statistics = reactive<KalodataStatistics>({
  total_count: 0,
  latest_date: '',
  country: '',
  category: '',
})

// 是否显示统计面板
const showStatistics = ref(false)

// 保存当前选中的类目信息（用于获取最新数据）
const currentCategory = ref<{ label: string; value: string } | null>(null)

// 批量获取一级类目相关
const fetchByCategory1DialogVisible = ref(false)
const selectedCategory1 = ref<CategoryItem | null>(null)
const category1CookieValue = ref('')
const fetchingCategory1Data = ref(false)
const processingCategory1 = ref('')
const fetchByCategory1Result = ref<{
  code: number
  message: string
  data: FetchByCategory1Response
} | null>(null)

// Cookie配置相关
const cookieConfigDialogVisible = ref(false)
const localStorageCookieKey = 'kalodata_cookie'

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
  } catch (e) {
    return dateStr
  }
}

// 打开Cookie配置对话框
const openCookieConfigDialog = () => {
  cookieConfigDialogVisible.value = true
  // 从本地存储加载Cookie
  const savedCookie = localStorage.getItem(localStorageCookieKey)
  if (savedCookie) {
    cookieValue.value = savedCookie
  }
}

// 保存Cookie
const saveCookie = () => {
  if (cookieValue.value) {
    localStorage.setItem(localStorageCookieKey, cookieValue.value)
    ElMessage.success('Cookie保存成功')
  }
  cookieConfigDialogVisible.value = false
}

// 获取最新数据相关
const fetchResultDialogVisible = ref(false)
const fetchResultMessage = ref('')

// 处理获取最新数据
const handleFetchLatestData = () => {
  if (!cookieValue.value.trim()) {
    ElMessage.warning('请先配置Cookie')
    openCookieConfigDialog()
    return
  }

  fetchLatestData()
}

// 获取最新数据
const fetchLatestData = async () => {
  if (!cookieValue.value.trim()) {
    ElMessage.warning('请输入Cookie')
    return
  }

  if (!currentCategory.value) {
    ElMessage.warning('请先选择一个三级类目')
    return
  }

  fetchingLatestData.value = true
  fetchResultMessage.value = ''

  try {
    // 获取日期范围（7天）
    const { startDate, endDate } = getDateRange()

    // 准备请求参数
    const params = {
      cookie: cookieValue.value,
      country: selectedCountry.value,
      start_date: startDate,
      end_date: endDate,
      cate_ids: [currentCategory.value.value], // 三级类目ID
    }

    // 调用API获取最新数据
    const res = await kalodataApi.fetchAndStoreKalodata(params)

    if (res.data.code === 200) {
      const successCount = res.data.data.success_count || 0
      const skipCount = res.data.data.skip_count || 0

      fetchResultMessage.value = `获取结果：成功 ${successCount} 条，已存在 ${skipCount} 条`
      fetchResultDialogVisible.value = true

      // 保存cookie到本地存储
      localStorage.setItem(localStorageCookieKey, cookieValue.value)

      // 更新统计信息
      await fetchStatistics(selectedCountry.value, selectedCategoryName.value)

      ElMessage.success('获取数据成功')
    } else {
      fetchResultMessage.value = res.data.message || '获取失败'
      fetchResultDialogVisible.value = true
      ElMessage.error(res.data.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    fetchResultMessage.value = '获取失败: ' + (error as Error).message
    fetchResultDialogVisible.value = true
    ElMessage.error('获取数据失败')
  } finally {
    fetchingLatestData.value = false
  }
}

// 国家变更处理
const handleCountryChange = () => {
  // 重置类目选择
  selectedCategories.level1 = ''
  selectedCategories.level2 = ''
  selectedCategories.level3 = ''
  selectedCategoryName.value = ''
  currentCategory.value = null

  // 重置统计信息
  showStatistics.value = false

  // 重新加载一级类目（注：类目请求不传country参数）
  loadLevel1Categories()
}

// 加载一级类目
const loadLevel1Categories = async () => {
  try {
    loading.level1 = true
    categories.level2 = []
    categories.level3 = []

    const res = await kalodataApi.getLevel1Categories()
    if (res.data.code === 200) {
      categories.level1 = res.data.data
    } else {
      ElMessage.error(res.data.message || '获取一级类目失败')
    }
  } catch (error) {
    console.error('获取一级类目失败:', error)
    ElMessage.error('获取一级类目失败')
  } finally {
    loading.level1 = false
  }
}

// 选择一级类目，加载对应的二级类目
const selectLevel1Category = async (category: CategoryItem) => {
  selectedCategories.level1 = category.value
  selectedCategories.level2 = ''
  selectedCategories.level3 = ''
  selectedCategoryName.value = ''
  currentCategory.value = null
  categories.level2 = []
  categories.level3 = []
  showStatistics.value = false

  try {
    loading.level2 = true
    const res = await kalodataApi.getLevel2Categories(category.value)
    if (res.data.code === 200) {
      categories.level2 = res.data.data
    } else {
      ElMessage.error(res.data.message || '获取二级类目失败')
    }
  } catch (error) {
    console.error('获取二级类目失败:', error)
    ElMessage.error('获取二级类目失败')
  } finally {
    loading.level2 = false
  }
}

// 选择二级类目，加载对应的三级类目
const selectLevel2Category = async (category: CategoryItem) => {
  selectedCategories.level2 = category.value
  selectedCategories.level3 = ''
  selectedCategoryName.value = ''
  currentCategory.value = null
  categories.level3 = []
  showStatistics.value = false

  try {
    loading.level3 = true
    const res = await kalodataApi.getLevel3Categories(category.value)
    if (res.data.code === 200) {
      categories.level3 = res.data.data
    } else {
      ElMessage.error(res.data.message || '获取三级类目失败')
    }
  } catch (error) {
    console.error('获取三级类目失败:', error)
    ElMessage.error('获取三级类目失败')
  } finally {
    loading.level3 = false
  }
}

// 选择三级类目，加载对应的统计信息
const selectLevel3Category = async (category: CategoryItem) => {
  selectedCategories.level3 = category.value
  selectedCategoryName.value = category.label

  // 保存类目的label和value
  currentCategory.value = {
    label: category.label,
    value: category.value,
  }

  // 获取统计信息
  await fetchStatistics(selectedCountry.value, category.label)
}

// 获取统计信息
const fetchStatistics = async (country: string, category: string) => {
  showStatistics.value = true
  loading.statistics = true

  try {
    const res = await kalodataApi.getKalodataStatistics(country, category)
    if (res.data.code === 200) {
      Object.assign(statistics, res.data.data)
    } else {
      ElMessage.error(res.data.message || '获取统计信息失败')
    }
  } catch (error) {
    console.error('获取统计信息失败:', error)
    ElMessage.error('获取统计信息失败')
  } finally {
    loading.statistics = false
  }
}

// cookie输入框值
const cookieValue = ref('')
// 获取最新数据loading状态
const fetchingLatestData = ref(false)

// 获取日期范围
const getDateRange = () => {
  const endDate = new Date()
  endDate.setDate(endDate.getDate() - 1) // 当前日期前一天

  const startDate = new Date(endDate)
  startDate.setDate(startDate.getDate() - 7) // end_date前7天

  // 格式化日期为YYYY-MM-DD
  const formatDate = (date: Date) => {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }

  return {
    startDate: formatDate(startDate),
    endDate: formatDate(endDate),
  }
}

// 打开批量获取一级类目数据对话框
const openFetchByCategory1Dialog = (category: CategoryItem) => {
  selectedCategory1.value = category
  category1CookieValue.value = cookieValue.value // 复用之前输入的cookie
  fetchByCategory1Result.value = null
  fetchByCategory1DialogVisible.value = true
}

// 批量获取一级类目数据
const fetchDataByCategory1 = async () => {
  if (!selectedCategory1.value || !category1CookieValue.value.trim()) {
    ElMessage.warning('请输入Cookie')
    return
  }

  const params = {
    country: selectedCountry.value,
    category1: selectedCategory1.value.value,
    cookie: category1CookieValue.value,
  }

  fetchingCategory1Data.value = true
  processingCategory1.value = selectedCategory1.value.value

  try {
    const res = await kalodataApi.fetchByCategoryLevel1(params)
    fetchByCategory1Result.value = res.data

    // 更新主 cookie 值，方便下次使用
    cookieValue.value = category1CookieValue.value

    ElMessage.success('批量获取数据成功')
  } catch (error) {
    console.error('批量获取数据失败:', error)
    ElMessage.error('批量获取数据失败')
  } finally {
    fetchingCategory1Data.value = false
    processingCategory1.value = ''
  }
}

// 初始化
onMounted(() => {
  const savedCookie = localStorage.getItem(localStorageCookieKey)
  if (savedCookie) {
    cookieValue.value = savedCookie
  }

  loadLevel1Categories()
})
</script>

<style scoped>
.category-manage-container {
  padding: 20px;
}

.category-card {
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  flex-wrap: wrap;
  gap: 16px;
}

.title-area h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.country-selector {
  display: flex;
  align-items: center;
}

.selector-label {
  margin-right: 12px;
  font-weight: 600;
  color: #606266;
}

/* 快速统计信息面板 */
.quick-stats-panel {
  margin: 16px 0 24px;
  border-radius: 8px;
  background-color: #f9fafc;
  border: 1px solid #ebeef5;
  overflow: hidden;
}

.quick-stats-content {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.selected-info {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.info-tag {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

.country-tag {
  background-color: #ecf5ff;
  color: #409eff;
}

.category-tag {
  background-color: #f0f9eb;
  color: #67c23a;
}

.stats-data {
  display: flex;
  gap: 24px;
}

.stat-box {
  text-align: center;
  background: white;
  padding: 10px 16px;
  border-radius: 6px;
  border: 1px solid #ebeef5;
  min-width: 120px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #409eff;
}

.stats-actions {
  margin-left: auto;
}

.category-content {
  padding: 10px 0;
}

.category-tree {
  display: flex;
  gap: 16px;
  margin-top: 20px;
  overflow-x: auto;
}

.level-column {
  flex: 1;
  min-width: 220px;
  max-width: 320px;
  border-radius: 8px;
  border: 1px solid #ebeef5;
  overflow: hidden;
}

.level-title {
  padding: 12px 16px;
  font-weight: 600;
  background-color: #f5faff;
  border-bottom: 1px solid #ebeef5;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 6px;
}

.category-list {
  height: 500px;
  overflow-y: auto;
  padding: 8px;
  background-color: #fff;
}

.category-item {
  padding: 8px 12px;
  margin-bottom: 6px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
  border: 1px solid transparent;
}

.category-item:hover {
  background-color: #f5f7fa;
  border-color: #e4e7ed;
}

.category-item.active {
  background-color: #ecf5ff;
  color: #409eff;
  border-color: #d9ecff;
}

.category-item-content {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fetch-category-btn {
  opacity: 0.7;
  transition: opacity 0.3s;
}

.category-item:hover .fetch-category-btn {
  opacity: 1;
}

/* Cookie配置对话框 */
.cookie-description {
  margin-bottom: 16px;
  line-height: 1.6;
  color: #606266;
}

/* 对话框样式 */
.dialog-description {
  margin-bottom: 20px;
  color: #606266;
  line-height: 1.5;
}

.dialog-description b {
  color: #409eff;
}

.dialog-warning {
  margin: 16px 0;
}

.fetch-result {
  margin: 16px 0;
}

.result-summary {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.summary-item {
  background-color: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.summary-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 6px;
}

.summary-value {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.failed-title {
  margin: 20px 0 10px;
  font-size: 16px;
  color: #f56c6c;
}

/* Cookie配置样式 */
.cookie-config-form {
  padding: 0 20px;
}

.form-tip {
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
  line-height: 1.5;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  gap: 10px;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .country-selector {
    width: 100%;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .quick-stats-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-data {
    width: 100%;
    justify-content: space-between;
  }

  .stats-actions {
    width: 100%;
    margin-left: 0;
    text-align: center;
  }

  .category-tree {
    flex-direction: column;
  }

  .level-column {
    width: 100%;
    margin-right: 0;
    margin-bottom: 20px;
  }

  .category-list {
    max-height: 300px;
  }

  .result-summary {
    grid-template-columns: 1fr;
  }

  .fetch-form {
    display: flex;
    flex-direction: column;
  }
}

/* 批量获取一级类目数据结果样式 */
.fetch-category1-form {
  padding: 0 20px;
}

.form-desc {
  margin-bottom: 20px;
  line-height: 1.6;
  color: #606266;
}

.result-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.summary-item {
  background-color: #f9fafc;
  border-radius: 6px;
  padding: 12px 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.summary-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.summary-value {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.summary-value.success {
  color: #67c23a;
}

.summary-value.info {
  color: #909399;
}

.summary-value.error {
  color: #f56c6c;
}

.failed-title {
  margin: 20px 0 12px;
  font-size: 16px;
  color: #606266;
}

/* 获取结果对话框 */
.fetch-result {
  text-align: center;
  padding: 20px 0;
}
</style>
