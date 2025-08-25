<template>
  <div class="attendance-container">
    <h1 class="page-title">考勤管理</h1>
    
    <el-row :gutter="20">
      <!-- 左侧课程列表和签到管理 -->
      <el-col :span="8">
        <!-- 课程卡片 -->
        <el-card class="courses-card">
          <template #header>
            <div class="card-header">
              <span>课程列表</span>
            </div>
          </template>
          
          <div class="course-search">
            <el-input
              v-model="searchQuery"
              placeholder="搜索课程"
              prefix-icon="el-icon-search"
              clearable
              @input="filterCourses"
            />
          </div>
          
          <el-tabs v-model="courseTabActive" @tab-click="handleCourseTabChange">
            <el-tab-pane label="今日课程" name="today">
              <div v-if="todayCourses.length === 0" class="empty-courses">
                <el-empty description="今日暂无课程" />
              </div>
              <div v-else class="course-list">
                <div
                  v-for="course in todayCourses"
                  :key="course.id"
                  class="course-item"
                  :class="{ 'active': selectedCourse && selectedCourse.id === course.id }"
                  @click="selectCourse(course)"
                >
                  <div class="course-title">{{ course.title }}</div>
                  <div class="course-info">
                    <span>{{ course.teacher }}</span>
                    <span>{{ formatTime(course.start_time) }} - {{ formatTime(course.end_time) }}</span>
                  </div>
                  <div class="course-status">
                    <el-tag :type="getCourseStatusType(course)" size="small">{{ getCourseStatusText(course) }}</el-tag>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            <el-tab-pane label="所有课程" name="all">
              <div v-if="filteredCourses.length === 0" class="empty-courses">
                <el-empty description="暂无课程" />
              </div>
              <div v-else class="course-list">
                <div
                  v-for="course in filteredCourses"
                  :key="course.id"
                  class="course-item"
                  :class="{ 'active': selectedCourse && selectedCourse.id === course.id }"
                  @click="selectCourse(course)"
                >
                  <div class="course-title">{{ course.title }}</div>
                  <div class="course-info">
                    <span>{{ course.teacher }}</span>
                    <span>{{ formatDate(course.date) }}</span>
                  </div>
                  <div class="course-status">
                    <el-tag :type="getCourseStatusType(course)" size="small">{{ getCourseStatusText(course) }}</el-tag>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
        
        <!-- 签到方式卡片 -->
        <el-card v-if="selectedCourse" class="check-in-card">
          <template #header>
            <div class="card-header">
              <span>发起签到</span>
            </div>
          </template>
          
          <div class="check-in-methods">
            <el-tabs v-model="checkInMethodActive">
              <el-tab-pane label="二维码签到" name="qrcode">
                <div class="check-in-method-content">
                  <div v-if="checkInActive" class="check-in-active">
                    <div class="qrcode-container">
                      <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=attendance_code_123456" class="qrcode-image" />
                    </div>
                    <div class="check-in-code">
                      <span class="code-label">签到码:</span>
                      <span class="code-value">{{ checkInCode }}</span>
                    </div>
                    <div class="check-in-timer">
                      <span class="timer-label">剩余时间:</span>
                      <span class="timer-value">{{ checkInCountdown }}</span>
                    </div>
                    <el-button type="danger" plain @click="stopCheckIn">结束签到</el-button>
                  </div>
                  <div v-else class="check-in-inactive">
                    <el-form :model="qrcodeForm" label-position="top">
                      <el-form-item label="有效时间(分钟)">
                        <el-input-number v-model="qrcodeForm.duration" :min="1" :max="30" />
                      </el-form-item>
                      <el-button type="primary" @click="startQrcodeCheckIn">开始签到</el-button>
                    </el-form>
                  </div>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="口令签到" name="password">
                <div class="check-in-method-content">
                  <div v-if="checkInActive" class="check-in-active">
                    <div class="password-display">
                      <span class="password-label">签到口令:</span>
                      <span class="password-value">{{ checkInPassword }}</span>
                    </div>
                    <div class="check-in-timer">
                      <span class="timer-label">剩余时间:</span>
                      <span class="timer-value">{{ checkInCountdown }}</span>
                    </div>
                    <el-button type="danger" plain @click="stopCheckIn">结束签到</el-button>
                  </div>
                  <div v-else class="check-in-inactive">
                    <el-form :model="passwordForm" label-position="top">
                      <el-form-item label="签到口令">
                        <el-input v-model="passwordForm.password" placeholder="输入签到口令或自动生成" clearable>
                          <template #append>
                            <el-button @click="generateRandomPassword">随机</el-button>
                          </template>
                        </el-input>
                      </el-form-item>
                      <el-form-item label="有效时间(分钟)">
                        <el-input-number v-model="passwordForm.duration" :min="1" :max="30" />
                      </el-form-item>
                      <el-button type="primary" @click="startPasswordCheckIn">开始签到</el-button>
                    </el-form>
                  </div>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="手势签到" name="gesture">
                <div class="check-in-method-content">
                  <div v-if="checkInActive" class="check-in-active">
                    <div class="gesture-display">
                      <div class="gesture-image">
                        <img :src="gestureImageUrl" class="gesture-img" />
                      </div>
                      <div class="gesture-name">{{ gestureName }}</div>
                    </div>
                    <div class="check-in-timer">
                      <span class="timer-label">剩余时间:</span>
                      <span class="timer-value">{{ checkInCountdown }}</span>
                    </div>
                    <el-button type="danger" plain @click="stopCheckIn">结束签到</el-button>
                  </div>
                  <div v-else class="check-in-inactive">
                    <el-form :model="gestureForm" label-position="top">
                      <el-form-item label="选择手势">
                        <el-select v-model="gestureForm.gesture" placeholder="请选择手势">
                          <el-option label="剪刀" value="scissors" />
                          <el-option label="石头" value="rock" />
                          <el-option label="布" value="paper" />
                          <el-option label="OK" value="ok" />
                          <el-option label="点赞" value="thumbs-up" />
                        </el-select>
                      </el-form-item>
                      <el-form-item label="有效时间(分钟)">
                        <el-input-number v-model="gestureForm.duration" :min="1" :max="30" />
                      </el-form-item>
                      <el-button type="primary" @click="startGestureCheckIn">开始签到</el-button>
                    </el-form>
                  </div>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="随机点名" name="random">
                <div class="check-in-method-content">
                  <div v-if="randomStudent" class="random-student-active">
                    <div class="random-student-display">
                      <div class="student-avatar">
                        <el-avatar :size="80" :src="randomStudent.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
                      </div>
                      <div class="student-name">{{ randomStudent.name }}</div>
                      <div class="student-class">{{ randomStudent.class }}</div>
                    </div>
                    <div class="random-actions">
                      <el-button type="success" @click="markAttendance(randomStudent, 'present')">出勤</el-button>
                      <el-button type="danger" @click="markAttendance(randomStudent, 'absent')">缺勤</el-button>
                      <el-button plain @click="randomStudent = null">取消</el-button>
                    </div>
                  </div>
                  <div v-else class="random-student-inactive">
                    <p class="random-description">从班级学生名单中随机选择一名学生进行点名</p>
                    <el-button type="primary" @click="randomCallStudent">开始随机点名</el-button>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧考勤记录 -->
      <el-col :span="16">
        <el-card class="attendance-records-card">
          <template #header>
            <div class="card-header-with-actions">
              <span>考勤记录</span>
              <div class="header-actions">
                <el-button size="small" type="primary" plain @click="exportAttendance('excel')">
                  <el-icon><el-icon-download /></el-icon>
                  导出Excel
                </el-button>
                <el-button size="small" plain @click="exportAttendance('csv')">
                  <el-icon><el-icon-document /></el-icon>
                  导出CSV
                </el-button>
              </div>
            </div>
          </template>
          
          <div v-if="!selectedCourse" class="no-course-selected">
            <el-empty description="请选择一门课程查看考勤记录" />
          </div>
          
          <div v-else>
            <div class="attendance-summary">
              <div class="summary-item">
                <span class="label">总人数:</span>
                <span class="value">{{ selectedCourse.total_students }}</span>
              </div>
              <div class="summary-item">
                <span class="label">已签到:</span>
                <span class="value">{{ attendanceStats.present }}</span>
              </div>
              <div class="summary-item">
                <span class="label">缺勤:</span>
                <span class="value">{{ attendanceStats.absent }}</span>
              </div>
              <div class="summary-item">
                <span class="label">迟到:</span>
                <span class="value">{{ attendanceStats.late }}</span>
              </div>
              <div class="summary-item">
                <span class="label">请假:</span>
                <span class="value">{{ attendanceStats.leave }}</span>
              </div>
              <div class="summary-item">
                <span class="label">出勤率:</span>
                <span class="value">{{ attendanceStats.attendanceRate }}%</span>
              </div>
            </div>
            
            <div class="attendance-chart-container">
              <div ref="attendanceChart" style="width: 100%; height: 300px;"></div>
            </div>
            
            <el-table
              :data="attendanceRecords"
              style="width: 100%; margin-top: 20px"
              border
            >
              <el-table-column prop="student_id" label="学号" width="120" />
              <el-table-column prop="student_name" label="姓名" width="100" />
              <el-table-column prop="class" label="班级" width="120" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getAttendanceTagType(scope.row.status)">
                    {{ getAttendanceStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="check_in_time" label="签到时间" width="180">
                <template #default="scope">
                  {{ scope.row.check_in_time ? formatDateTime(scope.row.check_in_time) : '-' }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150">
                <template #default="scope">
                  <el-dropdown @command="(command) => handleAttendanceCommand(command, scope.row)">
                    <el-button size="small" plain>
                      修改状态
                      <el-icon class="el-icon--right"><el-icon-arrow-down /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="present">出勤</el-dropdown-item>
                        <el-dropdown-item command="late">迟到</el-dropdown-item>
                        <el-dropdown-item command="leave">请假</el-dropdown-item>
                        <el-dropdown-item command="absent">缺勤</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { attendanceApi } from '../api'

// 状态变量
const searchQuery = ref('')
const courseTabActive = ref('today')
const checkInMethodActive = ref('qrcode')
const selectedCourse = ref(null)
const checkInActive = ref(false)
const checkInCode = ref('123456')
const checkInPassword = ref('')
const checkInCountdown = ref('05:00')
const gestureName = ref('')
const gestureImageUrl = ref('')
const randomStudent = ref(null)
let countdownTimer = null

// 表单数据
const qrcodeForm = reactive({
  duration: 5
})

const passwordForm = reactive({
  password: '',
  duration: 5
})

const gestureForm = reactive({
  gesture: '',
  duration: 5
})

// 课程数据
const courses = ref([])

// 考勤记录
const attendanceRecords = ref([])

// 计算属性
const todayCourses = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  return courses.value.filter(course => course.date === today)
})

const filteredCourses = computed(() => {
  if (!searchQuery.value) return courses.value
  
  const query = searchQuery.value.toLowerCase()
  return courses.value.filter(course => 
    course.title.toLowerCase().includes(query) || 
    course.teacher.toLowerCase().includes(query)
  )
})

const attendanceStats = computed(() => {
  const present = attendanceRecords.value.filter(r => r.status === 'present').length
  const absent = attendanceRecords.value.filter(r => r.status === 'absent').length
  const late = attendanceRecords.value.filter(r => r.status === 'late').length
  const leave = attendanceRecords.value.filter(r => r.status === 'leave').length
  const total = selectedCourse.value ? selectedCourse.value.total_students : 0
  const attendanceRate = total > 0 ? Math.round(((present + late) / total) * 100) : 0
  
  return {
    present,
    absent,
    late,
    leave,
    attendanceRate
  }
})

// 方法
const filterCourses = () => {
  // 通过计算属性自动筛选
}

const handleCourseTabChange = () => {
  // 切换课程标签时的处理
}

const selectCourse = (course) => {
  selectedCourse.value = course
  fetchAttendanceRecords(course.id)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
}

const formatTime = (timeString) => {
  return timeString.substring(11, 16)
}

const formatDateTime = (dateTimeString) => {
  return `${formatDate(dateTimeString)} ${formatTime(dateTimeString)}`
}

const getCourseStatusType = (course) => {
  const now = new Date()
  const startTime = new Date(`${course.date}T${course.start_time}`)
  const endTime = new Date(`${course.date}T${course.end_time}`)
  
  if (now < startTime) return 'info'    // 未开始
  if (now > endTime) return ''          // 已结束
  return 'success'                      // 进行中
}

const getCourseStatusText = (course) => {
  const now = new Date()
  const startTime = new Date(`${course.date}T${course.start_time}`)
  const endTime = new Date(`${course.date}T${course.end_time}`)
  
  if (now < startTime) return '未开始'
  if (now > endTime) return '已结束'
  return '进行中'
}

const getAttendanceTagType = (status) => {
  const types = {
    present: 'success',
    late: 'warning',
    absent: 'danger',
    leave: 'info'
  }
  return types[status] || ''
}

const getAttendanceStatusText = (status) => {
  const texts = {
    present: '出勤',
    late: '迟到',
    absent: '缺勤',
    leave: '请假'
  }
  return texts[status] || '未知'
}

const startQrcodeCheckIn = () => {
  checkInActive.value = true
  checkInCode.value = generateRandomCode(6)
  startCountdown(qrcodeForm.duration)
}

const startPasswordCheckIn = () => {
  if (!passwordForm.password) {
    passwordForm.password = generateRandomPassword()
  }
  
  checkInActive.value = true
  checkInPassword.value = passwordForm.password
  startCountdown(passwordForm.duration)
}

const startGestureCheckIn = () => {
  if (!gestureForm.gesture) {
    alert('请选择手势')
    return
  }
  
  checkInActive.value = true
  const gestures = {
    'scissors': { name: '剪刀', url: 'https://via.placeholder.com/200x200?text=Scissors' },
    'rock': { name: '石头', url: 'https://via.placeholder.com/200x200?text=Rock' },
    'paper': { name: '布', url: 'https://via.placeholder.com/200x200?text=Paper' },
    'ok': { name: 'OK', url: 'https://via.placeholder.com/200x200?text=OK' },
    'thumbs-up': { name: '点赞', url: 'https://via.placeholder.com/200x200?text=ThumbsUp' }
  }
  
  gestureName.value = gestures[gestureForm.gesture].name
  gestureImageUrl.value = gestures[gestureForm.gesture].url
  startCountdown(gestureForm.duration)
}

const stopCheckIn = () => {
  checkInActive.value = false
  if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
}

const startCountdown = (minutes) => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
  
  let seconds = minutes * 60
  
  const updateCountdown = () => {
    const mins = Math.floor(seconds / 60).toString().padStart(2, '0')
    const secs = (seconds % 60).toString().padStart(2, '0')
    checkInCountdown.value = `${mins}:${secs}`
    
    if (seconds <= 0) {
      clearInterval(countdownTimer)
      checkInActive.value = false
      return
    }
    
    seconds--
  }
  
  updateCountdown()
  countdownTimer = setInterval(updateCountdown, 1000)
}

