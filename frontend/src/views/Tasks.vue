<template>
  <div class="tasks-container">
    <h1 class="page-title">任务发布</h1>
    
    <div class="tasks-header">
      <el-button type="primary" @click="openNewTaskDialog">
        <el-icon><el-icon-plus /></el-icon>
        发布新任务
      </el-button>
      
      <div class="filter-container">
        <el-select v-model="filterStatus" placeholder="任务状态" clearable @change="filterTasks">
          <el-option label="全部" value="" />
          <el-option label="进行中" value="ongoing" />
          <el-option label="已截止" value="ended" />
        </el-select>
        
        <el-select v-model="filterClass" placeholder="班级" clearable @change="filterTasks">
          <el-option label="全部" value="" />
          <el-option v-for="cls in classes" :key="cls" :label="cls" :value="cls" />
        </el-select>
        
        <el-input
          v-model="searchQuery"
          placeholder="搜索任务"
          prefix-icon="el-icon-search"
          clearable
          style="width: 250px"
          @input="filterTasks"
        />
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="filteredTasks.length === 0" class="empty-container">
      <el-empty description="暂无任务" />
    </div>
    
    <div v-else class="tasks-list">
      <div v-for="task in filteredTasks" :key="task.id" class="task-card">
        <el-card>
          <template #header>
            <div class="task-header">
              <div class="task-title">
                {{ task.title }}
                <el-tag :type="getStatusTagType(task)" size="small" class="task-status">
                  {{ getStatusText(task) }}
                </el-tag>
              </div>
              <div class="task-actions">
                <el-dropdown @command="(cmd) => handleCommand(cmd, task)">
                  <el-button size="small" type="primary" plain>
                    操作
                    <el-icon class="el-icon--right"><el-icon-arrow-down /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="view">查看详情</el-dropdown-item>
                      <el-dropdown-item command="edit">编辑</el-dropdown-item>
                      <el-dropdown-item command="statistics">统计分析</el-dropdown-item>
                      <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </template>
          
          <div class="task-info">
            <div class="task-meta">
              <div class="meta-item">
                <span class="label">截止日期:</span>
                <span :class="isExpired(task) ? 'value expired' : 'value'">{{ formatDate(task.due_date) }}</span>
              </div>
              <div class="meta-item">
                <span class="label">适用班级:</span>
                <span class="value">{{ task.classes.join(', ') }}</span>
              </div>
              <div class="meta-item">
                <span class="label">发布时间:</span>
                <span class="value">{{ formatDate(task.created_at) }}</span>
              </div>
            </div>
            
            <div class="task-progress">
              <div class="progress-header">
                <span>完成进度</span>
                <span>{{ task.submitted }}/{{ task.total_students }}</span>
              </div>
              <el-progress 
                :percentage="task.completion_rate" 
                :color="getProgressColor(task.completion_rate)"
                :format="percentageFormat"
                :stroke-width="10"
              />
            </div>
            
            <div class="task-description">{{ task.description }}</div>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 新任务对话框 -->
    <el-dialog
      v-model="newTaskDialogVisible"
      :title="isEditMode ? '编辑任务' : '发布新任务'"
      width="600px"
    >
      <el-form :model="taskForm" label-width="100px">
        <el-form-item label="任务标题">
          <el-input v-model="taskForm.title" placeholder="请输入任务标题" />
        </el-form-item>
        
        <el-form-item label="截止日期">
          <el-date-picker
            v-model="taskForm.due_date"
            type="datetime"
            placeholder="选择截止日期"
            format="YYYY-MM-DD HH:mm"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="适用班级">
          <el-select
            v-model="taskForm.classes"
            multiple
            collapse-tags
            placeholder="请选择班级"
            style="width: 100%"
          >
            <el-option
              v-for="cls in classes"
              :key="cls"
              :label="cls"
              :value="cls"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="任务类型">
          <el-radio-group v-model="taskForm.type">
            <el-radio label="homework">作业</el-radio>
            <el-radio label="exam">考试</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="关联试卷" v-if="taskForm.type === 'exam'">
          <el-select v-model="taskForm.paper_id" placeholder="请选择试卷" style="width: 100%">
            <el-option
              v-for="paper in papers"
              :key="paper.id"
              :label="paper.name"
              :value="paper.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="补交设置">
          <el-switch
            v-model="taskForm.allow_late_submission"
            active-text="允许补交"
            inactive-text="不允许补交"
          />
        </el-form-item>
        
        <el-form-item label="任务描述">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            rows="4"
            placeholder="请输入任务描述"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="newTaskDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitTask">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 统计分析对话框 -->
    <el-dialog
      v-model="statisticsDialogVisible"
      :title="`${currentTask.title} - 统计分析`"
      width="70%"
      class="statistics-dialog"
    >
      <div v-if="currentTask" class="statistics-container">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card class="statistics-card">
              <template #header>
                <div class="card-header">
                  <span>基本统计</span>
                </div>
              </template>
              
              <div class="statistics-info">
                <div class="stat-item large">
                  <div class="stat-value">{{ currentTask.completion_rate }}%</div>
                  <div class="stat-label">完成率</div>
                </div>
                
                <div class="stat-item">
                  <div class="stat-value">{{ currentTask.submitted }}</div>
                  <div class="stat-label">已提交</div>
                </div>
                
                <div class="stat-item">
                  <div class="stat-value">{{ currentTask.total_students - currentTask.submitted }}</div>
                  <div class="stat-label">未提交</div>
                </div>
                
                <div class="stat-item">
                  <div class="stat-value">{{ currentTask.avg_score || '暂无' }}</div>
                  <div class="stat-label">平均分</div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="12">
            <el-card class="statistics-card">
              <template #header>
                <div class="card-header">
                  <span>分数分布</span>
                </div>
              </template>
              
              <div class="chart-container">
                <div ref="scoreDistributionChart" style="height: 250px"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :span="24">
            <el-card class="statistics-card">
              <template #header>
                <div class="card-header">
                  <span>提交时间分布</span>
                </div>
              </template>
              
              <div class="chart-container">
                <div ref="timeDistributionChart" style="height: 300px"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :span="24">
            <el-card class="statistics-card">
              <template #header>
                <div class="card-header">
                  <span>学生提交情况</span>
                  <div class="export-actions">
                    <el-button size="small" @click="exportSubmissions('excel')">
                      <el-icon><el-icon-document /></el-icon>
                      导出Excel
                    </el-button>
                  </div>
                </div>
              </template>
              
              <el-table :data="currentTask.submissions || []" style="width: 100%">
                <el-table-column prop="student_name" label="学生姓名" width="120" />
                <el-table-column prop="student_number" label="学号" width="120" />
                <el-table-column prop="score" label="分数" width="120">
                  <template #default="scope">
                    <span v-if="scope.row.score !== null">{{ scope.row.score }}</span>
                    <span v-else class="no-score">未评分</span>
                  </template>
                </el-table-column>
                <el-table-column prop="submitted_at" label="提交时间" width="180">
                  <template #default="scope">
                    <span v-if="scope.row.submitted_at">{{ formatDateTime(scope.row.submitted_at) }}</span>
                    <span v-else class="no-submission">未提交</span>
                  </template>
                </el-table-column>
                <el-table-column label="提交状态" width="120">
                  <template #default="scope">
                    <el-tag v-if="scope.row.submitted_at" :type="isLateSubmission(scope.row, currentTask) ? 'warning' : 'success'">
                      {{ isLateSubmission(scope.row, currentTask) ? '逾期提交' : '按时提交' }}
                    </el-tag>
                    <el-tag v-else type="danger">未提交</el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="120">
                  <template #default="scope">
                    <el-button size="small" @click="viewSubmission(scope.row)" :disabled="!scope.row.submitted_at">
                      查看
                    </el-button>
                    <el-button size="small" type="primary" @click="gradeSubmission(scope.row)" :disabled="!scope.row.submitted_at">
                      评分
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { tasksApi } from '../api'

