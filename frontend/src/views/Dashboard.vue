<template>
  <div class="dashboard-container">
    <h1 class="page-title">学情监控</h1>

    <!-- 统计卡片区域 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6" v-for="(stat, index) in statsData" :key="index">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-title">{{ stat.title }}</div>
            <div class="stat-trend" :class="{ 'up': stat.trend > 0, 'down': stat.trend < 0 }">
              {{ stat.trend > 0 ? '↑' : '↓' }} {{ Math.abs(stat.trend) }}%
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 学生排名区域 -->
    <div class="ranking-section">
      <h2 class="section-title">学习指数加权排名</h2>
      <el-table
        :data="rankings"
        style="width: 100%"
        :row-class-name="tableRowClassName"
        @row-click="handleRowClick"
      >
        <el-table-column prop="rank" label="排名" width="80" align="center" />
        <el-table-column prop="name" label="学生姓名" width="120" />
        <el-table-column prop="class" label="班级" width="120" />
        <el-table-column prop="score" label="学习指数" width="120" >
          <template #default="scope">
            <span class="score">{{ scope.row.score }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="completionRate" label="完成度" width="200">
          <template #default="scope">
            <el-progress 
              :percentage="scope.row.completionRate" 
              :color="getColorByPercentage(scope.row.completionRate)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="accuracyRate" label="正确率" width="200">
          <template #default="scope">
            <el-progress 
              :percentage="scope.row.accuracyRate" 
              :color="getColorByPercentage(scope.row.accuracyRate)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="trend" label="趋势" width="100">
          <template #default="scope">
            <span :class="scope.row.trend >= 0 ? 'trend-up' : 'trend-down'">
              {{ scope.row.trend >= 0 ? '↑' : '↓' }} {{ Math.abs(scope.row.trend) }}%
            </span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 整体学情概览图表 -->
    <div class="charts-section">
      <h2 class="section-title">整体学情概览</h2>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="chart-container">
            <div ref="scoreDistributionChart" style="width: 100%; height: 350px;"></div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="chart-container">
            <div ref="subjectPerformanceChart" style="width: 100%; height: 350px;"></div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStudentsStore } from '../store'
import { studentsApi } from '../api'
import * as echarts from 'echarts'

const router = useRouter()
const studentsStore = useStudentsStore()
const scoreDistributionChart = ref(null)
const subjectPerformanceChart = ref(null)

const statsData = ref([
  { title: '总学生数', value: 182, trend: 5 },
  { title: '平均学习指数', value: 78.5, trend: 3.2 },
  { title: '作业完成率', value: '86%', trend: 2.5 },
  { title: '平均正确率', value: '73%', trend: -1.8 }
])

const rankings = ref([])

const getColorByPercentage = (percentage) => {
  if (percentage < 60) return '#F56C6C'
  if (percentage < 80) return '#E6A23C'
  return '#67C23A'
}

const tableRowClassName = ({ row }) => {
  if (row.rank <= 3) return 'top-ranking-row'
  return ''
}

const handleRowClick = (row) => {
  router.push(`/student/${row.id}`)
}

const initScoreDistributionChart = () => {
  const chartInstance = echarts.init(scoreDistributionChart.value)
  
  const option = {
    title: {
      text: '学习指数分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['0-60', '60-70', '70-80', '80-90', '90-100']
    },
    yAxis: {
      type: 'value',
      name: '学生数'
    },
    series: [
      {
        data: [12, 28, 45, 68, 29],
        type: 'bar',
        color: '#409EFF'
      }
    ]
  }
  
  chartInstance.setOption(option)
  window.addEventListener('resize', () => {
    chartInstance.resize()
  })
}

const initSubjectPerformanceChart = () => {
  const chartInstance = echarts.init(subjectPerformanceChart.value)
  
  const option = {
    title: {
      text: '生物各领域表现',
      left: 'center'
    },
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
            value: [85, 78, 82, 75, 80, 88],
            name: '班级平均',
            areaStyle: {
              color: 'rgba(64, 158, 255, 0.6)'
            }
          }
        ]
      }
    ]
  }
  
  chartInstance.setOption(option)
  window.addEventListener('resize', () => {
    chartInstance.resize()
  })
}

const fetchRankings = async () => {
  try {
    // 模拟数据 - 实际应该从API获取
    const data = [
      { id: 1, rank: 1, name: '张三', class: '高三(1)班', score: 95.8, completionRate: 98, accuracyRate: 96, trend: 2.5 },
      { id: 2, rank: 2, name: '李四', class: '高三(2)班', score: 93.2, completionRate: 95, accuracyRate: 94, trend: 1.8 },
      { id: 3, rank: 3, name: '王五', class: '高三(1)班', score: 91.5, completionRate: 93, accuracyRate: 92, trend: 3.2 },
      { id: 4, rank: 4, name: '赵六', class: '高三(3)班', score: 88.7, completionRate: 90, accuracyRate: 89, trend: -0.5 },
      { id: 5, rank: 5, name: '钱七', class: '高三(2)班', score: 87.3, completionRate: 88, accuracyRate: 86, trend: 1.2 },
      { id: 6, rank: 6, name: '孙八', class: '高三(1)班', score: 85.6, completionRate: 87, accuracyRate: 84, trend: -1.0 },
      { id: 7, rank: 7, name: '周九', class: '高三(3)班', score: 82.9, completionRate: 85, accuracyRate: 81, trend: 0.8 },
      { id: 8, rank: 8, name: '吴十', class: '高三(2)班', score: 81.4, completionRate: 83, accuracyRate: 80, trend: -0.3 },
      { id: 9, rank: 9, name: '郑十一', class: '高三(1)班', score: 79.8, completionRate: 81, accuracyRate: 78, trend: 1.5 },
      { id: 10, rank: 10, name: '王十二', class: '高三(3)班', score: 78.2, completionRate: 79, accuracyRate: 77, trend: -0.7 }
    ]
    
    rankings.value = data
    studentsStore.setRankings(data)
    
    // 实际API调用 (现在先注释掉)
    /*
    const response = await studentsApi.getRankings()
    rankings.value = response.data
    studentsStore.setRankings(response.data)
    */
  } catch (error) {
    console.error('Failed to fetch rankings', error)
  }
}

onMounted(() => {
  fetchRankings()
  
  // 初始化图表
  initScoreDistributionChart()
  initSubjectPerformanceChart()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 600;
  color: #333;
}

.stats-cards {
  margin-bottom: 30px;
}

.stat-card {
  text-align: center;
  padding: 10px 0;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-title {
  font-size: 14px;
  color: #999;
  margin-bottom: 5px;
}

.stat-trend {
  font-size: 12px;
  margin-top: 5px;
}

.stat-trend.up {
  color: #67C23A;
}

.stat-trend.down {
  color: #F56C6C;
}

.section-title {
  font-size: 18px;
  margin-bottom: 15px;
  font-weight: 500;
  color: #333;
}

.ranking-section {
  margin-bottom: 30px;
}

.score {
  font-weight: bold;
  color: #409EFF;
}

.trend-up {
  color: #67C23A;
}

.trend-down {
  color: #F56C6C;
}

.charts-section {
  margin-bottom: 30px;
}

.chart-container {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.top-ranking-row {
  background-color: #fdf6ec;
  font-weight: bold;
}
</style> 