const generateRandomCode = (length) => {
  const digits = '0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += digits.charAt(Math.floor(Math.random() * digits.length))
  }
  return result
}

const generateRandomPassword = () => {
  const words = ['苹果', '香蕉', '橙子', '西瓜', '草莓', '葡萄', '菠萝', '梨子', '樱桃', '蓝莓']
  return words[Math.floor(Math.random() * words.length)]
}

const randomCallStudent = () => {
  if (!selectedCourse.value || !attendanceRecords.value.length) {
    alert('请先选择一门课程')
    return
  }
  
  // 从考勤记录中随机选择一个学生
  const randomIndex = Math.floor(Math.random() * attendanceRecords.value.length)
  randomStudent.value = attendanceRecords.value[randomIndex]
}

const markAttendance = (student, status) => {
  if (!student) return
  
  // 更新考勤状态
  const index = attendanceRecords.value.findIndex(r => r.id === student.id)
  if (index !== -1) {
    const newRecord = { ...attendanceRecords.value[index] }
    newRecord.status = status
    if (status === 'present' || status === 'late') {
      newRecord.check_in_time = new Date().toISOString()
    }
    
    attendanceRecords.value.splice(index, 1, newRecord)
    
    // 关闭随机点名
    randomStudent.value = null
    
    // 重新初始化图表
    initAttendanceChart()
  }
}