// 状态变量
const loading = ref(false)
const newTaskDialogVisible = ref(false)
const statisticsDialogVisible = ref(false)
const isEditMode = ref(false)
const currentTask = ref(null)
const filterStatus = ref('')
const filterClass = ref('')
const searchQuery = ref('')
const scoreDistributionChart = ref(null)
const timeDistributionChart = ref(null)

// 任务列表数据
const tasks = ref([])

// 表单数据
const taskForm = reactive({
  title: '',
  description: '',
  due_date: '',
  type: 'homework',
  paper_id: null,
  classes: [],
  allow_late_submission: false
})

// 模拟数据 - 班级列表
const classes = ref([
  '高三(1)班',
  '高三(2)班',
  '高三(3)班',
  '高三(4)班',
  '高三(5)班'
])

// 模拟数据 - 试卷列表
const papers = ref([
  { id: 1, name: '高三生物期中测试' },
  { id: 2, name: '高三生物遗传与变异专题' },
  { id: 3, name: '高三生物生态系统专题' },
  { id: 4, name: '高三生物细胞与分子综合' }
])

// 计算属性
const filteredTasks = computed(() => {
  let result = [...tasks.value]
  
  // 按状态筛选
  if (filterStatus.value === 'ongoing') {
    result = result.filter(task => !isExpired(task))
  } else if (filterStatus.value === 'ended') {
    result = result.filter(task => isExpired(task))
  }
  
  // 按班级筛选
  if (filterClass.value) {
    result = result.filter(task => task.classes.includes(filterClass.value))
  }
  
  // 按搜索词筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(task => 
      task.title.toLowerCase().includes(query) || 
      task.description.toLowerCase().includes(query)
    )
  }
  
  return result
})

