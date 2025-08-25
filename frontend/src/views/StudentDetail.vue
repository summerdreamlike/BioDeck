<template>
  <div class="student-detail-container">
    <div class="header-actions">
      <el-button @click="goBack" type="primary" plain icon="el-icon-arrow-left">
        返回
      </el-button>
    </div>

    <div v-if="loading" class="loading">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else>
      <!-- 学生基本信息卡片 -->
      <el-card class="info-card">
        <div class="student-info">
          <div class="avatar-container">
            <el-avatar :size="80" :src="studentData.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
          </div>
          <div class="info-details">
            <h2>{{ studentData.name }} <el-tag size="small">{{ studentData.studentId }}</el-tag></h2>
            <p>{{ studentData.class }} | {{ studentData.gender }} | {{ studentData.age }}岁</p>
            <div class="ranking-badge">
              <span class="rank-label">学习指数排名</span>
              <span class="rank-value">{{ studentData.rank }}</span>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 学习指标卡片 -->
      <el-row :gutter="20" class="metric-cards">
        <el-col :span="8" v-for="(metric, index) in studentData.metrics" :key="index">
          <el-card class="metric-card" shadow="hover">
            <div class="metric-title">{{ metric.name }}</div>
            <div class="metric-chart">
              <el-progress 
                type="dashboard" 
                :percentage="metric.value" 
                :color="getProgressColor(metric.value)"
              />
            </div>
            <div class="metric-comparison">
              <span>班级平均: {{ metric.classAvg }}%</span>
              <span :class="getComparisonClass(metric.value, metric.classAvg)">
                {{ getComparisonText(metric.value, metric.classAvg) }}
              </span>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 学习详情图表 -->
      <el-row :gutter="20" class="chart-section">
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="chart-title">学习趋势（近30天）</div>
            </template>
            <div ref="trendChart" style="height: 350px; width: 100%"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="chart-title">知识点掌握情况</div>
            </template>
            <div ref="knowledgeChart" style="height: 350px; width: 100%"></div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 学习时间统计 -->
      <el-card class="time-stats-card">
        <template #header>
          <div class="card-header">
            <span>学习时间统计</span>
            <el-radio-group v-model="timeRange" size="small">
              <el-radio-button label="week">本周</el-radio-button>
              <el-radio-button label="month">本月</el-radio-button>
              <el-radio-button label="semester">本学期</el-radio-button>
            </el-radio-group>
          </div>
        </template>
        <div ref="timeStatsChart" style="height: 300px; width: 100%"></div>
      </el-card>

      <!-- 推荐改进措施 -->
      <el-card class="recommendation-card">
        <template #header>
          <div class="card-title">学习改进建议</div>
        </template>
        <div class="recommendations">
          <div v-for="(item, index) in studentData.recommendations" :key="index" class="recommendation-item">
            <div class="recommendation-icon">
              <el-icon><el-icon-warning-outline /></el-icon>
            </div>
            <div class="recommendation-content">
              <div class="recommendation-title">{{ item.title }}</div>
              <div class="recommendation-desc">{{ item.description }}</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStudentsStore } from '../store'
import { studentsApi } from '../api'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()
const studentsStore = useStudentsStore()
const studentId = ref(parseInt(route.params.id))
const loading = ref(true)
const trendChart = ref(null)
const knowledgeChart = ref(null)
const timeStatsChart = ref(null)
const timeRange = ref('week')

const studentData = reactive({
  id: 0,
  name: '',
  studentId: '',
  class: '',
  gender: '',
  age: 0,
  rank: 0,
  avatar: '',
  metrics: [
    { name: '学习完成度', value: 0, classAvg: 0 },
    { name: '正确率', value: 0, classAvg: 0 },
    { name: '专注力', value: 0, classAvg: 0 }
  ],
  recommendations: []
})

const goBack = () => {
  router.push('/dashboard')
}

const getProgressColor = (value) => {
  if (value < 60) return '#F56C6C'
  if (value < 80) return '#E6A23C'
  return '#67C23A'
}

const getComparisonClass = (value, avg) => {
  const diff = value - avg
  if (diff > 5) return 'comparison better'
  if (diff < -5) return 'comparison worse'
  return 'comparison same'
}

const getComparisonText = (value, avg) => {
  const diff = value - avg
  if (diff > 5) return `高于平均${diff.toFixed(1)}%`
  if (diff < -5) return `低于平均${Math.abs(diff).toFixed(1)}%`
  return '与平均接近'
}

const fetchStudentData = async () => {
  loading.value = true
  try {
    // 模拟从API获取数据，实际使用时替换为API调用
    // const response = await studentsApi.getStudentDetails(studentId.value)
    // const data = response.data
    
    // 使用模拟数据
    const data = {
      id: studentId.value,
      name: '张三',
      studentId: 'S20210001',
      class: '高三(1)班',
      gender: '男',
      age: 18,
      rank: 1,
      avatar: '',
      metrics: [
        { name: '学习完成度', value: 98, classAvg: 86 },
        { name: '正确率', value: 96, classAvg: 73 },
        { name: '专注力', value: 92, classAvg: 78 }
      ],
      recommendations: [
        { 
          title: '细胞结构与功能复习', 
          description: '细胞结构部分的题目正确率低于平均水平，建议回顾细胞膜、细胞器的结构与功能，配合显微图练习。' 
        },
        { 
          title: '遗传规律专项训练', 
          description: '二杂合交配与自由组合定律题型错误率较高，建议进行遗传图谱与亲子鉴定类题目专项训练。' 
        },
        { 
          title: '生态系统案例分析', 
          description: '对能量流动与物质循环的理解不够深入，建议多做生态系统能量金字塔与食物网相关题目。' 
        }
      ]
    }
    
    Object.assign(studentData, data)
    studentsStore.setStudentDetails(studentId.value, data)
  } catch (error) {
    console.error('Failed to fetch student details', error)
  } finally {
    loading.value = false
  }
}

