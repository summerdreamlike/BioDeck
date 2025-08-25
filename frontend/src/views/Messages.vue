<template>
  <div class="messages-container">
    <h1 class="page-title">消息中心</h1>
    
    <el-row :gutter="20">
      <!-- 左侧消息类型列表 -->
      <el-col :span="6">
        <el-card class="message-types-card">
          <template #header>
            <div class="card-header">
              <span>消息类型</span>
            </div>
          </template>
          
          <el-menu
            :default-active="activeType"
            @select="handleTypeSelect"
            class="message-types-menu"
          >
            <el-menu-item index="all">
              <el-badge :value="unreadCounts.all || 0" :hidden="unreadCounts.all === 0" class="menu-badge">
                全部消息
              </el-badge>
            </el-menu-item>
            <el-menu-item index="announcement">
              <el-badge :value="unreadCounts.announcement || 0" :hidden="unreadCounts.announcement === 0" class="menu-badge">
                学校公告
              </el-badge>
            </el-menu-item>
            <el-menu-item index="personal">
              <el-badge :value="unreadCounts.personal || 0" :hidden="unreadCounts.personal === 0" class="menu-badge">
                个人消息
              </el-badge>
            </el-menu-item>
            <el-menu-item index="feedback">
              <el-badge :value="unreadCounts.feedback || 0" :hidden="unreadCounts.feedback === 0" class="menu-badge">
                学生反馈
              </el-badge>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>
      
      <!-- 右侧消息列表 -->
      <el-col :span="18">
        <div class="message-tools">
          <div class="message-actions">
            <el-button :disabled="selectedMessages.length === 0" @click="markSelectedAsRead">
              标为已读
            </el-button>
            <el-button :disabled="selectedMessages.length === 0" type="danger" @click="deleteSelected">
              删除
            </el-button>
          </div>
          
          <div class="message-search">
            <el-input
              v-model="searchQuery"
              placeholder="搜索消息"
              prefix-icon="el-icon-search"
              clearable
              @input="filterMessages"
            />
          </div>
        </div>
        
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="10" animated />
        </div>
        
        <div v-else-if="filteredMessages.length === 0" class="empty-container">
          <el-empty description="暂无消息" />
        </div>
        
        <el-card v-else class="messages-list-card">
          <el-table
            ref="messageTable"
            :data="filteredMessages"
            style="width: 100%"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column width="40">
              <template #default="scope">
                <div class="message-status">
                  <el-badge is-dot :hidden="scope.row.read" />
                </div>
              </template>
            </el-table-column>
            <el-table-column label="类型" width="100">
              <template #default="scope">
                <el-tag :type="getMessageTypeTag(scope.row.type)" size="small">
                  {{ getMessageTypeText(scope.row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="标题" min-width="250">
              <template #default="scope">
                <div 
                  class="message-title" 
                  :class="{ 'unread': !scope.row.read }"
                  @click="openMessage(scope.row)"
                >
                  {{ scope.row.title }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="发送者" width="120">
              <template #default="scope">
                <div class="message-sender">
                  {{ scope.row.sender || '系统' }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="时间" width="180">
              <template #default="scope">
                <div class="message-time">
                  {{ formatDate(scope.row.created_at) }}
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
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
    
    <!-- 消息详情对话框 -->
    <el-dialog
      v-model="messageDialogVisible"
      :title="currentMessage.title"
      width="600px"
    >
      <div v-if="currentMessage" class="message-detail">
        <div class="message-detail-header">
          <div class="message-detail-meta">
            <span class="label">发送者:</span>
            <span class="value">{{ currentMessage.sender || '系统' }}</span>
          </div>
          <div class="message-detail-meta">
            <span class="label">时间:</span>
            <span class="value">{{ formatDate(currentMessage.created_at) }}</span>
          </div>
        </div>
        
        <div class="message-detail-content">
          {{ currentMessage.content }}
        </div>
        
        <div v-if="currentMessage.attachments && currentMessage.attachments.length > 0" class="message-attachments">
          <div class="attachments-title">附件:</div>
          <div class="attachments-list">
            <div
              v-for="(attachment, index) in currentMessage.attachments"
              :key="index"
              class="attachment-item"
              @click="downloadAttachment(attachment)"
            >
              <el-icon><el-icon-document /></el-icon>
              <span class="attachment-name">{{ attachment.name }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="messageDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="replyMessage" v-if="currentMessage.type === 'personal'">
            回复
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 回复消息对话框 -->
    <el-dialog
      v-model="replyDialogVisible"
      title="回复消息"
      width="500px"
    >
      <el-form :model="replyForm" label-width="80px">
        <el-form-item label="收件人">
          <el-input v-model="replyForm.recipient" disabled />
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="replyForm.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input
            v-model="replyForm.content"
            type="textarea"
            rows="5"
            placeholder="请输入消息内容"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="replyDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReply">发送</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { messagesApi } from '../api'
import { useMessagesStore } from '../store'

// 状态变量
const activeType = ref('all')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)
const selectedMessages = ref([])

// 对话框控制
const messageDialogVisible = ref(false)
const replyDialogVisible = ref(false)
const currentMessage = ref({})

// 回复表单
const replyForm = reactive({
  recipient: '',
  title: '',
  content: ''
})

// Pinia store
const messagesStore = useMessagesStore()

// 模拟消息数据
const messages = ref([])

// 生成模拟消息
const generateMockMessages = () => {
  const types = ['announcement', 'personal', 'feedback']
  const titles = [
    '关于期末考试安排的通知',
    '教学进度反馈',
    '学生成绩分析报告',
    '教研活动邀请',
    '教材更新通知',
    '课程调整安排',
    '家长会通知',
    '教师培训计划'
  ]
  const senders = ['系统', '张主任', '李老师', '王校长', '教务处', '学生张三', '学生李四']
  
  const mockMessages = []
  
  for (let i = 1; i <= 50; i++) {
    const type = types[Math.floor(Math.random() * types.length)]
    const titleIndex = Math.floor(Math.random() * titles.length)
    const senderIndex = Math.floor(Math.random() * senders.length)
    const read = Math.random() > 0.3 // 70%已读
    
    const date = new Date()
    date.setDate(date.getDate() - Math.floor(Math.random() * 30))
    
    mockMessages.push({
      id: i,
      type: type,
      title: titles[titleIndex],
      sender: type === 'announcement' ? '系统' : senders[senderIndex],
      content: `这是一条${getMessageTypeText(type)}消息的详细内容，用于展示消息的完整信息。消息ID: ${i}`,
      read: read,
      created_at: date.toISOString(),
      attachments: Math.random() > 0.7 ? [
        { id: i * 100 + 1, name: '附件1.pdf' },
        { id: i * 100 + 2, name: '附件2.docx' }
      ] : []
    })
  }
  
  return mockMessages
}

// 计算属性
const filteredMessages = computed(() => {
  let result = [...messages.value]
  
  // 按类型筛选
  if (activeType.value !== 'all') {
    result = result.filter(message => message.type === activeType.value)
  }
  
  // 按搜索词筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(message => 
      message.title.toLowerCase().includes(query) || 
      (message.sender && message.sender.toLowerCase().includes(query)) ||
      message.content.toLowerCase().includes(query)
    )
  }
  
  // 更新总数
  total.value = result.length
  
  // 应用分页
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  
  return result.slice(start, end)
})

const unreadCounts = computed(() => {
  const counts = {
    all: 0,
    announcement: 0,
    personal: 0,
    feedback: 0
  }
  
  messages.value.forEach(message => {
    if (!message.read) {
      counts.all++
      counts[message.type]++
    }
  })
  
  return counts
})

// 方法
const handleTypeSelect = (type) => {
  activeType.value = type
  currentPage.value = 1
}

const filterMessages = () => {
  currentPage.value = 1
}

const handleSelectionChange = (selection) => {
  selectedMessages.value = selection
}

const handleCurrentChange = (page) => {
  currentPage.value = page
}

const markSelectedAsRead = () => {
  selectedMessages.value.forEach(message => {
    const index = messages.value.findIndex(m => m.id === message.id)
    if (index !== -1) {
      messages.value[index].read = true
    }
  })
  
  // 更新消息存储
  messagesStore.setMessages(messages.value)
}

const deleteSelected = () => {
  if (confirm(`确定要删除选中的 ${selectedMessages.value.length} 条消息吗？`)) {
    const selectedIds = selectedMessages.value.map(message => message.id)
    messages.value = messages.value.filter(message => !selectedIds.includes(message.id))
    
    // 更新消息存储
    messagesStore.setMessages(messages.value)
  }
}

const openMessage = (message) => {
  currentMessage.value = message
  messageDialogVisible.value = true
  
  // 标记为已读
  if (!message.read) {
    const index = messages.value.findIndex(m => m.id === message.id)
    if (index !== -1) {
      messages.value[index].read = true
      
      // 更新消息存储
      messagesStore.setMessages(messages.value)
    }
  }
}

const replyMessage = () => {
  replyForm.recipient = currentMessage.value.sender
  replyForm.title = `回复: ${currentMessage.value.title}`
  replyForm.content = ''
  
  messageDialogVisible.value = false
  replyDialogVisible.value = true
}

const submitReply = () => {
  // 实际应用中这里应该调用API发送消息
  alert('回复已发送')
  replyDialogVisible.value = false
}

const downloadAttachment = (attachment) => {
  // 实际应用中这里应该调用API下载附件
  alert(`开始下载: ${attachment.name}`)
}

const getMessageTypeText = (type) => {
  const typeMap = {
    announcement: '公告',
    personal: '个人消息',
    feedback: '学生反馈'
  }
  return typeMap[type] || '未知'
}

const getMessageTypeTag = (type) => {
  const tagMap = {
    announcement: 'info',
    personal: 'primary',
    feedback: 'success'
  }
  return tagMap[type] || ''
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 获取消息数据
const fetchMessages = async () => {
  loading.value = true
  
  try {
    // 模拟API调用
    setTimeout(() => {
      messages.value = generateMockMessages()
      total.value = messages.value.length
      
      // 更新消息存储
      messagesStore.setMessages(messages.value)
      
      loading.value = false
    }, 500)
    
    // 实际API调用
    /*
    const response = await messagesApi.getMessages()
    messages.value = response
    total.value = response.length
    
    // 更新消息存储
    messagesStore.setMessages(messages.value)
    */
  } catch (error) {
    console.error('Failed to fetch messages', error)
  } finally {
    loading.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  fetchMessages()
})
</script>

<style scoped>
.messages-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 600;
  color: #333;
}

.message-types-card {
  margin-bottom: 20px;
}

.card-header {
  font-weight: bold;
}

.menu-badge {
  margin-top: 0;
}

.message-tools {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.message-search {
  width: 250px;
}

.loading-container,
.empty-container {
  padding: 40px 0;
  text-align: center;
}

.messages-list-card {
  margin-bottom: 20px;
}

.message-status {
  display: flex;
  justify-content: center;
}

.message-title {
  cursor: pointer;
}

.message-title:hover {
  color: #409EFF;
}

.message-title.unread {
  font-weight: bold;
}

.message-sender,
.message-time {
  font-size: 14px;
  color: #909399;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.message-detail {
  padding: 10px;
}

.message-detail-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.message-detail-meta {
  font-size: 14px;
}

.message-detail-content {
  line-height: 1.8;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  white-space: pre-line;
}

.message-attachments {
  margin-top: 20px;
}

.attachments-title {
  font-weight: bold;
  margin-bottom: 10px;
}

.attachment-item {
  display: flex;
  align-items: center;
  padding: 5px 10px;
  border: 1px solid #EBEEF5;
  border-radius: 4px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.attachment-item:hover {
  background-color: #f5f7fa;
}

.attachment-name {
  margin-left: 5px;
  color: #409EFF;
}

.label {
  color: #909399;
  margin-right: 5px;
}
</style> 