// 方法
const filterTasks = () => {
  // 通过计算属性自动筛选
}

const isExpired = (task) => {
  return new Date(task.due_date) < new Date()
}

const isLateSubmission = (submission, task) => {
  return new Date(submission.submitted_at) > new Date(task.due_date)
}

const getStatusTagType = (task) => {
  if (isExpired(task)) {
    return task.completion_rate === 100 ? 'success' : 'info'
  } else {
    return 'primary'
  }
}

const getStatusText = (task) => {
  if (isExpired(task)) {
    return '已截止'
  } else {
    return '进行中'
  }
}

const getProgressColor = (percentage) => {
  if (percentage < 30) return '#F56C6C'
  if (percentage < 70) return '#E6A23C'
  return '#67C23A'
}

const percentageFormat = (percentage) => {
  return `${percentage}%`
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
}

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return `${formatDate(dateString)} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const handleCommand = (command, task) => {
  switch (command) {
    case 'view':
      // 查看任务详情
      break
    case 'edit':
      editTask(task)
      break
    case 'statistics':
      viewStatistics(task)
      break
    case 'delete':
      deleteTask(task)
      break
  }
}

const openNewTaskDialog = () => {
  isEditMode.value = false
  
  // 重置表单
  Object.assign(taskForm, {
    title: '',
    description: '',
    due_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 默认一周后截止
    type: 'homework',
    paper_id: null,
    classes: [],
    allow_late_submission: false
  })
  
  newTaskDialogVisible.value = true
}

const editTask = (task) => {
  isEditMode.value = true
  
  // 填充表单
  Object.assign(taskForm, {
    id: task.id,
    title: task.title,
    description: task.description,
    due_date: new Date(task.due_date),
    type: task.type || 'homework',
    paper_id: task.paper_id,
    classes: [...task.classes],
    allow_late_submission: task.allow_late_submission
  })
  
  newTaskDialogVisible.value = true
}

const submitTask = () => {
  if (!taskForm.title) {
    alert('请输入任务标题')
    return
  }
  
  if (!taskForm.due_date) {
    alert('请选择截止日期')
    return
  }
  
  if (taskForm.classes.length === 0) {
    alert('请选择适用班级')
    return
  }
  
  if (taskForm.type === 'exam' && !taskForm.paper_id) {
    alert('请选择关联试卷')
    return
  }
  
  // 模拟保存任务
  if (isEditMode.value) {
    // 更新任务
    const index = tasks.value.findIndex(t => t.id === taskForm.id)
    if (index !== -1) {
      const updatedTask = {
        ...tasks.value[index],
        title: taskForm.title,
        description: taskForm.description,
        due_date: taskForm.due_date.toISOString(),
        type: taskForm.type,
        paper_id: taskForm.paper_id,
        classes: [...taskForm.classes],
        allow_late_submission: taskForm.allow_late_submission
      }
      
      tasks.value.splice(index, 1, updatedTask)
    }
  } else {
    // 新建任务
    const newTask = {
      id: Date.now(),
      title: taskForm.title,
      description: taskForm.description,
      due_date: taskForm.due_date.toISOString(),
      type: taskForm.type,
      paper_id: taskForm.paper_id,
      classes: [...taskForm.classes],
      allow_late_submission: taskForm.allow_late_submission,
      created_at: new Date().toISOString(),
      total_students: 30 + Math.floor(Math.random() * 20), // 模拟数据
      submitted: Math.floor(Math.random() * 40), // 模拟数据
      completion_rate: Math.floor(Math.random() * 100), // 模拟数据
      avg_score: Math.floor(Math.random() * 30) + 70 // 模拟数据
    }
    
    // 确保提交人数不超过总人数
    newTask.submitted = Math.min(newTask.submitted, newTask.total_students)
    newTask.completion_rate = Math.round((newTask.submitted / newTask.total_students) * 100)
    
    tasks.value.unshift(newTask)
  }
  
  newTaskDialogVisible.value = false
}

const deleteTask = (task) => {
  if (confirm(`确定要删除任务"${task.title}"吗？`)) {
    const index = tasks.value.findIndex(t => t.id === task.id)
    if (index !== -1) {
      tasks.value.splice(index, 1)
    }
  }
}

const viewStatistics = (task) => {
  currentTask.value = task
  statisticsDialogVisible.value = true
  
  // 添加模拟提交数据（如果没有）
  if (!currentTask.value.submissions) {
    generateMockSubmissions(currentTask.value)
  }
  
  // 等待DOM渲染完成后初始化图表
  setTimeout(() => {
    initScoreDistributionChart()
    initTimeDistributionChart()
  }, 100)
}

const generateMockSubmissions = (task) => {
  const submissions = []
  const studentNames = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十']
  const totalStudents = task.total_students
  const submittedCount = task.submitted
  
  for (let i = 0; i < totalStudents; i++) {
    const isSubmitted = i < submittedCount
    const dueDate = new Date(task.due_date)
    const createdDate = new Date(task.created_at)
    
    // 生成提交时间（可能在截止日期之前或之后）
    let submittedAt = null
    if (isSubmitted) {
      const timeDiff = dueDate - createdDate
      const randomTime = Math.random() * timeDiff * 1.2 // 可能超过截止日期
      submittedAt = new Date(createdDate.getTime() + randomTime)
    }
    
    submissions.push({
      student_name: studentNames[i % studentNames.length] + (Math.floor(i / studentNames.length) + 1),
      student_number: `S2023${(10000 + i).toString().substring(1)}`,
      submitted_at: isSubmitted ? submittedAt.toISOString() : null,
      score: isSubmitted ? Math.floor(Math.random() * 40) + 60 : null // 60-100的随机分数
    })
  }
  
  currentTask.value.submissions = submissions
}

const initScoreDistributionChart = () => {
  if (!currentTask.value || !currentTask.value.submissions || !scoreDistributionChart.value) return
  
  const chart = echarts.init(scoreDistributionChart.value)
  
  // 计算分数分布
  const scoreRanges = [
    { min: 0, max: 60, label: '0-60' },
    { min: 60, max: 70, label: '60-70' },
    { min: 70, max: 80, label: '70-80' },
    { min: 80, max: 90, label: '80-90' },
    { min: 90, max: 100, label: '90-100' }
  ]
  
  const distribution = scoreRanges.map(range => {
    return {
      range: range.label,
      count: currentTask.value.submissions.filter(s => 
        s.score !== null && 
        s.score >= range.min && 
        s.score <= range.max
      ).length
    }
  })
  
  const option = {
    title: {
      text: '分数分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: distribution.map(item => item.range)
    },
    series: [
      {
        name: '分数分布',
        type: 'pie',
        radius: '70%',
        center: ['50%', '60%'],
        data: distribution.map(item => ({
          name: item.range,
          value: item.count
        })),
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

const initTimeDistributionChart = () => {
  if (!currentTask.value || !currentTask.value.submissions || !timeDistributionChart.value) return
  
  const chart = echarts.init(timeDistributionChart.value)
  
  const createdDate = new Date(currentTask.value.created_at)
  const dueDate = new Date(currentTask.value.due_date)
  const daysDiff = Math.ceil((dueDate - createdDate) / (24 * 60 * 60 * 1000))
  
  // 生成日期范围
  const dateRange = []
  for (let i = 0; i <= daysDiff; i++) {
    const date = new Date(createdDate)
    date.setDate(date.getDate() + i)
    dateRange.push(formatDate(date))
  }
  
  // 统计每天的提交数量
  const submissionCounts = dateRange.map(date => {
    return currentTask.value.submissions.filter(s => 
      s.submitted_at && formatDate(s.submitted_at) === date
    ).length
  })
  
  const option = {
    title: {
      text: '提交时间分布',
      left: 'center'
    },
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
      type: 'category',
      data: dateRange,
      axisLabel: {
        rotate: 45,
        interval: Math.ceil(dateRange.length / 10)
      }
    },
    yAxis: {
      type: 'value',
      name: '提交数量'
    },
    series: [{
      name: '提交数量',
      type: 'bar',
      data: submissionCounts,
      itemStyle: {
        color: function(params) {
          const date = new Date(dateRange[params.dataIndex])
          return date <= dueDate ? '#67C23A' : '#E6A23C'
        }
      },
      markLine: {
        data: [
          {
            name: '截止日期',
            xAxis: formatDate(dueDate)
          }
        ],
        lineStyle: {
          color: '#F56C6C',
          type: 'dashed'
        },
        label: {
          formatter: '截止日期',
          position: 'start'
        }
      }
    }]
  }
  
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

const exportSubmissions = (format) => {
  // 实际应用中，这里应该调用API导出数据
  alert(`正在导出${format === 'excel' ? 'Excel' : 'CSV'}文件...`)
}

const viewSubmission = (submission) => {
  // 查看提交详情
  alert(`查看${submission.student_name}的提交内容`)
}

const gradeSubmission = (submission) => {
  // 评分
  const score = prompt('请输入分数 (0-100):', submission.score || '')
  if (score !== null) {
    const numScore = parseFloat(score)
    if (!isNaN(numScore) && numScore >= 0 && numScore <= 100) {
      submission.score = numScore
      alert('评分已保存')
    } else {
      alert('请输入0-100之间的有效分数')
    }
  }
}

// 生成任务模拟数据
const generateMockTasks = () => {
  const mockTasks = []
  const taskTitles = [
    '高三生物细胞结构与功能练习',
    '高三生物遗传规律巩固',
    '高三生物生态系统案例分析',
    '高三生物实验报告撰写',
    '高三生物光合作用与呼吸作用对比'
  ]
  
  for (let i = 1; i <= 10; i++) {
    const createdAt = new Date()
    createdAt.setDate(createdAt.getDate() - Math.floor(Math.random() * 14))
    
    const dueDate = new Date(createdAt)
    dueDate.setDate(dueDate.getDate() + 3 + Math.floor(Math.random() * 10))
    
    const isHomework = Math.random() > 0.3
    const totalStudents = 30 + Math.floor(Math.random() * 20)
    const submitted = Math.floor(Math.random() * totalStudents)
    
    mockTasks.push({
      id: i,
      title: `${taskTitles[i % taskTitles.length]}${Math.ceil(i / taskTitles.length)}`,
      description: `这是${isHomework ? '作业' : '考试'}任务的详细描述，包含${isHomework ? '作业' : '考试'}要求和提交方式。`,
      due_date: dueDate.toISOString(),
      created_at: createdAt.toISOString(),
      type: isHomework ? 'homework' : 'exam',
      paper_id: isHomework ? null : (i % 4) + 1,
      classes: classes.value.slice(0, 1 + Math.floor(Math.random() * 3)),
      allow_late_submission: Math.random() > 0.5,
      total_students: totalStudents,
      submitted: submitted,
      completion_rate: Math.round((submitted / totalStudents) * 100),
      avg_score: Math.floor(Math.random() * 30) + 70
    })
  }
  
  return mockTasks
}

// 获取任务数据
const fetchTasks = async () => {
  loading.value = true
  
  try {
    // 模拟API调用
    setTimeout(() => {
      tasks.value = generateMockTasks()
      loading.value = false
    }, 500)
    
    // 实际API调用
    /*
    const response = await tasksApi.getTasks()
    tasks.value = response
    */
  } catch (error) {
    console.error('Failed to fetch tasks', error)
  } finally {
    loading.value = false
  }
}

// 监听对话框关闭
watch(statisticsDialogVisible, (newValue) => {
  if (!newValue) {
    // 对话框关闭后清除当前任务
    currentTask.value = null
  }
})

// 生命周期钩子
onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.tasks-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 600;
  color: #333;
}

.tasks-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-container {
  display: flex;
  gap: 10px;
}

.loading-container,
.empty-container {
  padding: 40px 0;
  text-align: center;
}

.tasks-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 20px;
}

.task-card {
  margin-bottom: 20px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-title {
  font-weight: bold;
  font-size: 16px;
  display: flex;
  align-items: center;
}

.task-status {
  margin-left: 10px;
}

.task-info {
  margin-top: 10px;
}

.task-meta {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 15px;
}

.meta-item {
  display: flex;
  flex-direction: column;
}

.label {
  color: #909399;
  font-size: 12px;
  margin-bottom: 5px;
}

.value {
  font-weight: 500;
}

.value.expired {
  color: #F56C6C;
}

.task-progress {
  margin-bottom: 15px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 14px;
  color: #606266;
}

.task-description {
  color: #606266;
  font-size: 14px;
  margin-top: 15px;
  white-space: pre-line;
}

.statistics-container {
  padding: 10px;
}

.statistics-info {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 10px;
  flex: 1;
  min-width: 80px;
  border-radius: 4px;
  background-color: #f5f7fa;
}

.stat-item.large {
  flex: 2;
  background-color: #ecf5ff;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  padding: 10px 0;
}

.no-score,
.no-submission {
  color: #909399;
  font-style: italic;
}

.export-actions {
  display: flex;
  gap: 10px;
}

.el-dialog.statistics-dialog {
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  margin: 5vh auto !important;
}

.el-dialog.statistics-dialog .el-dialog__body {
  flex: 1;
  overflow: auto;
}
</style> 