<template>
  <div class="feedback-container">
    <h1 class="page-title">反馈收集</h1>
    
    <el-row :gutter="20">
      <!-- 左侧统计分析 -->
      <el-col :span="8">
        <!-- 满意度统计卡片 -->
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>满意度统计</span>
            </div>
          </template>
          
          <div class="satisfaction-overview">
            <div class="satisfaction-score">
              <div class="score-value">{{ averageSatisfaction }}</div>
              <div class="score-label">平均满意度</div>
            </div>
            <div class="satisfaction-chart">
              <div ref="satisfactionChart" class="chart"></div>
            </div>
          </div>
        </el-card>
        
        <!-- 班级满意度对比卡片 -->
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>班级满意度对比</span>
            </div>
          </template>
          
          <div ref="classComparisonChart" class="chart" style="height: 300px;"></div>
        </el-card>
        
        <!-- 关键词云卡片 -->
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>热点关键词</span>
            </div>
          </template>
          
          <div class="keyword-cloud">
            <div v-for="(keyword, index) in keywords" :key="index" class="keyword-item" :style="getKeywordStyle(keyword)">
              {{ keyword.text }}
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧反馈列表 -->
      <el-col :span="16">
        <div class="feedback-tools">
          <div class="filter-container">
            <el-select v-model="filterSatisfaction" placeholder="满意度" clearable @change="filterFeedbacks">
              <el-option label="全部" value="" />
              <el-option label="非常满意" value="5" />
              <el-option label="满意" value="4" />
              <el-option label="一般" value="3" />
              <el-option label="不满意" value="2" />
              <el-option label="非常不满意" value="1" />
            </el-select>
            
            <el-select v-model="filterClass" placeholder="班级" clearable @change="filterFeedbacks">
              <el-option label="全部" value="" />
              <el-option v-for="cls in classes" :key="cls" :label="cls" :value="cls" />
            </el-select>
            
            <el-date-picker
              v-model="filterDate"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
              @change="filterFeedbacks"
            />
          </div>
          
          <div class="export-actions">
            <el-button size="small" @click="exportFeedbacks('excel')">
              <el-icon><el-icon-document /></el-icon>
              导出数据
            </el-button>
          </div>
        </div>
        
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="10" animated />
        </div>
        
        <div v-else-if="filteredFeedbacks.length === 0" class="empty-container">
          <el-empty description="暂无反馈" />
        </div>
        
        <div v-else class="feedback-list">
          <el-card v-for="feedback in filteredFeedbacks" :key="feedback.id" class="feedback-card">
            <div class="feedback-header">
              <div class="student-info">
                <span class="student-name">{{ feedback.student_name }}</span>
                <span class="student-class">{{ feedback.student_class }}</span>
              </div>
              <div class="feedback-time">{{ formatDate(feedback.created_at) }}</div>
            </div>
            
            <div class="feedback-content">{{ feedback.content }}</div>
            
            <div class="feedback-rating">
              <div class="rating-label">满意度评分:</div>
              <el-rate
                v-model="feedback.satisfaction"
                disabled
                show-score
                text-color="#ff9900"
              />
            </div>
            
            <div class="feedback-tags">
              <el-tag 
                v-for="(tag, index) in getFeedbackTags(feedback)"
                :key="index"
                size="small"
                :type="getTagType(tag)"
                class="feedback-tag"
              >
                {{ tag }}
              </el-tag>
            </div>
          </el-card>
        </div>
        
        <div class="pagination-container">
          <el-pagination
            background
            layout="total, prev, pager, next"
            :total="total"
            :current-page="currentPage"
            :page-size="pageSize"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import * as echarts from 'echarts'
import { feedbackApi } from '../api'

// 状态变量
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const filterSatisfaction = ref('')
const filterClass = ref('')
const filterDate = ref(null)
const satisfactionChart = ref(null)
const classComparisonChart = ref(null)

// 反馈数据
const feedbacks = ref([])