const handleAttendanceCommand = (command, row) => {
  markAttendance(row, command)
}

const exportAttendance = (format) => {
  if (!selectedCourse.value) {
    alert('请先选择一门课程')
    return
  }
  
  // 实际应用中调用API导出数据
  alert(`正在导出${format === 'excel' ? 'Excel' : 'CSV'}格式考勤表...`)
}

const initAttendanceChart = () => {
  if (!document.querySelector('[ref="attendanceChart"]')) return
  
  const chartDom = document.querySelector('[ref="attendanceChart"]')
  const chart = echarts.init(chartDom)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: 'bottom',
      data: ['出勤', '迟到', '缺勤', '请假']
    },
    series: [
      {
        name: '考勤状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: attendanceStats.value.present, name: '出勤', itemStyle: { color: '#67C23A' } },
          { value: attendanceStats.value.late, name: '迟到', itemStyle: { color: '#E6A23C' } },
          { value: attendanceStats.value.absent, name: '缺勤', itemStyle: { color: '#F56C6C' } },
          { value: attendanceStats.value.leave, name: '请假', itemStyle: { color: '#909399' } }
        ]
      }
    ]
  }
  
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

// 获取考勤记录
const fetchAttendanceRecords = async (courseId) => {
  // 实际应用中调用API获取数据
  // const response = await attendanceApi.getAttendance(courseId)
  // attendanceRecords.value = response
  
  // 生成模拟考勤数据
  const mockStudents = []
  const statuses = ['present', 'present', 'present', 'late', 'absent', 'leave'] // 权重比例
  const studentNames = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十']
  
  if (selectedCourse.value) {
    const totalStudents = selectedCourse.value.total_students || 30
    
    for (let i = 1; i <= totalStudents; i++) {
      const nameIndex = Math.floor(Math.random() * studentNames.length)
      const statusIndex = Math.floor(Math.random() * statuses.length)
      const status = statuses[statusIndex]
      
      mockStudents.push({
        id: i,
        student_id: `S2023${(10000 + i).toString().substring(1)}`,
        student_name: `${studentNames[nameIndex]}${Math.floor(i / studentNames.length) + 1}`,
        class: `高三(${Math.floor(i % 5) + 1})班`,
        status: status,
        check_in_time: status === 'present' || status === 'late' ? new Date().toISOString() : null
      })
    }
    
    attendanceRecords.value = mockStudents
    
    // 初始化图表
    setTimeout(() => {
      initAttendanceChart()
    }, 100)
  }
}

