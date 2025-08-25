<template>
  <div class="app-container">
    <!-- 左侧导航栏 -->
    <nav class="side-nav">
      <div class="nav-header">
        <span class="logo-icon">🧬</span>
        <span class="logo-text">生物问答系统</span>
      </div>
      <div class="nav-links">
        <router-link to="/chat" class="nav-link" active-class="active">
          <div class="nav-link-content">
            <span class="nav-icon">💭</span>
            <span class="nav-text">AI 问答</span>
          </div>
        </router-link>
        <router-link to="/biology" class="nav-link" active-class="active">
          <div class="nav-link-content">
            <span class="nav-icon">🔬</span>
            <span class="nav-text">生物实验</span>
          </div>
        </router-link>
      </div>
      <!-- 添加用户信息和升级按钮部分 -->
      <div class="user-section">
        <div class="user-info">
          <div class="user-avatar">U</div>
          <div class="user-details">
            <div class="user-name">User_fX5b</div>
            <div class="user-credits">
              <span class="credits-icon">💎</span>
              <span>20</span>
            </div>
          </div>
        </div>
        <button class="upgrade-btn">
          <span class="upgrade-icon">⭐</span>
          <span>Upgrade</span>
        </button>
      </div>
    </nav>

    <div class="main-content">
      <div class="chat-container">
        <!-- 聊天历史区域 -->
        <div class="chat-history" ref="chatHistoryRef">
          <div v-for="(message, index) in messages" :key="index" class="message" :class="message.role">
            <div class="message-content">
              <div class="message-header">
                <span class="message-icon">{{ message.role === 'user' ? '👤' : '🧬' }}</span>
              </div>
              <div class="message-text" v-if="message.role === 'user'">
                <template v-if="message.imageUrl">
                  <div class="message-image">
                    <img :src="message.imageUrl" alt="问题图片" class="message-image-preview" />
                  </div>
                  <div class="message-question" v-if="message.content">
                    {{ message.content }}
                  </div>
                </template>
                <template v-else>
                  {{ message.content }}
                </template>
              </div>
              <div class="message-text" v-else v-html="formatMessage(message.content)"></div>
            </div>
          </div>
          <div v-if="isLoading" class="message assistant">
            <div class="message-content">
              <div class="message-header">
                <span class="message-icon">🧬</span>
              </div>
              <div class="loading">思考中...</div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-area">
          <div class="input-wrapper">
            <textarea
              v-model="userInput"
              placeholder="输入你的生物学问题..."
              @keydown.enter.prevent="sendMessage"
              rows="3"
              :disabled="isLoading"
            ></textarea>
            <div class="input-actions">
              <button class="upload-btn" @click="triggerFileUpload" :disabled="isLoading">
                <span class="upload-icon">🔬</span>
                <span class="upload-text">上传图片</span>
              </button>
              <input
                type="file"
                ref="fileInput"
                accept="image/*"
                @change="handleFileUpload"
                style="display: none"
              />
              <button class="send-btn" @click="sendMessage" :disabled="!userInput.trim() || isLoading">
                <span class="send-icon">📤</span>
                <span class="send-text">{{ isLoading ? '发送中...' : '发送' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { biologyApi } from '../../api/biology'
import { v4 as uuidv4 } from 'uuid'
import '@/styles/nav.css'

// 声明 MathJax 类型
declare global {
  interface Window {
    MathJax: any
  }
}

interface Message {
  role: 'user' | 'assistant'
  content: string
  imageUrl?: string
}

const messages = ref<Message[]>([])
const userInput = ref('')
const chatHistoryRef = ref<HTMLElement | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const sessionId = ref(localStorage.getItem('sessionId') || uuidv4())
const isLoading = ref(false)

// 加载 MathJax
const loadMathJax = () => {
  return new Promise<void>((resolve) => {
    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js'
    script.async = true
    script.onload = () => {
      window.MathJax.startup = {
        typeset: false,
        ready: () => {
          window.MathJax.startup.defaultReady()
          resolve()
        }
      }
    }
    document.head.appendChild(script)
  })
}

// 格式化消息内容（处理生物学公式和术语）
const formatMessage = (content: string) => {
  // 将生物学公式用 \[...\] 或 \(...\) 包裹
  return content
    .replace(/\$\$(.*?)\$\$/g, '\\[$1\\]')
    .replace(/\$(.*?)\$/g, '\\($1\\)')
    .replace(/\n/g, '<br>')
}

// 渲染消息中的生物学公式
const renderBiology = async () => {
  await nextTick()
  const messageElements = chatHistoryRef.value?.querySelectorAll('.message-text')
  if (messageElements) {
    try {
      await window.MathJax.typesetPromise(Array.from(messageElements))
    } catch (error) {
      console.error('生物学公式渲染失败:', error)
    }
  }
}

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (chatHistoryRef.value) {
    chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight
  }
}

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim()) return

  const question = userInput.value
  messages.value.push({ 
    role: 'user', 
    content: question || '请解答这个生物学问题'
  })
  userInput.value = ''
  isLoading.value = true
  await scrollToBottom()

  try {
    console.log('发送问题:', question)
    const response = await biologyApi.sendQuestion(question)
    console.log('收到回答:', response)
    if (response.answer) {
      messages.value.push({ 
        role: 'assistant', 
        content: response.answer
      })
      await renderBiology()
    } else {
      throw new Error('回答为空')
    }
    await scrollToBottom()
  } catch (error: any) {
    console.error('发送消息失败:', error)
    messages.value.push({ 
      role: 'assistant', 
      content: `抱歉，处理问题时出现错误：${error.message || '未知错误'}，请稍后重试。` 
    })
    await scrollToBottom()
  } finally {
    isLoading.value = false
  }
}