const initTrendChart = () => {
  const chart = echarts.init(trendChart.value)
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['学习指数', '完成度', '正确率'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '12%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: Array.from({length: 30}, (_, i) => `${i+1}日`)
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      interval: 20
    },
    series: [
      {
        name: '学习指数',
        type: 'line',
        data: generateTrendData(30, 85, 98),
        lineStyle: {
          color: '#409EFF'
        }
      },
      {
        name: '完成度',
        type: 'line',
        data: generateTrendData(30, 90, 100),
        lineStyle: {
          color: '#67C23A'
        }
      },
      {
        name: '正确率',
        type: 'line',
        data: generateTrendData(30, 80, 98),
        lineStyle: {
          color: '#E6A23C'
        }
      }
    ]
  }
  
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

const initKnowledgeChart = () => {
  const chart = echarts.init(knowledgeChart.value)
  
  const option = {
    tooltip: {
      trigger: 'item'
    },
    radar: {
      indicator: [
        { name: '细胞与分子', max: 100 },
        { name: '遗传与进化', max: 100 },
        { name: '生态与稳态', max: 100 },
        { name: '生命活动调节', max: 100 },
        { name: '实验与探究', max: 100 },
        { name: '综合应用', max: 100 }
      ]
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: [95, 80, 85, 90, 88, 92],
            name: '知识点掌握程度',
            areaStyle: {
              color: 'rgba(64, 158, 255, 0.6)'
            }
          },
          {
            value: [80, 70, 75, 78, 72, 80],
            name: '班级平均',
            areaStyle: {
              color: 'rgba(144, 147, 153, 0.3)'
            }
          }
        ]
      }
    ]
  }
  
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

const initTimeStatsChart = () => {
  const chart = echarts.init(timeStatsChart.value)
  
  const days = timeRange.value === 'week' ? 7 : timeRange.value === 'month' ? 30 : 120
  const dailyData = generateDailyTimeData(days)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        const data = params[0]
        return `${data.name}<br/>${data.seriesName}: ${data.value} 分钟`
      }
    },
    xAxis: {
      type: 'category',
      data: dailyData.dates,
      axisLabel: {
        interval: timeRange.value === 'week' ? 0 : 'auto'
      }
    },
    yAxis: {
      type: 'value',
      name: '学习时间（分钟）'
    },
    series: [
      {
        name: '学习时间',
        type: 'bar',
        data: dailyData.times,
        itemStyle: {
          color: function(params) {
            const value = params.value
            if (value < 60) return '#F56C6C'
            if (value < 120) return '#E6A23C'
            return '#67C23A'
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

// 生成模拟学习趋势数据
const generateTrendData = (days, min, max) => {
  return Array.from({length: days}, () => {
    return Math.floor(Math.random() * (max - min + 1) + min)
  })
}

// 生成模拟每日学习时间数据
const generateDailyTimeData = (days) => {
  const dates = []
  const times = []
  const today = new Date()
  
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    
    const month = date.getMonth() + 1
    const day = date.getDate()
    dates.push(`${month}/${day}`)
    
    // 生成30-180分钟之间的随机学习时间
    times.push(Math.floor(Math.random() * 150 + 30))
  }
  
  return { dates, times }
}

watch(timeRange, () => {
  initTimeStatsChart()
})

onMounted(() => {
  fetchStudentData()
  initTrendChart()
  initKnowledgeChart()
  initTimeStatsChart()
})
</script>

<style scoped>
.student-detail-container {
  padding: 20px;
}

.header-actions {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-start;
}

.loading {
  padding: 20px;
}

.info-card {
  margin-bottom: 20px;
}

.student-info {
  display: flex;
  align-items: center;
}

.avatar-container {
  margin-right: 20px;
}

.info-details {
  flex: 1;
}

.info-details h2 {
  margin-top: 0;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.info-details h2 .el-tag {
  margin-left: 10px;
}

.info-details p {
  color: #606266;
  margin-bottom: 10px;
}

.ranking-badge {
  display: inline-block;
  background-color: #f0f9eb;
  border: 1px solid #e1f3d8;
  border-radius: 4px;
  padding: 5px 12px;
}

.rank-label {
  color: #67C23A;
  margin-right: 5px;
}

.rank-value {
  font-weight: bold;
  color: #67C23A;
}

.metric-cards {
  margin-bottom: 20px;
}

.metric-card {
  text-align: center;
  padding: 20px 0;
}

.metric-title {
  font-size: 16px;
  margin-bottom: 15px;
  color: #303133;
}

.metric-chart {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

.metric-comparison {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 12px;
}

.comparison {
  font-weight: bold;
}

.comparison.better {
  color: #67C23A;
}

.comparison.worse {
  color: #F56C6C;
}

.comparison.same {
  color: #909399;
}

.chart-section {
  margin-bottom: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-title {
  font-size: 16px;
  font-weight: bold;
}

.time-stats-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recommendation-card {
  margin-bottom: 20px;
}

.card-title {
  font-size: 16px;
  font-weight: bold;
}

.recommendations {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.recommendation-item {
  display: flex;
  padding: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.recommendation-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #fdf6ec;
  color: #e6a23c;
  margin-right: 10px;
}

.recommendation-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #303133;
}

.recommendation-desc {
  font-size: 12px;
  color: #606266;
  line-height: 1.5;
}
</style> 