// 获取课程数据
const fetchCourses = async () => {
  // 实际应用中调用API获取数据
  // const response = await attendanceApi.getCourses()
  // courses.value = response
  
  // 生成模拟课程数据
  const mockCourses = []
  const courseTitles = [
    '高三生物总复习',
    '高三生物细胞与分子',
    '高三生物生态系统',
    '高三生物生命活动调节',
    '高三生物遗传与进化'
  ]
  const teachers = ['张老师', '李老师', '王老师', '赵老师', '钱老师']
  
  // 生成今天的课程
  const today = new Date().toISOString().slice(0, 10)
  for (let i = 1; i <= 3; i++) {
    const startHour = 8 + i * 2
    const endHour = startHour + 1
    
    mockCourses.push({
      id: i,
      title: courseTitles[i % courseTitles.length],
      teacher: teachers[i % teachers.length],
      date: today,
      start_time: `${startHour.toString().padStart(2, '0')}:00:00`,
      end_time: `${endHour.toString().padStart(2, '0')}:00:00`,
      total_students: 30 + Math.floor(Math.random() * 20)
    })
  }
  
  // 生成过去几天的课程
  for (let day = 1; day <= 5; day++) {
    const date = new Date()
    date.setDate(date.getDate() - day)
    const dateStr = date.toISOString().slice(0, 10)
    
    for (let i = 1; i <= 2; i++) {
      const startHour = 8 + i * 2
      const endHour = startHour + 1
      const courseIndex = (day + i) % courseTitles.length
      const teacherIndex = (day + i) % teachers.length
      
      mockCourses.push({
        id: 3 + (day - 1) * 2 + i,
        title: courseTitles[courseIndex],
        teacher: teachers[teacherIndex],
        date: dateStr,
        start_time: `${startHour.toString().padStart(2, '0')}:00:00`,
        end_time: `${endHour.toString().padStart(2, '0')}:00:00`,
        total_students: 30 + Math.floor(Math.random() * 20)
      })
    }
  }
  
  courses.value = mockCourses
  
  // 如果有今日课程，默认选择第一个
  if (todayCourses.value.length > 0) {
    selectCourse(todayCourses.value[0])
  }
}