// 触发文件上传
const triggerFileUpload = () => {
  fileInput.value?.click()
}

// 处理文件上传
const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    const file = input.files[0]
    const reader = new FileReader()
    reader.onload = async (e) => {
      const imageUrl = e.target?.result as string
      // 直接发送图片到聊天区域
      messages.value.push({ 
        role: 'user', 
        content: userInput.value || '请解答这个生物学问题',
        imageUrl: imageUrl
      })
      isLoading.value = true
      await scrollToBottom()

      try {
        const response = await biologyApi.uploadImage(file, userInput.value || '请解答这个生物学问题')
        if (response.answer) {
          messages.value.push({ 
            role: 'assistant', 
            content: response.answer
          })
          await renderBiology()
        } else {
          throw new Error('回答为空')
        }
      } catch (error) {
        console.error('发送图片失败:', error)
        messages.value.push({ 
          role: 'assistant', 
          content: '抱歉，处理图片时出现错误，请重试。'
        })
      } finally {
        isLoading.value = false
        userInput.value = ''
        // 清空文件输入
        if (fileInput.value) {
          fileInput.value.value = ''
        }
      }
    }
    reader.readAsDataURL(file)
  }
}

// 加载历史记录
const loadHistory = async () => {
  try {
    console.log('加载历史记录:', sessionId.value)
    const response = await biologyApi.getHistory(sessionId.value)
    console.log('历史记录:', response)
    if (response.history) {
      messages.value = response.history
      await renderBiology()
    }
    await scrollToBottom()
  } catch (error) {
    console.error('加载历史记录失败:', error)
  }
}

