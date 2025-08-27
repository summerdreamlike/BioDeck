<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h1 class="page-title">学情监控</h1>
      <div class="class-info" v-if="currentTeacher">
        <el-tag type="primary" size="large" v-if="teacherClassId">
          <el-icon><el-icon-school /></el-icon>
          班级 {{ teacherClassId }}
        </el-tag>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-cards">
      <el-row :gutter="20" justify="center">
        <el-col :xs="24" :sm="12" :md="8" v-for="(stat, index) in statsData" :key="stat.title">
          <el-card 
            class="stat-card" 
            :class="{ 'clickable': index === 0 }"
            shadow="hover" 
            @click="index === 0 ? toggleStudentDetails() : null"
          >
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-title">{{ stat.title }}</div>
            <div class="stat-trend" :class="{ 'up': stat.trend > 0, 'down': stat.trend < 0 }">
              {{ stat.trend > 0 ? '↑' : '↓' }} {{ Math.abs(stat.trend) }}%
            </div>
            <div v-if="index === 0" class="click-hint">
              <el-icon><el-icon-arrow-down /></el-icon>
              <span>点击查看详情</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 学生详情展开区域 -->
    <transition name="slideDown">
      <div v-if="showStudentDetails" class="student-details">
        <div class="details-header">
          <h3>
            学生详情
            <span v-if="teacherClassId" class="class-name">- 班级 {{ teacherClassId }}</span>
          </h3>
          <el-button type="text" @click="toggleStudentDetails">
            <el-icon><el-icon-close /></el-icon>
          </el-button>
        </div>
        <el-table :data="studentList" v-loading="loading.students" stripe>
          <el-table-column prop="name" label="姓名" width="300%" />
          <el-table-column prop="student_id" label="学号" width="350%" />
          <el-table-column prop="completion_rate" label="关卡完成情况" width="350%" sortable>
            <template #default="{ row }">
              <el-tag :type="getCompletionType(row.completion_rate)">
                {{ row.completion_rate }}%
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="accuracy_rate" label="关卡正确率" width="400%" sortable>
            <template #default="{ row }">
              <el-tag :type="getAccuracyType(row.accuracy_rate)">
                {{ row.accuracy_rate }}%
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="最近作业" width="350%">
            <template #default="{ row }">
              <span v-if="row.last_task">{{ row.last_task }}</span>
              <span v-else class="text-muted">暂无</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </transition>

    <!-- 整体学情概览图表 -->
    <div class="charts-section">
      <h2 class="section-title">整体学情概览</h2>
      <el-row :gutter="20">
        <el-col :xs="24" :md="12">
          <div class="chart-container">
            <div ref="scoreDistributionChart" class="chart"></div>
          </div>
        </el-col>
        <el-col :xs="24" :md="12">
          <div class="chart-container">
            <div ref="subjectPerformanceChart" class="chart"></div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import * as echarts from 'echarts'
import { studentsApi } from '../api'
import { useUserStore } from '../store'


const scoreDistributionChart = ref(null)
const subjectPerformanceChart = ref(null)
const userStore = useUserStore()


const loading = reactive({ overview: false, charts: false, students: false })
const showStudentDetails = ref(false)
const studentList = ref([])


// 获取当前教师的班级信息
const currentTeacher = computed(() => userStore.getUserInfo)
const teacherClassId = computed(() => currentTeacher.value?.class_number || null)

const statsData = ref([
  { title: '学生总人数', value: 30, trend: 0 },
  { title: '关卡完成率', value: '86%', trend: 2.5 },
  { title: '关卡正确率', value: '73%', trend: -1.8 }
])

const initScoreDistributionChart = (data) => {
  const chartInstance = echarts.init(scoreDistributionChart.value)
  const option = {
    title: { text: '学习指数分布', left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: (data && data.buckets) || ['0-60', '60-70', '70-80', '80-90', '90-100'] },
    yAxis: { type: 'value', name: '学生数' },
    series: [{ data: (data && data.values) || [12, 28, 45, 68, 29], type: 'bar', color: '#409EFF', itemStyle: { borderRadius: [4,4,0,0] } }],
    animationDuration: 600,
    animationEasing: 'cubicOut'
  }
  chartInstance.setOption(option)
  window.addEventListener('resize', () => chartInstance.resize())
}

