<template>
  <div class="classroom-container">
    <h1 class="page-title">在线课堂</h1>
    
    <el-row :gutter="20">
      <!-- 左侧课程列表 -->
      <el-col :span="6">
        <el-card class="course-list-card">
          <template #header>
            <div class="card-header">
              <span>课程列表</span>
              <el-radio-group v-model="courseFilter" size="small">
                <el-radio-button label="all">全部</el-radio-button>
                <el-radio-button label="live">直播中</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          
          <el-input
            v-model="searchQuery"
            placeholder="搜索课程"
            prefix-icon="el-icon-search"
            clearable
            @clear="filterCourses"
            @input="filterCourses"
          />
          
          <div class="courses-container">
            <div
              v-for="course in filteredCourses"
              :key="course.id"
              class="course-item"
              :class="{ 'active': selectedCourse && selectedCourse.id === course.id }"
              @click="selectCourse(course)"
            >
              <div class="course-item-top">
                <span class="course-title">{{ course.title }}</span>
                <el-tag
                  size="small"
                  :type="course.status === 'live' ? 'danger' : course.status === 'upcoming' ? 'warning' : 'info'"
                >
                  {{ getStatusText(course.status) }}
                </el-tag>
              </div>
              <div class="course-info">
                <span>{{ course.teacher }}</span>
                <span>{{ formatDate(course.startTime) }}</span>
              </div>
              <div class="course-students">
                <el-avatar
                  v-for="(student, index) in course.students.slice(0, 3)"
                  :key="index"
                  :size="24"
                  :src="student.avatar"
                  class="student-avatar"
                />
                <span v-if="course.students.length > 3" class="more-students">
                  +{{ course.students.length - 3 }}
                </span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧课程内容 -->
      <el-col :span="18">
        <div v-if="!selectedCourse" class="no-course-selected">
          <el-empty description="请选择一门课程" />
        </div>
        
        <div v-else class="course-content">
          <!-- 视频区域 -->
          <el-card class="video-card">
            <div class="video-container">
              <div v-if="selectedCourse.status === 'ended'" class="video-placeholder ended">
                <el-icon><el-icon-video-pause /></el-icon>
                <span>课程已结束</span>
              </div>
              <div v-else-if="selectedCourse.status === 'upcoming'" class="video-placeholder upcoming">
                <el-icon><el-icon-alarm-clock /></el-icon>
                <span>课程即将开始</span>
                <div class="countdown">{{ countdown }}</div>
              </div>
              <div v-else class="video-player">
                <video
                  ref="videoPlayer"
                  class="video-element"
                  :poster="selectedCourse.poster"
                  controls
                  autoplay
                  muted
                >
                  <source :src="selectedCourse.videoUrl" type="video/mp4">
                  您的浏览器不支持 HTML5 视频。
                </video>
              </div>
              
              <div class="video-info">
                <h2>{{ selectedCourse.title }}</h2>
                <div class="teacher-info">
                  <el-avatar :size="36" :src="selectedCourse.teacherAvatar" />
                  <span>{{ selectedCourse.teacher }}</span>
                </div>
                <div class="course-stats">
                  <div class="stat-item">
                    <el-icon><el-icon-user /></el-icon>
                    <span>{{ selectedCourse.students.length }} 人</span>
                  </div>
                  <div class="stat-item">
                    <el-icon><el-icon-clock /></el-icon>
                    <span>{{ selectedCourse.duration }} 分钟</span>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
          
          <el-row :gutter="20" class="classroom-bottom-row">
            <!-- 左侧课件区域 -->
            <el-col :span="16">
              <el-card class="materials-card">
                <template #header>
                  <div class="card-header">
                    <span>课件展示</span>
                    <el-dropdown v-if="selectedCourse.materials.length > 0">
                      <span class="el-dropdown-link">
                        课件列表
                        <el-icon><el-icon-arrow-down /></el-icon>
                      </span>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item
                            v-for="(material, index) in selectedCourse.materials"
                            :key="index"
                            @click="selectMaterial(material)"
                          >
                            {{ material.name }}
                          </el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </template>
                
                <div v-if="selectedCourse.materials.length === 0" class="no-materials">
                  <el-empty description="暂无课件" />
                </div>
                
                <div v-else-if="selectedMaterial" class="material-preview">
                  <div v-if="selectedMaterial.type === 'pdf'" class="pdf-preview">
                    <div class="pdf-controls">
                      <el-button-group>
                        <el-button size="small" @click="currentPage > 1 && currentPage--">上一页</el-button>
                        <el-button size="small" disabled>{{ currentPage }} / {{ totalPages }}</el-button>
                        <el-button size="small" @click="currentPage < totalPages && currentPage++">下一页</el-button>
                      </el-button-group>
                    </div>
                    <div class="pdf-container">
                      <img :src="selectedMaterial.preview" class="pdf-page" />
                    </div>
                  </div>
                  
                  <div v-else-if="selectedMaterial.type === 'image'" class="image-preview">
                    <img :src="selectedMaterial.url" class="material-image" />
                  </div>
                  
                  <div v-else-if="selectedMaterial.type === 'h5'" class="h5-preview">
                    <iframe :src="selectedMaterial.url" frameborder="0" class="h5-frame"></iframe>
                  </div>
                </div>
              </el-card>
            </el-col>
            
            <!-- 右侧聊天区域 -->
            <el-col :span="8">
              <el-card class="chat-card">
                <template #header>
                  <div class="card-header">
                    <span>实时交流</span>
                    <el-switch
                      v-model="isDanmakuMode"
                      active-text="弹幕模式"
                      inactive-text="聊天室"
                    />
                  </div>
                </template>
                
                <div class="chat-container">
                  <div class="messages-container">
                    <div v-for="(message, index) in messages" :key="index" class="message-item">
                      <el-avatar :size="28" :src="message.avatar" class="message-avatar" />
                      <div class="message-content">
                        <div class="message-sender">{{ message.sender }}</div>
                        <div class="message-text">{{ message.text }}</div>
                      </div>
                      <div class="message-time">{{ formatMessageTime(message.time) }}</div>
                    </div>
                  </div>
                  
                  <div class="message-input">
                    <el-input
                      v-model="newMessage"
                      placeholder="输入消息..."
                      @keyup.enter="sendMessage"
                    >
                      <template #append>
                        <el-button @click="sendMessage">发送</el-button>
                      </template>
                    </el-input>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
    
    <!-- 弹幕层，仅在弹幕模式下显示 -->
    <div v-if="isDanmakuMode && selectedCourse" class="danmaku-container">
      <transition-group name="danmaku" tag="div">
        <div 
          v-for="danmaku in activeDanmakus" 
          :key="danmaku.id" 
          class="danmaku-item"
          :style="{ top: `${danmaku.top}px`, color: danmaku.color, animationDuration: `${danmaku.duration}s` }"
        >
          {{ danmaku.text }}
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, onUnmounted, watch } from 'vue'
import { classroomApi } from '../api'