// 保存会话ID到本地存储
onMounted(async () => {
  await loadMathJax()
  localStorage.setItem('sessionId', sessionId.value)
  loadHistory()
  
  // 检查是否有预设问题
  const route = useRoute()
  if (route.query.question) {
    userInput.value = route.query.question as string
    // 自动发送预设问题
    setTimeout(() => {
      sendMessage()
    }, 1000)
  }
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  width: 100vw;
  min-width: 100vw;
  background-color: #ffffff;
  display: flex;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.side-nav {
  width: 240px;
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e8e8e8;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 10;
}

.nav-header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #e8e8e8;
}

.logo-icon {
  font-size: 24px;
  line-height: 1;
  margin-right: 12px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.nav-links {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: #64748b;
  text-decoration: none;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: #f8fafc;
  color: #3b82f6;
}

.nav-link.active {
  background: #f1f5f9;
  color: #3b82f6;
}

.nav-icon {
  font-size: 1.25rem;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
}

.main-content {
  flex: 1;
  margin-left: 240px;
  min-height: 100vh;
  background: #f8fafc;
}

.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 24px;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: calc(100vh - 200px); /* 减去输入区域和其他元素的高度 */
  min-height: 200px; /* 设置最小高度 */
}

/* 自定义滚动条样式 */
.chat-history::-webkit-scrollbar {
  width: 8px;
}

.chat-history::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.chat-history::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.chat-history::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.message {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message.user .message-content {
  background: #e3f2fd;
  margin-left: auto;
}

.message.assistant .message-content {
  background: white;
  margin-right: auto;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.message-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.message-text {
  flex: 1;
  padding: 8px 0;
  color: #1e293b;
  line-height: 1.5;
}

.message-text :deep(.MathJax) {
  display: inline-block;
  margin: 0 2px;
}

.message-text :deep(.MathJax_SVG) {
  display: inline-block;
  margin: 0 2px;
}

.user-message .message-text {
  background: #e3f2fd;
}

.assistant-message .message-text {
  background: #ffffff;
  color: #1e293b;
}

.math-formula {
  display: inline-block;
  padding: 2px 4px;
  background: #f1f5f9;
  border-radius: 4px;
  font-family: 'Consolas', monospace;
}

.math-fraction {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  vertical-align: middle;
  margin: 0 2px;
}

.math-fraction .numerator {
  border-bottom: 1px solid #000;
  padding: 0 4px;
}

.math-fraction .denominator {
  padding: 0 4px;
}

.math-sqrt {
  display: inline-flex;
  align-items: center;
  margin: 0 2px;
}

.math-sqrt .radicand {
  border-top: 1px solid #000;
  padding: 0 4px;
}

.math-sum,
.math-integral {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  margin: 0 2px;
}

.math-sum .sum-range,
.math-integral .integral-range {
  font-size: 0.8em;
}

.math-limit {
  display: inline-flex;
  align-items: center;
  margin: 0 2px;
}

.math-limit .limit-expr {
  font-size: 0.8em;
  margin-left: 4px;
}

.input-area {
  flex-shrink: 0;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  resize: none;
  font-size: 1rem;
  line-height: 1.5;
  min-height: 80px;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.upload-btn,
.send-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.upload-btn {
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.upload-btn:hover {
  background: #e2e8f0;
}

.send-btn {
  background: #3b82f6;
  color: #ffffff;
  border: none;
}

.send-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.send-btn:not(:disabled):hover {
  background: #2563eb;
}

.loading {
  color: #666;
  font-style: italic;
  padding: 8px 0;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

:deep(.math-formula) {
  font-family: 'KaTeX_Math', 'Times New Roman', serif;
  font-style: italic;
}

.image-preview {
  position: relative;
  margin-top: 12px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.preview-image {
  width: 100%;
  max-height: 200px;
  object-fit: contain;
}

.remove-preview {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.remove-preview:hover {
  background: rgba(0, 0, 0, 0.7);
}

.remove-icon {
  font-size: 16px;
  line-height: 1;
}

.message-image {
  margin-bottom: 8px;
}

.message-image-preview {
  max-width: 100%;
  max-height: 200px;
  border-radius: 6px;
  object-fit: contain;
}

.message-question {
  color: #1e293b;
  line-height: 1.5;
  margin-top: 8px;
}

@media (max-width: 768px) {
  .side-nav {
    width: 60px;
  }

  .nav-header {
    padding: 0 16px;
  }

  .logo-text {
    display: none;
  }

  .nav-links {
    padding: 12px 0;
  }

  .nav-link {
    padding: 12px;
    justify-content: center;
  }

  .nav-text {
    display: none;
  }

  .main-content {
    margin-left: 60px;
  }

  .chat-container {
    padding: 16px;
  }
}

/* 添加用户信息和升级按钮样式 */
.user-section {
  padding: 16px;
  border-top: 1px solid #e8e8e8;
  margin-top: auto;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  margin-bottom: 12px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #64748b;
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.user-credits {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #64748b;
}

.credits-icon {
  color: #3b82f6;
}

.upgrade-btn {
  width: 100%;
  padding: 8px 16px;
  background: #fef3c7;
  border: none;
  border-radius: 6px;
  color: #92400e;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.upgrade-btn:hover {
  background: #fde68a;
}

.upgrade-icon {
  font-size: 16px;
}
</style> 