const initSubjectPerformanceChart = (data) => {
  const chartInstance = echarts.init(subjectPerformanceChart.value)
  const option = {
    title: { text: '生物各领域表现', left: 'center' },
    tooltip: { trigger: 'item' },
    radar: {
      indicator: (data && data.indicator) || [
        { name: '细胞与分子', max: 100 },
        { name: '遗传与进化', max: 100 },
        { name: '生态与稳态', max: 100 },
        { name: '生命活动调节', max: 100 },
        { name: '实验与探究', max: 100 },
        { name: '综合应用', max: 100 }
      ]
    },
    series: [{ type: 'radar', data: [{ value: (data && data.values) || [85, 78, 82, 75, 80, 88], name: '班级平均', areaStyle: { color: 'rgba(64, 158, 255, 0.6)' } }] }],
    animationDuration: 600,
    animationEasing: 'cubicOut'
  }
  chartInstance.setOption(option)
  window.addEventListener('resize', () => chartInstance.resize())
}

async function loadOverview() {
  loading.overview = true
  
  try {
    // 调用后端接口获取学生数据
    const studentsRes = await studentsApi.getStudents()
    const allStudents = studentsRes?.data || studentsRes || []
    
    // 根据教师班级筛选学生
    let classStudents = allStudents
    if (teacherClassId.value) {
      classStudents = allStudents.filter(student => 
        student.class_number === teacherClassId.value || 
        student.class_id === teacherClassId.value ||
        student.class === teacherClassId.value
      )
    }
    
    const totalStudents = classStudents.length
    
    // 模拟作业完成率和正确率数据（后续可以连接真实接口）
    const homeworkCompletion = Math.floor(Math.random() * 20 + 75) // 75-95%
    const avgAccuracy = Math.floor(Math.random() * 15 + 70) // 70-85%
    
    const newStatsData = [
      { title: '学生总人数', value: totalStudents, trend: 5 },
      { title: '关卡完成率', value: `${homeworkCompletion}%`, trend: 2.5 },
      { title: '关卡正确率', value: `${avgAccuracy}%`, trend: -1.8 }
    ]
    
    statsData.value = newStatsData
    
    // 生成学生详情数据
    generateStudentDetails(classStudents)
    
  } catch (e) {
    console.error('加载概览数据失败:', e)
    // 失败则使用默认模拟数据
    statsData.value = [
      { title: '学生总人数', value: 30, trend: 5 },
      { title: '作业完成率', value: '86%', trend: 2.5 },
      { title: '作业正确率', value: '73%', trend: -1.8 }
    ]
  } finally {
    loading.overview = false
  }
}



function generateStudentDetails(students) {
  const studentDetails = []
  
  students.forEach((student, index) => {
    studentDetails.push({
      id: student.id,
      name: student.name || student.username || `学生${index + 1}`,
      student_id: student.student_id || student.id_number || `1001${(index + 1).toString().padStart(3, '0')}`,
      completion_rate: Math.floor(Math.random() * 30 + 70), // 70-100% 模拟数据
      accuracy_rate: Math.floor(Math.random() * 25 + 65),   // 65-90% 模拟数据
      last_task: `作业${Math.floor(Math.random() * 10 + 1)}`
    })
  })
  
  // 默认排序：先按关卡完成情况降序，再按关卡正确率降序
  studentList.value = studentDetails
    .sort((a, b) => {
      if (b.completion_rate !== a.completion_rate) {
        return b.completion_rate - a.completion_rate
      }
      return b.accuracy_rate - a.accuracy_rate
    })
  return studentDetails
}

async function loadCharts() {
  loading.charts = true
  try {
    // 模拟数据加载延迟
    await new Promise(resolve => setTimeout(resolve, 600))
    
    // 直接使用模拟数据初始化图表
    initScoreDistributionChart()
    initSubjectPerformanceChart()
  } catch (e) {
    console.error('加载图表数据失败:', e)
    initScoreDistributionChart()
    initSubjectPerformanceChart()
  } finally {
    loading.charts = false
  }
}

function refreshAll() {
  loadOverview()
  loadCharts()
}