// 状态
const searchQuery = ref('')
const courseFilter = ref('all')
const selectedCourse = ref(null)
const selectedMaterial = ref(null)
const currentPage = ref(1)
const totalPages = ref(10)
const isDanmakuMode = ref(false)
const newMessage = ref('')
const messages = ref([])
const danmakuId = ref(0)
const activeDanmakus = ref([])
const countdown = ref('00:00:00')
let countdownTimer = null

// 模拟课程数据
const courses = ref([
  {
    id: 1,
    title: '高三生物冲刺班 - 细胞结构与功能',
    teacher: '张老师',
    teacherAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    status: 'live',
    startTime: new Date(Date.now() - 30 * 60000).toISOString(),
    endTime: new Date(Date.now() + 60 * 60000).toISOString(),
    duration: 90,
    poster: 'https://via.placeholder.com/800x450?text=生物课程',
    videoUrl: 'https://www.w3schools.com/html/mov_bbb.mp4',
    students: [
      { id: 1, name: '学生1', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' },
      { id: 2, name: '学生2', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' },
      { id: 3, name: '学生3', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' },
      { id: 4, name: '学生4', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' },
      { id: 5, name: '学生5', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' }
    ],
    materials: [
      { id: 1, name: '细胞结构与功能PPT', type: 'pdf', url: '#', preview: 'https://via.placeholder.com/800x600?text=细胞结构与功能PPT' },
      { id: 2, name: '显微图-细胞结构', type: 'image', url: 'https://via.placeholder.com/800x600?text=显微图-细胞结构' },
      { id: 3, name: '细胞膜模型交互课件', type: 'h5', url: '#' }
    ]
  },
  {
    id: 2,
    title: '高三生物遗传与变异专题',
    teacher: '李老师',
    teacherAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    status: 'upcoming',
    startTime: new Date(Date.now() + 30 * 60000).toISOString(),
    endTime: new Date(Date.now() + 120 * 60000).toISOString(),
    duration: 90,
    poster: 'https://via.placeholder.com/800x450?text=生物课程',
    videoUrl: '',
    students: [
      { id: 1, name: '学生1', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' },
      { id: 2, name: '学生2', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' },
      { id: 6, name: '学生6', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' }
    ],
    materials: [
      { id: 4, name: '遗传规律基础PPT', type: 'pdf', url: '#', preview: 'https://via.placeholder.com/800x600?text=遗传规律基础PPT' }
    ]
  },
  {
    id: 3,
    title: '高三生物生态系统案例分析',
    teacher: '王老师',
    teacherAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    status: 'ended',
    startTime: new Date(Date.now() - 120 * 60000).toISOString(),
    endTime: new Date(Date.now() - 30 * 60000).toISOString(),
    duration: 90,
    poster: 'https://via.placeholder.com/800x450?text=生物课程',
    videoUrl: 'https://www.w3schools.com/html/mov_bbb.mp4',
    students: [
      { id: 1, name: '学生1', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' },
      { id: 3, name: '学生3', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' },
      { id: 5, name: '学生5', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' },
      { id: 7, name: '学生7', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png' }
    ],
    materials: [
      { id: 5, name: '能量流动与物质循环', type: 'pdf', url: '#', preview: 'https://via.placeholder.com/800x600?text=能量流动与物质循环' },
      { id: 6, name: '生态系统食物网图', type: 'image', url: 'https://via.placeholder.com/800x600?text=生态系统食物网图' }
    ]
  }
])

// 模拟消息数据
const generateMessages = () => {
  const mockMessages = [
    { sender: '张三', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', text: '老师，细胞膜的主要成分是什么？', time: new Date(Date.now() - 300000) },
    { sender: '李四', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', text: '我看懂了，谢谢老师！', time: new Date(Date.now() - 240000) },
    { sender: '王五', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', text: '这个例题能再详细讲解一下吗？', time: new Date(Date.now() - 180000) },
    { sender: '张老师', avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png', text: '好的，我们来看一下这个例题的思路...', time: new Date(Date.now() - 120000) },
    { sender: '赵六', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', text: '谢谢老师的讲解！', time: new Date(Date.now() - 60000) },
    { sender: '张老师', avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png', text: '大家还有其他问题吗？', time: new Date(Date.now() - 30000) }
  ]
  
  return mockMessages
}

// 计算属性
const filteredCourses = computed(() => {
  if (!searchQuery.value && courseFilter.value === 'all') {
    return courses.value
  }
  
  return courses.value.filter(course => {
    const matchesFilter = courseFilter.value === 'all' || course.status === courseFilter.value
    const matchesSearch = !searchQuery.value || course.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesFilter && matchesSearch
  })
})

// 方法
const getStatusText = (status) => {
  const statusMap = {
    live: '直播中',
    upcoming: '即将开始',
    ended: '已结束'
  }
  return statusMap[status] || '未知'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const formatMessageTime = (date) => {
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const selectCourse = (course) => {
  selectedCourse.value = course
  if (course.materials.length > 0) {
    selectMaterial(course.materials[0])
  } else {
    selectedMaterial.value = null
  }
  
  // 加载消息
  messages.value = generateMessages()
  
  // 如果是即将开始的课程，启动倒计时
  if (course.status === 'upcoming') {
    updateCountdown()
    countdownTimer = setInterval(updateCountdown, 1000)
  } else if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
}

const selectMaterial = (material) => {
  selectedMaterial.value = material
  currentPage.value = 1
}

const updateCountdown = () => {
  if (!selectedCourse.value) return
  
  const startTime = new Date(selectedCourse.value.startTime).getTime()
  const now = Date.now()
  const diff = startTime - now
  
  if (diff <= 0) {
    clearInterval(countdownTimer)
    selectedCourse.value.status = 'live'
    countdown.value = '00:00:00'
    return
  }
  
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  const seconds = Math.floor((diff % (1000 * 60)) / 1000)
  
  countdown.value = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

const sendMessage = () => {
  if (!newMessage.value.trim()) return
  
  const message = {
    sender: '我',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    text: newMessage.value,
    time: new Date()
  }
  
  messages.value.push(message)
  
  if (isDanmakuMode.value) {
    addDanmaku(message.text)
  }
  
  newMessage.value = ''
  
  // 滚动到底部
  setTimeout(() => {
    const messagesContainer = document.querySelector('.messages-container')
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight
    }
  }, 50)
}

const addDanmaku = (text) => {
  const id = danmakuId.value++
  const top = Math.floor(Math.random() * 300)
  const colors = ['#ffffff', '#ff9966', '#66ccff', '#66ff66', '#ff6666', '#ffff66']
  const color = colors[Math.floor(Math.random() * colors.length)]
  const duration = Math.random() * 5 + 8 // 8-13秒
  
  const danmaku = { id, text, top, color, duration }
  activeDanmakus.value.push(danmaku)
  
  setTimeout(() => {
    // 移除弹幕
    const index = activeDanmakus.value.findIndex(d => d.id === id)
    if (index !== -1) {
      activeDanmakus.value.splice(index, 1)
    }
  }, duration * 1000)
}

const filterCourses = () => {
  // 已经通过计算属性处理
}

// 监听弹幕模式变化
watch(isDanmakuMode, (newVal) => {
  if (newVal) {
    // 将现有消息转换为弹幕
    messages.value.forEach(message => {
      addDanmaku(message.text)
    })
  } else {
    // 清除所有弹幕
    activeDanmakus.value = []
  }
})

// 生命周期钩子
onMounted(async () => {
  // 实际应该从API获取课程数据
  // const response = await classroomApi.getLiveCourses()
  // courses.value = response.data
  
  // 默认选中第一个直播中的课程
  const liveCourse = courses.value.find(c => c.status === 'live')
  if (liveCourse) {
    selectCourse(liveCourse)
  }
})

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
})
</script>

<style scoped>
.classroom-container {
  padding: 20px;
  position: relative;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 600;
  color: #333;
}

.course-list-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.courses-container {
  margin-top: 15px;
  max-height: 500px;
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

.course-item-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.course-title {
  font-weight: bold;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 10px;
}

.course-info {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 12px;
  margin-bottom: 5px;
}

.course-students {
  display: flex;
  align-items: center;
}

.student-avatar {
  margin-right: -8px;
  border: 2px solid #fff;
}

.more-students {
  font-size: 12px;
  color: #909399;
  margin-left: 8px;
}

.no-course-selected {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 100px 0;
}

.video-card {
  margin-bottom: 20px;
}

.video-container {
  width: 100%;
  background-color: #000;
  position: relative;
}

.video-player {
  width: 100%;
  background-color: #000;
}

.video-element {
  width: 100%;
  display: block;
}

.video-placeholder {
  width: 100%;
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-size: 24px;
}

.video-placeholder.ended {
  background-color: #606266;
}

.video-placeholder.upcoming {
  background-color: #e6a23c;
}

.video-placeholder .el-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.countdown {
  font-size: 36px;
  margin-top: 10px;
}

.video-info {
  padding: 15px;
  background-color: #fff;
}

.video-info h2 {
  margin-top: 0;
  margin-bottom: 10px;
}

.teacher-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.teacher-info span {
  margin-left: 10px;
  font-weight: bold;
}

.course-stats {
  display: flex;
}

.stat-item {
  display: flex;
  align-items: center;
  margin-right: 20px;
  color: #606266;
}

.stat-item .el-icon {
  margin-right: 5px;
}

.classroom-bottom-row {
  margin-top: 20px;
}

.materials-card, .chat-card {
  height: 500px;
}

.no-materials {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.material-preview {
  height: 400px;
  overflow: hidden;
}

.pdf-controls {
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
}

.pdf-container {
  height: 350px;
  overflow: auto;
  display: flex;
  justify-content: center;
}

.pdf-page {
  max-width: 100%;
  max-height: 100%;
}

.image-preview {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto;
}

.material-image {
  max-width: 100%;
  max-height: 100%;
}

.h5-preview {
  height: 400px;
}

.h5-frame {
  width: 100%;
  height: 100%;
  border: none;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 400px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 10px;
}

.message-item {
  display: flex;
  margin-bottom: 15px;
}

.message-avatar {
  margin-right: 8px;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 8px 12px;
}

.message-sender {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.message-text {
  word-break: break-word;
}

.message-time {
  font-size: 12px;
  color: #c0c4cc;
  margin-left: 8px;
  align-self: flex-end;
}

.danmaku-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.danmaku-item {
  position: absolute;
  white-space: nowrap;
  color: #fff;
  font-weight: bold;
  font-size: 18px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  animation: danmakuMove linear forwards;
  transform: translateX(100%);
}

@keyframes danmakuMove {
  from { transform: translateX(100%); }
  to { transform: translateX(-100%); }
}

.danmaku-enter-active {
  transition: opacity 0.3s;
}

.danmaku-leave-active {
  transition: opacity 0.3s;
}

.danmaku-enter-from, .danmaku-leave-to {
  opacity: 0;
}
</style> 