// 统计数据
const satisfactionDistribution = ref({
  very_satisfied: 0,
  satisfied: 0,
  neutral: 0,
  dissatisfied: 0,
  very_dissatisfied: 0
})

const classDistribution = ref([])

// 关键词云数据
const keywords = ref([
  { text: '教学方法', weight: 28 },
  { text: '作业量', weight: 22 },
  { text: '课堂气氛', weight: 20 },
  { text: '教学内容', weight: 19 },
  { text: '难度适中', weight: 18 },
  { text: '讲解清晰', weight: 16 },
  { text: '案例生动', weight: 15 },
  { text: '互动性强', weight: 14 },
  { text: '进度合理', weight: 13 },
  { text: '练习充足', weight: 12 },
  { text: '思路清晰', weight: 11 },
  { text: '知识点全面', weight: 10 },
  { text: '重难点突出', weight: 9 },
  { text: '太难', weight: 8 },
  { text: '太简单', weight: 7 },
  { text: '环境嘈杂', weight: 6 },
  { text: '课堂秩序', weight: 5 },
])

// 班级列表
const classes = ref([
  '高三(1)班',
  '高三(2)班',
  '高三(3)班',
  '高三(4)班',
  '高三(5)班'
])

// 计算属性
const filteredFeedbacks = computed(() => {
  let result = [...feedbacks.value]
  
  // 按满意度筛选
  if (filterSatisfaction.value) {
    result = result.filter(f => f.satisfaction === parseInt(filterSatisfaction.value))
  }
  
  // 按班级筛选
  if (filterClass.value) {
    result = result.filter(f => f.student_class === filterClass.value)
  }
  
  // 按日期筛选
  if (filterDate.value && filterDate.value.length === 2) {
    const startDate = new Date(filterDate.value[0])
    const endDate = new Date(filterDate.value[1])
    endDate.setHours(23, 59, 59) // 设置为当天结束时间
    
    result = result.filter(f => {
      const createdDate = new Date(f.created_at)
      return createdDate >= startDate && createdDate <= endDate
    })
  }
  
  // 更新总数
  total.value = result.length
  
  // 应用分页
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  
  return result.slice(start, end)
})

const averageSatisfaction = computed(() => {
  if (feedbacks.value.length === 0) return '0.0'
  
  const sum = feedbacks.value.reduce((acc, f) => acc + f.satisfaction, 0)
  return (sum / feedbacks.value.length).toFixed(1)
})

// 方法
const filterFeedbacks = () => {
  currentPage.value = 1
  // 通过计算属性自动筛选
}