function toggleStudentDetails() {
  showStudentDetails.value = !showStudentDetails.value
}



function getCompletionType(rate) {
  if (rate >= 90) return 'success'
  if (rate >= 70) return 'warning'
  return 'danger'
}

function getAccuracyType(rate) {
  if (rate >= 85) return 'success'
  if (rate >= 70) return 'warning'
  return 'danger'
}





onMounted(() => {
  refreshAll()
})
</script>

<style scoped>
.dashboard-container { padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.page-title { font-size: 24px; font-weight: 600; color: #333; margin: 0; }
.class-info { display: flex; gap: 8px; align-items: center; }
.filters { margin-bottom: 16px; }
.stats-cards { margin-bottom: 30px; }
.stat-card { text-align: center; padding: 14px 8px; }
.stat-value { font-size: 28px; font-weight: bold; color: #409EFF; margin-bottom: 5px; }
.stat-title { font-size: 14px; color: #999; margin-bottom: 5px; }
.stat-trend { font-size: 12px; margin-top: 5px; }
.stat-trend.up { color: #67C23A; }
.stat-trend.down { color: #F56C6C; }
.section-title { font-size: 18px; margin-bottom: 15px; font-weight: 500; color: #333; }
.charts-section { margin-bottom: 30px; }
.chart-container { background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 8px 24px rgba(64, 158, 255, 0.08), 0 2px 6px rgba(0,0,0,0.06); transition: transform .25s cubic-bezier(.2,.8,.2,1), box-shadow .25s cubic-bezier(.2,.8,.2,1); }
.chart-container:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(64, 158, 255, 0.12), 0 4px 10px rgba(0,0,0,0.08); }
.chart { width: 100%; height: 360px; }

/* 骨架屏 */
.skeleton { background: linear-gradient(90deg, #f2f6fc 25%, #eef2f7 37%, #f2f6fc 63%); border-radius: 6px; background-size: 400% 100%; animation: shimmer 1.4s ease infinite; margin: 6px auto; }
.skeleton.value { width: 60%; height: 28px; }
.skeleton.title { width: 40%; height: 14px; }
.skeleton.small { width: 30%; height: 12px; }
@keyframes shimmer { 0% { background-position: 100% 0; } 100% { background-position: -100% 0; } }

/* 卡片淡入 */
.cardFade-enter-active { transition: all .35s cubic-bezier(.2,.8,.2,1); }
.cardFade-leave-active { transition: all .2s cubic-bezier(.2,.8,.2,1); }
.cardFade-enter-from, .cardFade-leave-to { opacity: 0; transform: translateY(6px); }

/* 可点击卡片样式 */
.stat-card.clickable { cursor: pointer; position: relative; }
.stat-card.clickable:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(64, 158, 255, 0.15); }
.click-hint { position: absolute; bottom: 8px; right: 12px; display: flex; align-items: center; gap: 4px; font-size: 11px; color: #409EFF; opacity: 0.8; }

/* 学生详情展开区域 */
.student-details { 
  margin: 20px 0; 
  background: #fff; 
  border-radius: 12px; 
  box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
  overflow: hidden;
}
.details-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 16px 20px; 
  background: linear-gradient(135deg, #f8fafc, #e2e8f0); 
  border-bottom: 1px solid #e2e8f0;
}
.details-header h3 { margin: 0; color: #2d3748; font-size: 16px; font-weight: 600; }
.class-name { color: #409EFF; font-weight: 500; }

/* 下滑展开动画 */
.slideDown-enter-active { transition: all .4s cubic-bezier(.2,.8,.2,1); }
.slideDown-leave-active { transition: all .3s cubic-bezier(.2,.8,.2,1); }
.slideDown-enter-from, .slideDown-leave-to { opacity: 0; transform: translateY(-20px); max-height: 0; }
.slideDown-enter-to, .slideDown-leave-from { opacity: 1; transform: translateY(0); max-height: 500px; }

/* 表格样式优化 */
:deep(.el-table) { border-radius: 0; }
:deep(.el-table th) { background: #f8fafc; color: #4a5568; font-weight: 600; }
:deep(.el-table td) { border-bottom: 1px solid #e2e8f0; }
.text-muted { color: #a0aec0; font-style: italic; }
</style> 