// 清理函数
const cleanup = () => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
}

// 监听
watch(selectedCourse, (newCourse) => {
  if (newCourse) {
    checkInActive.value = false
    if (countdownTimer) {
      clearInterval(countdownTimer)
      countdownTimer = null
    }
  }
})

// 生命周期钩子
onMounted(() => {
  fetchCourses()
})

onUnmounted(() => {
  cleanup()
})
</script>

<style scoped>
.attendance-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 600;
  color: #333;
}

.card-header {
  font-weight: bold;
}

.card-header-with-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.courses-card,
.check-in-card {
  margin-bottom: 20px;
}

.course-search {
  margin-bottom: 15px;
}

.empty-courses {
  padding: 20px 0;
  text-align: center;
}

.course-list {
  max-height: 300px;
  overflow-y: auto;
}

.course-item {
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
  cursor: pointer;
  transition: background-color 0.3s;
}

.course-item:hover {
  background-color: #f5f7fa;
}

.course-item.active {
  background-color: #ecf5ff;
  border-left: 3px solid #409EFF;
}

.course-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.course-info {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 12px;
  margin-bottom: 5px;
}

.course-status {
  text-align: right;
}

.check-in-method-content {
  padding: 20px 0;
}

.check-in-inactive {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.check-in-active {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.qrcode-container {
  margin-bottom: 20px;
}

.qrcode-image {
  max-width: 200px;
  border: 1px solid #ddd;
}

.check-in-code,
.password-display,
.check-in-timer {
  margin-bottom: 15px;
  font-size: 16px;
}

.code-label,
.password-label,
.timer-label {
  color: #909399;
  margin-right: 5px;
}

.code-value,
.password-value,
.timer-value {
  font-weight: bold;
  font-size: 18px;
}

.timer-value {
  color: #F56C6C;
}

.gesture-display {
  margin-bottom: 20px;
}

.gesture-img {
  width: 200px;
  height: 200px;
  object-fit: contain;
  margin-bottom: 10px;
}

.gesture-name {
  font-size: 18px;
  font-weight: bold;
}

.random-student-display {
  margin-bottom: 20px;
  text-align: center;
}

.student-name {
  font-size: 18px;
  font-weight: bold;
  margin-top: 10px;
}

.student-class {
  color: #909399;
}

.random-actions {
  display: flex;
  gap: 10px;
}

.random-description {
  margin-bottom: 20px;
  text-align: center;
  color: #909399;
}

.no-course-selected {
  padding: 50px 0;
  text-align: center;
}

.attendance-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
}

.summary-item {
  background-color: #f5f7fa;
  padding: 10px 15px;
  border-radius: 4px;
  min-width: 100px;
  flex: 1;
}

.label {
  color: #909399;
  font-size: 12px;
  margin-right: 5px;
}

.value {
  font-weight: bold;
  font-size: 16px;
}

.attendance-chart-container {
  margin-bottom: 20px;
}
</style> 