const handleCurrentChange = (page) => {
  currentPage.value = page
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const getFeedbackTags = (feedback) => {
  // 根据反馈内容提取标签（实际应用中可能需要NLP或预定义标签）
  const content = feedback.content.toLowerCase()
  const tags = []
  
  // 简单关键词匹配
  if (content.includes('教学') || content.includes('讲解')) tags.push('教学方法')
  if (content.includes('作业') || content.includes('练习')) tags.push('作业')
  if (content.includes('难') || content.includes('简单')) tags.push('难度')
  if (content.includes('互动') || content.includes('气氛')) tags.push('课堂氛围')
  if (content.includes('进度') || content.includes('时间')) tags.push('教学进度')
  
  // 如果没有匹配到标签，添加一个默认标签
  if (tags.length === 0) {
    if (feedback.satisfaction >= 4) tags.push('正面评价')
    else if (feedback.satisfaction <= 2) tags.push('负面评价')
    else tags.push('一般评价')
  }
  
  return tags
}

const getTagType = (tag) => {
  const tagTypes = {
    '教学方法': '',
    '作业': 'success',
    '难度': 'warning',
    '课堂氛围': 'info',
    '教学进度': 'danger',
    '正面评价': 'success',
    '负面评价': 'danger',
    '一般评价': 'info'
  }
  
  return tagTypes[tag] || ''
}

const getKeywordStyle = (keyword) => {
  const maxWeight = 28
  const minWeight = 5
  
  const fontSize = 12 + ((keyword.weight - minWeight) / (maxWeight - minWeight)) * 18
  
  return {
    fontSize: `${fontSize}px`,
    fontWeight: keyword.weight > 15 ? 'bold' : 'normal',
    color: getKeywordColor(keyword.weight)
  }
}

const getKeywordColor = (weight) => {
  const colors = [
    '#409EFF', // primary
    '#67C23A', // success
    '#E6A23C', // warning
    '#F56C6C', // danger
    '#909399', // info
    '#9370DB', // medium purple
    '#3CB371', // medium sea green
    '#20B2AA', // light sea green
    '#6495ED', // cornflower blue
    '#FF7F50'  // coral
  ]
  
  // 根据权重返回不同的颜色
  return colors[Math.floor(weight * colors.length / 30) % colors.length]
}

const initSatisfactionChart = () => {
  const chart = echarts.init(satisfactionChart.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: ['非常满意', '满意', '一般', '不满意', '非常不满意']
    },
    color: ['#67C23A', '#95D475', '#E6A23C', '#F89898', '#F56C6C'],
    series: [
      {
        name: '满意度分布',
        type: 'pie',
        radius: '65%',
        center: ['40%', '50%'],
        data: [
          { value: satisfactionDistribution.value.very_satisfied, name: '非常满意' },
          { value: satisfactionDistribution.value.satisfied, name: '满意' },
          { value: satisfactionDistribution.value.neutral, name: '一般' },
          { value: satisfactionDistribution.value.dissatisfied, name: '不满意' },
          { value: satisfactionDistribution.value.very_dissatisfied, name: '非常不满意' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

const initClassComparisonChart = () => {
  const chart = echarts.init(classComparisonChart.value)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      min: 0,
      max: 5,
      axisLabel: {
        formatter: '{value} 分'
      }
    },
    yAxis: {
      type: 'category',
      data: classDistribution.value.map(item => item.class)
    },
    series: [
      {
        name: '平均满意度',
        type: 'bar',
        data: classDistribution.value.map(item => item.avg_satisfaction),
        itemStyle: {
          color: (params) => {
            const value = params.value
            if (value >= 4) return '#67C23A'
            if (value >= 3) return '#E6A23C'
            return '#F56C6C'
          }
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c} 分'
        }
      }
    ]
  }
  
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

const exportFeedbacks = (format) => {
  // 实际应用中这里应该调用API导出数据
  alert(`正在导出${format === 'excel' ? 'Excel' : 'CSV'}文件...`)
}

// 生成模拟反馈数据
const generateMockFeedbacks = () => {
  const mockFeedbacks = []
  const studentNames = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十']
  const feedbackContents = [
    '老师的课讲得很好，内容生动有趣，讲解清晰。',
    '作业量有点大，希望能适当减少。',
    '教学进度有点快，有些知识点没有完全掌握。',
    '课堂气氛活跃，互动性很强，学习效果很好。',
    '老师讲解的例题比较难，希望能多讲解一些基础题目。',
    '课程内容很充实，但是希望能够增加一些实践环节。',
    '老师讲课很有激情，能够调动学生的积极性，很喜欢这种教学方式。',
    '课程内容难度适中，讲解清晰，很容易理解。',
    '有些知识点讲解得不够详细，希望能够增加课时。',
    '老师很耐心，对学生提出的问题都会详细解答。'
  ]
  
  // 用于生成满意度分布统计
  const satisfactionCounts = {
    very_satisfied: 0,   // 5分
    satisfied: 0,        // 4分
    neutral: 0,          // 3分
    dissatisfied: 0,     // 2分
    very_dissatisfied: 0 // 1分
  }
  
  // 用于生成班级满意度统计
  const classStats = {}
  
  for (let i = 1; i <= 50; i++) {
    const nameIndex = Math.floor(Math.random() * studentNames.length)
    const contentIndex = Math.floor(Math.random() * feedbackContents.length)
    const classIndex = Math.floor(Math.random() * classes.value.length)
    const className = classes.value[classIndex]
    const satisfaction = Math.floor(Math.random() * 5) + 1 // 1-5的随机分数
    
    // 更新满意度计数
    if (satisfaction === 5) satisfactionCounts.very_satisfied++
    else if (satisfaction === 4) satisfactionCounts.satisfied++
    else if (satisfaction === 3) satisfactionCounts.neutral++
    else if (satisfaction === 2) satisfactionCounts.dissatisfied++
    else if (satisfaction === 1) satisfactionCounts.very_dissatisfied++
    
    // 更新班级统计
    if (!classStats[className]) {
      classStats[className] = {
        total: 0,
        sum: 0
      }
    }
    classStats[className].total++
    classStats[className].sum += satisfaction
    
    // 创建日期（最近30天内的随机日期）
    const date = new Date()
    date.setDate(date.getDate() - Math.floor(Math.random() * 30))
    
    mockFeedbacks.push({
      id: i,
      student_name: `${studentNames[nameIndex]}${Math.floor(i / studentNames.length) + 1}`,
      student_class: className,
      content: feedbackContents[contentIndex],
      satisfaction: satisfaction,
      created_at: date.toISOString()
    })
  }
  
  // 保存满意度分布
  satisfactionDistribution.value = satisfactionCounts
  
  // 计算班级平均满意度
  classDistribution.value = []
  Object.keys(classStats).forEach(className => {
    const stat = classStats[className]
    classDistribution.value.push({
      class: className,
      avg_satisfaction: +(stat.sum / stat.total).toFixed(1)
    })
  })
  
  // 按平均满意度排序
  classDistribution.value.sort((a, b) => b.avg_satisfaction - a.avg_satisfaction)
  
  return mockFeedbacks
}

// 获取反馈数据
const fetchFeedbacks = async () => {
  loading.value = true
  
  try {
    // 模拟API调用
    setTimeout(() => {
      feedbacks.value = generateMockFeedbacks()
      total.value = feedbacks.value.length
      
      // 初始化图表
      initSatisfactionChart()
      initClassComparisonChart()
      
      loading.value = false
    }, 500)
    
    // 实际API调用
    /*
    const response = await feedbackApi.getFeedbacks()
    feedbacks.value = response
    total.value = response.length
    
    const stats = await feedbackApi.getFeedbackStatistics()
    satisfactionDistribution.value = stats.satisfaction_distribution
    classDistribution.value = stats.satisfaction_by_class
    */
  } catch (error) {
    console.error('Failed to fetch feedbacks', error)
  } finally {
    loading.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  fetchFeedbacks()
})
</script>

<style scoped>
.feedback-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 600;
  color: #333;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  font-weight: bold;
}

.satisfaction-overview {
  display: flex;
  align-items: center;
}

.satisfaction-score {
  text-align: center;
  padding: 20px;
  flex: 1;
}

.score-value {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
}

.score-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.satisfaction-chart {
  flex: 2;
}

.chart {
  height: 200px;
  width: 100%;
}

.keyword-cloud {
  padding: 20px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.keyword-item {
  margin: 5px;
  padding: 3px 8px;
  border-radius: 15px;
  cursor: pointer;
  transition: transform 0.3s;
}

.keyword-item:hover {
  transform: scale(1.1);
}

.feedback-tools {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-container {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.loading-container,
.empty-container {
  padding: 40px 0;
  text-align: center;
}

.feedback-card {
  margin-bottom: 20px;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.student-name {
  font-weight: bold;
  margin-right: 10px;
}

.student-class {
  color: #909399;
}

.feedback-time {
  color: #909399;
  font-size: 12px;
}

.feedback-content {
  margin-bottom: 15px;
  line-height: 1.6;
  white-space: pre-line;
}

.feedback-rating {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.rating-label {
  margin-right: 10px;
  color: #606266;
}

.feedback-tags {
  margin-top: 10px;
}

.feedback-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 