<template>
  <div class="ai-assistant" :style="{ left: pos.x + 'px', top: pos.y + 'px' }">
    <button
      class="fab"
      @click.prevent="onFabClick"
      @mousedown.prevent="onDown"
      @touchstart.prevent="onDown"
    >
      <img :src="botPng" alt="AI" class="bot" />
    </button>

    <transition name="panel">
      <div
        v-if="open"
        ref="panelRef"
        class="panel"
        :style="{
          left: panelPos.left + 'px',
          top: panelPos.top + 'px',
          width: panelSize.w + 'px',
          height: panelSize.h + 'px',
          position: 'fixed'
        }"
      >
        <div class="panel-header">
          <div class="ttl">
            <img :src="botPng" alt="AI" class="bot sm" />
            卡盒先生
          </div>
          <button class="close" @click="toggle">×</button>
        </div>
        <div class="panel-body">
          <div ref="scrollRef" class="messages">
            <div v-for="(m, i) in messages" :key="i" :class="['msg', m.role]">
              <div :class="['bubble', m.imageUrl ? 'has-media' : '']">
                <template v-if="m.loading">
                  <span>思考中…</span>
                  <span class="loading-spinner" aria-hidden="true"></span>
                </template>
                <template v-else>
                  <template v-if="m.imageUrl">
                    <img class="bubble-img" :src="m.imageUrl" :alt="m.imageAlt || 'image'" />
                  </template>
                  <div v-if="m.content && m.isHtml" class="bubble-text" v-html="m.content"></div>
                  <div v-else-if="m.content" class="bubble-text">{{ m.content }}</div>
                </template>
              </div>
            </div>
          </div>
          <div class="composer" role="region" aria-label="输入区">
            <!-- 图片预览区域 -->
            <div v-if="uploadedImage" class="image-preview">
              <div class="image-info">
                <img :src="uploadedImage.preview" :alt="uploadedImage.name" class="preview-img" />
                <div class="image-details">
                  <span class="image-name">{{ uploadedImage.name }}</span>
                  <span class="image-size">({{ formatFileSize(uploadedImage.size) }})</span>
                </div>
              </div>
              <button class="remove-image" @click="removeImage" title="移除图片">×</button>
            </div>
            
            <div class="composer-input">
              <textarea
                v-model="input"
                class="ipt ta"
                :placeholder="loading ? '' : (uploadedImage ? '可以继续输入文字描述...' : '输入你的问题...')"
                rows="1"
                @keydown.enter.prevent="onEnter"
              />
              <div class="composer-actions">
                <input
                  ref="imageInputRef"
                  type="file"
                  accept="image/*"
                  style="display: none"
                  @change="onImageSelect"
                />
                <button 
                  class="upload-btn" 
                  :disabled="loading" 
                  @click="triggerImageSelect"
                  title="上传图片"
                >
                  <svg viewBox="0 0 24 24" class="upload-icon">
                    <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20ZM12,11L8,15H11V19H13V15H16L12,11Z"/>
                  </svg>
                </button>
                <button class="send" :disabled="(!input && !uploadedImage) || loading" @click="send">发送</button>
              </div>
            </div>
          </div>
        </div>
        <div class="resizer" :class="handleCorner" @mousedown.prevent="onResizeDown" @touchstart.prevent="onResizeDown" />
      </div>
    </transition>
  </div>
</template>

<script setup>
/* global defineProps */
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import botPng from '@/assets/img/aibot.png'

const props = defineProps({
  baseURL: { type: String, default: '/api/v1/ai' },
  sessionId: { type: String, default: () => `web-${Math.random().toString(36).slice(2)}` }
})

const open = ref(false)
const pos = ref({ x: 0, y: 0 })
const dragging = ref(false)
let startMouseX = 0
let startMouseY = 0
let startX = 0
let startY = 0
let moved = false
const input = ref('')
const loading = ref(false)
const uploadedImage = ref(null)
const messages = ref([
  { role: 'assistant', content: '你好啊！我是你的卡盒先生，有什么生物问题快来问我吧' }
])
const scrollRef = ref(null)
const panelRef = ref(null)
const imageInputRef = ref(null)
const panelPos = ref({ left: 0, top: 0 })
const panelSize = ref({ w: 360, h: Math.round(window.innerHeight * 0.62) })
let resizing = false
let startRX = 0
let startRY = 0
let startW = 0
let startH = 0
const handleCorner = ref('br') // tl | tr | bl | br
const typingTimer = ref(null)

function toggle(){
  open.value = !open.value
  nextTick(() => { placePanel(); scrollToBottom() })
}

function onFabClick(){
  // 仅在未发生拖动时触发 toggle
  if (!moved) toggle()
}

function onDown(e){
  const ev = e.touches ? e.touches[0] : e
  dragging.value = true
  moved = false
  startMouseX = ev.clientX
  startMouseY = ev.clientY
  startX = pos.value.x
  startY = pos.value.y
  window.addEventListener('mousemove', onMove, { passive: false })
  window.addEventListener('mouseup', onUp, { passive: false })
  window.addEventListener('touchmove', onMove, { passive: false })
  window.addEventListener('touchend', onUp, { passive: false })
}

function onMove(e){
  if (!dragging.value) return
  const ev = e.touches ? e.touches[0] : e
  const dx = ev.clientX - startMouseX
  const dy = ev.clientY - startMouseY
  if (Math.abs(dx) + Math.abs(dy) > 4) moved = true
  const vw = window.innerWidth
  const vh = window.innerHeight
  const size = 60 // 近似 FAB 尺寸
  const nx = Math.min(Math.max(8, startX + dx), vw - size - 8)
  const ny = Math.min(Math.max(8, startY + dy), vh - size - 8)
  pos.value = { x: nx, y: ny }
  localStorage.setItem('aiAssistantPos', JSON.stringify(pos.value))
  if (open.value) placePanel()
}

function onUp(){
  dragging.value = false
  window.removeEventListener('mousemove', onMove)
  window.removeEventListener('mouseup', onUp)
  window.removeEventListener('touchmove', onMove)
  window.removeEventListener('touchend', onUp)
}

function onResizeDown(e){
  const ev = e.touches ? e.touches[0] : e
  resizing = true
  startRX = ev.clientX
  startRY = ev.clientY
  startW = panelSize.value.w
  startH = panelSize.value.h
  window.addEventListener('mousemove', onResizing, { passive: false })
  window.addEventListener('mouseup', onResizeUp, { passive: false })
  window.addEventListener('touchmove', onResizing, { passive: false })
  window.addEventListener('touchend', onResizeUp, { passive: false })
}

function onResizing(e){
  if (!resizing) return
  const ev = e.touches ? e.touches[0] : e
  const dx = ev.clientX - startRX
  const dy = ev.clientY - startRY
  const vw = window.innerWidth
  const vh = window.innerHeight
  const minW = 280, minH = 280
  const maxW = Math.min(1700, vw - 16)
  const maxH = Math.min(Math.round(vh * 1.0), vh - 16)
  // 根据当前手柄方向决定宽高变化方向
  let dw = dx
  let dh = dy
  if (handleCorner.value.includes('l')) dw = -dx
  if (handleCorner.value.includes('t')) dh = -dy
  const nw = Math.max(minW, Math.min(maxW, startW + dw))
  const nh = Math.max(minH, Math.min(maxH, startH + dh))
  panelSize.value = { w: nw, h: nh }
  localStorage.setItem('aiAssistantSize', JSON.stringify(panelSize.value))
  placePanel()
}

function onResizeUp(){
  resizing = false
  window.removeEventListener('mousemove', onResizing)
  window.removeEventListener('mouseup', onResizeUp)
  window.removeEventListener('touchmove', onResizing)
  window.removeEventListener('touchend', onResizeUp)
}

function scrollToBottom(){
  const el = scrollRef.value
  if (!el) return
  el.scrollTop = el.scrollHeight
}

function formatAnswer(raw){
  if (!raw) return ''
  let text = String(raw).trim()
  // 规范换行与空白
  text = text.replace(/\r\n?|\n/g, '\n').replace(/\n{3,}/g, '\n\n')
  // 清理 markdown 列表/多余符号：*, -, + 开头的项目；多余星号
  text = text.replace(/^\s*[*\-+]\s+/gm, '')
             .replace(/[*]{2,}/g, '')

  // 处理 ### 标题：本行中“### ”后的文字为标题
  text = text.replace(/^\s*#{3}\s*(.+)$/gm, (m, p1) => `<div class="h3-title">${escapeHtml(String(p1).trim())}</div>`)

  // 将所有 # 转为空格（避免残留的 markdown 井号）
  text = text.replace(/#/g, ' ')

  // 规范标题后的空行：确保每个标题块后恰好只有一行空行
  text = text.replace(/(<div class="h3-title">[\s\S]*?<\/div>)\n+/g, '\n$1\n')

  // 为疑问句加色区分：仅在文本片段内处理，避开 HTML 标签
  text = highlightQuestions(text)

  // 若没有明显分段，则按句号分段为更易读的形式（不再截断）
  if (!/\n/.test(text)) {
    const parts = text.split(/(?<=。|！|\?|？)/).map(s => s.trim()).filter(Boolean)
    if (parts.length) {
      text = parts.map((s, i) => `${i+1}. ${s}`).join('\n')
    }
  }
  // 返回 HTML 字符串
  return text
}

function escapeHtml(s){
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

function highlightQuestions(html){
  // 按标签切割，奇偶段为文本/标签交替
  const parts = html.split(/(<[^>]+>)/g)
  // 第一遍：标记每个片段是否在标题 .h3-title 内，并确定最后一个应高亮的文本片段索引
  const inTitle = new Array(parts.length).fill(false)
  let insideTitle = false
  for (let i = 0; i < parts.length; i++) {
    const token = parts[i]
    if (/^<[^>]+>$/.test(token)) {
      // 开始标题：class 中包含 h3-title
      if (/^<[^>]*class=["'][^"']*h3-title[^"']*["'][^>]*>$/i.test(token)) insideTitle = true
      // 结束标题：遇到 </div> 时退出（标题块通常单独一层）
      if (insideTitle && /^<\s*\/\s*div\s*>$/i.test(token)) insideTitle = false
    } else {
      inTitle[i] = insideTitle
    }
  }
  // 找到最后一个非空且不在标题内的文本片段
  let lastTextIdx = -1
  for (let i = parts.length - 1; i >= 0; i--) {
    if (!/^<[^>]+>$/.test(parts[i]) && !inTitle[i] && parts[i].trim().length > 0) { lastTextIdx = i; break }
  }
  // 第二遍：对非标题文本片段做问句高亮；最后一个文本片段保留最后一行
  for (let i = 0; i < parts.length; i++) {
    if (!/^<[^>]+>$/.test(parts[i]) && !inTitle[i]) {
      if (i !== lastTextIdx) {
        parts[i] = parts[i].replace(/([^。\n！!？?]+?[？?])(?=\s|$)/g, '<span class="q-text">$1</span>')
      } else {
        const lines = parts[i].split(/\n/)
        let lastLineIdx = -1
        for (let j = lines.length - 1; j >= 0; j--) { if (lines[j].trim().length > 0) { lastLineIdx = j; break } }
        for (let j = 0; j < lines.length; j++) {
          if (j === lastLineIdx) continue
          lines[j] = lines[j].replace(/([^。\n！!？?]+?[？?])(?=\s|$)/g, '<span class="q-text">$1</span>')
        }
        parts[i] = lines.join('\n')
      }
    }
  }
  return parts.join('')
}

function typeOut(targetIndex, fullText){
  // 将 messages[targetIndex].content 按逐字打印
  const step = () => {
    const cur = messages.value[targetIndex].content
    if (cur.length >= fullText.length) { typingTimer.value = null; return }
    const nextLen = Math.min(fullText.length, cur.length + Math.max(1, Math.floor(Math.random()*3+1)))
    messages.value[targetIndex].content = fullText.slice(0, nextLen)
    nextTick(scrollToBottom)
    typingTimer.value = setTimeout(step, 16 + Math.random()*40)
  }
  if (typingTimer.value) clearTimeout(typingTimer.value)
  typingTimer.value = setTimeout(step, 60)
}

function onEnter(e){
  if (e.shiftKey) {
    // 允许换行
    return
  }
  e.preventDefault()
  send()
}

function triggerImageSelect() {
  imageInputRef.value?.click()
}

function onImageSelect(event) {
  const file = event.target.files?.[0]
  if (!file) return
  
  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }
  
  // 检查文件大小 (限制为10MB)
  if (file.size > 10 * 1024 * 1024) {
    alert('图片大小不能超过10MB')
    return
  }
  
  // 创建预览URL
  const preview = URL.createObjectURL(file)
  uploadedImage.value = {
    file: file,
    name: file.name,
    size: file.size,
    preview: preview
  }
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function removeImage() {
  if (uploadedImage.value?.preview) {
    URL.revokeObjectURL(uploadedImage.value.preview)
  }
  uploadedImage.value = null
  if (imageInputRef.value) {
    imageInputRef.value.value = ''
  }
}

async function uploadImage(imageFile, questionText) {
  loading.value = true
  // 生成一份图片预览URL（若已存在则复用）
  const previewUrl = uploadedImage.value?.preview || URL.createObjectURL(imageFile)
  messages.value.push({ role: 'user', content: questionText || '', imageUrl: previewUrl, imageAlt: imageFile.name })
  const pendingIdx = messages.value.push({ role: 'assistant', content: '正在分析图片…', loading: true }) - 1
  await nextTick(); scrollToBottom()
  
  try {
    const formData = new FormData()
    formData.append('image', imageFile)
    formData.append('question', (questionText && questionText.trim()) || '请分析这张图片中的生物学内容')
    
    const res = await fetch(`${props.baseURL}/upload-image`, {
      method: 'POST',
      body: formData
    })
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}))
      throw new Error(errorData.error || '图片上传失败')
    }
    
    const data = await res.json()
    const answer = data.answer || '抱歉，无法分析这张图片。'
    const formatted = formatAnswer(answer)
    messages.value[pendingIdx].loading = false
    messages.value[pendingIdx].content = ''
    // 标记为 HTML 以启用富文本渲染
    messages.value[pendingIdx].isHtml = true
    typeOut(pendingIdx, formatted)
  } catch (e) {
    console.error('Upload error:', e)
    const fallback = `图片分析服务暂不可用，请稍后再试。错误信息：${e.message}`
    messages.value[pendingIdx].loading = false
    messages.value[pendingIdx].content = ''
    typeOut(pendingIdx, formatAnswer(fallback))
  } finally {
    loading.value = false
    await nextTick(); scrollToBottom()
    // 清空图片输入和状态
    removeImage()
  }
}



async function send(){
  if ((!input.value && !uploadedImage.value) || loading.value) return
  
  if (uploadedImage.value) {
    const question = input.value.trim()
    input.value = ''
    await uploadImage(uploadedImage.value.file, question)
  } else {
    const question = input.value.trim()
    input.value = ''
    await sendText(question)
  }
}

async function sendText(question) {
  messages.value.push({ role: 'user', content: question })
  loading.value = true
  const pendingIdx = messages.value.push({ role: 'assistant', content: '思考中…', loading: true }) - 1
  await nextTick(); scrollToBottom()
  try {
    const res = await fetch(`${props.baseURL}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, session_id: props.sessionId })
    })
    if (!res.ok) throw new Error('网络错误')
    const data = await res.json()
    const answer = data.answer || '抱歉，暂时无法回答。'
    const formatted = formatAnswer(answer)
    messages.value[pendingIdx].loading = false
    messages.value[pendingIdx].content = ''
    messages.value[pendingIdx].isHtml = true
    typeOut(pendingIdx, formatted)
  } catch (e) {
    const fallback = '服务暂不可用，已切换到示例回答：\n1. 细胞膜的主要成分是磷脂双分子层与蛋白质。\n2. 膜蛋白包括外周蛋白与整合蛋白，承担物质转运与信号传导。'
    messages.value[pendingIdx].loading = false
    messages.value[pendingIdx].content = ''
    typeOut(pendingIdx, formatAnswer(fallback))
  } finally {
    loading.value = false
    await nextTick(); scrollToBottom()
  }
}

onMounted(() => {
  // 读取上次位置，默认右下角，并适配不同屏幕尺寸
  try {
    const saved = localStorage.getItem('aiAssistantPos')
    if (saved) {
      const p = JSON.parse(saved)
      // 验证保存的位置是否在当前屏幕范围内
      const vw = window.innerWidth
      const vh = window.innerHeight
      const btnSize = 60
      const margin = 20
      const maxX = vw - btnSize - margin
      const maxY = vh - btnSize - margin
      pos.value = { 
        x: Math.min(Math.max(margin, p.x || 0), maxX), 
        y: Math.min(Math.max(margin, p.y || 0), maxY) 
      }
    } else {
      // 默认右下角位置，适配不同屏幕
      const vw = window.innerWidth
      const vh = window.innerHeight
      const btnSize = 60
      const margin = 20
      pos.value = { 
        x: vw - btnSize - margin, 
        y: vh - btnSize - margin 
      }
    }
  } catch {
    // 异常情况下的默认位置
    const vw = window.innerWidth
    const vh = window.innerHeight
    const btnSize = 60
    const margin = 20
    pos.value = { 
      x: vw - btnSize - margin, 
      y: vh - btnSize - margin 
    }
  }
  try {
    const ss = localStorage.getItem('aiAssistantSize')
    if (ss) {
      const s = JSON.parse(ss)
      // 适配不同屏幕尺寸的面板大小
      const vw = window.innerWidth
      const vh = window.innerHeight
      const maxW = Math.min(400, vw * 0.9)
      const maxH = Math.min(vh * 0.8, vh - 100)
      panelSize.value = { 
        w: Math.min(s.w || 360, maxW), 
        h: Math.min(s.h || Math.round(vh * 0.62), maxH) 
      }
    } else {
      // 默认面板大小，适配不同屏幕
      const vw = window.innerWidth
      const vh = window.innerHeight
      const maxW = Math.min(400, vw * 0.9)
      const maxH = Math.min(vh * 0.8, vh - 100)
      panelSize.value = { 
        w: Math.min(360, maxW), 
        h: Math.min(Math.round(vh * 0.62), maxH) 
      }
    }
  } catch {
    // 异常情况下的默认面板大小
    const vw = window.innerWidth
    const vh = window.innerHeight
    const maxW = Math.min(400, vw * 0.9)
    const maxH = Math.min(vh * 0.8, vh - 100)
    panelSize.value = { 
      w: Math.min(360, maxW), 
      h: Math.min(Math.round(vh * 0.62), maxH) 
    }
  }
  scrollToBottom()
  window.addEventListener('resize', placePanel)
  // 监听窗口大小变化，重新计算位置和大小
  window.addEventListener('resize', () => {
    const vw = window.innerWidth
    const vh = window.innerHeight
    const btnSize = 60
    const margin = 20
    const maxX = vw - btnSize - margin
    const maxY = vh - btnSize - margin
    
    // 只在超出边界时才调整，保持用户设置的位置
    if (pos.value.x > maxX) pos.value.x = maxX
    if (pos.value.y > maxY) pos.value.y = maxY
    if (pos.value.x < margin) pos.value.x = margin
    if (pos.value.y < margin) pos.value.y = margin
    
    // 调整面板大小以适应新屏幕
    const maxW = Math.min(400, vw * 0.9)
    const maxH = Math.min(vh * 0.8, vh - 100)
    if (panelSize.value.w > maxW) panelSize.value.w = maxW
    if (panelSize.value.h > maxH) panelSize.value.h = maxH
    
    // 重新计算面板位置，但不改变FAB按钮位置
    placePanel()
    
    // 保存调整后的位置到localStorage
    localStorage.setItem('aiAssistantPos', JSON.stringify(pos.value))
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', placePanel)
  window.removeEventListener('mousemove', onMove)
  window.removeEventListener('mouseup', onUp)
  window.removeEventListener('touchmove', onMove)
  window.removeEventListener('touchend', onUp)
  window.removeEventListener('mousemove', onResizing)
  window.removeEventListener('mouseup', onResizeUp)
  window.removeEventListener('touchmove', onResizing)
  window.removeEventListener('touchend', onResizeUp)
  if (typingTimer.value) {
    clearTimeout(typingTimer.value)
    typingTimer.value = null
  }
  // 清理图片预览URL
  if (uploadedImage.value?.preview) {
    URL.revokeObjectURL(uploadedImage.value.preview)
  }
})

function placePanel(){
  const vw = window.innerWidth
  const vh = window.innerHeight
  const btnSize = 60
  const gap = 10
  let pw = panelSize.value.w || 360
  let ph = panelSize.value.h || Math.round(vh * 0.62)
  const el = panelRef.value
  if (el) {
    const rect = el.getBoundingClientRect()
    if (rect.width) pw = rect.width
    if (rect.height) ph = rect.height
  }

  // 计算四向可用空间
  const leftSpace = pos.value.x - gap
  const rightSpace = vw - (pos.value.x + btnSize + gap)
  const topSpace = pos.value.y - gap
  const bottomSpace = vh - (pos.value.y + btnSize + gap)

  // 选择水平放置方向：优先能容纳 pw 的一侧；若两侧都能容纳，选空间更大的一侧；否则贴边并裁剪
  let placeRight = rightSpace >= pw || rightSpace >= leftSpace
  if (leftSpace >= pw && rightSpace < pw) placeRight = false

  // 选择垂直放置方向：优先能容纳 ph 的一侧；若两侧都能容纳，选空间更大的一侧；否则贴边并裁剪
  let placeBelow = bottomSpace >= ph || bottomSpace >= topSpace
  if (topSpace >= ph && bottomSpace < ph) placeBelow = false

  // 计算位置
  let left = placeRight ? (pos.value.x + btnSize + gap) : (pos.value.x - pw - gap)
  let top = placeBelow ? (pos.value.y + btnSize + gap) : (pos.value.y - ph - gap)

  // 边界修正
  left = Math.max(8, Math.min(left, vw - pw - 8))
  top = Math.max(8, Math.min(top, vh - ph - 8))
  panelPos.value = { left, top }
  // 依据相对位置选择更合适的拖拽手柄角
  const cx = pos.value.x + 30 // 按钮中心大致 x
  const cy = pos.value.y + 30 // 按钮中心大致 y
  const px = left + panelSize.value.w / 2
  const py = top + panelSize.value.h / 2
  const rightSide = px >= cx
  const bottomSide = py >= cy
  handleCorner.value = (bottomSide ? 'b' : 't') + (rightSide ? 'r' : 'l')

  // 注意：placePanel函数只负责计算面板位置，不改变FAB按钮位置
  // FAB按钮位置的边界检查在resize事件监听器中处理
}
</script>

<style scoped>
.ai-assistant { position: fixed; z-index: 4000; pointer-events: none; }
.ai-assistant > * { pointer-events: auto; }
.fab { width: 52px; height: 52px; border-radius: 50%; border: none; background: linear-gradient(135deg,#fcfcfc,#797a7a); color: #fff; box-shadow: 0 8px 18px rgba(187, 187, 187, 0.594); cursor: pointer; display: grid; place-items: center; transition: transform .18s ease, box-shadow .18s ease; position: relative; overflow: hidden; padding: 0; }
.fab:hover { transform: translateY(-2px) scale(1.14); box-shadow: 0 12px 24px rgba(154, 154, 154, 0.594); }
.bot { width: 22px; height: 22px; }
.bot.sm { width: 24px; height: 24px; }
/* 放大浮动按钮中的图标至与圆形外圈重合 */
.fab .bot { position: absolute; inset: 0; width: 100%; height: 100%; border-radius: 50%; object-fit: cover; display: block; }

.panel-enter-active, .panel-leave-active { transition: opacity .22s ease, transform .22s ease; }
.panel-enter-from, .panel-leave-to { opacity: 0; transform: translateY(8px); }

.panel { width: min(360px, 86vw); height: 62vh; background: #fff; border-radius: 14px; box-shadow: 0 18px 40px rgba(0,0,0,.16); overflow: hidden; display: flex; flex-direction: column; }
.resizer { position: absolute; width: 16px; height: 16px; border-radius: 4px; background: linear-gradient(135deg, rgba(16,185,129,.25), rgba(16,185,129,.12)); }
.resizer.br { right: 6px; bottom: 6px; cursor: nwse-resize; }
.resizer.bl { left: 6px; bottom: 6px; cursor: nesw-resize; }
.resizer.tr { right: 6px; top: 6px; cursor: nesw-resize; }
.resizer.tl { left: 6px; top: 6px; cursor: nwse-resize; }
.panel-header { height: 48px; display: flex; align-items: center; justify-content: space-between; padding: 0 12px 0 14px; background: linear-gradient(180deg, rgba(16,185,129,.06), rgba(16,185,129,.02)); border-bottom: 1px solid rgba(16,185,129,.12); }
.ttl { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; color: #065f46; }
.close { width: 28px; height: 28px; border-radius: 8px; border: none; background: transparent; color: #065f46; cursor: pointer; font-size: 18px; }
.close:hover { background: rgba(16,185,129,.08); }

.panel-body { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.messages { flex: 1; min-height: 0; padding: 12px; overflow-y: auto; background: linear-gradient(180deg, #f6fffb 0%, #ffffff 100%); overscroll-behavior: contain; }
.msg { display: flex; margin: 8px 0; }
.msg.user { justify-content: flex-end; }
.bubble { max-width: 78%; padding: 10px 12px; border-radius: 12px; line-height: 1.6; font-size: 14px; box-shadow: 0 2px 8px rgba(0,0,0,.06); white-space: pre-wrap; }
.bubble.has-media { padding: 8px; }
.bubble-img { width: 100%; max-width: 220px; border-radius: 10px; display: block; object-fit: cover; }
.msg.user .bubble-img { margin-left: auto; }
.bubble-text { margin-top: 3px; }
.bubble-text :deep(.q-text) { color: #ff4242be; font-weight: 600; }
.bubble-text :deep(.h3-title) { font-weight: 900; font-size: 20px; line-height: 1.35; margin: 6px 0 4px; color: #064e3b; letter-spacing: .2px; }
.msg.assistant .bubble { background: #f0fdf4; border: 1px solid rgba(16,185,129,.2); color: #065f46; }
.msg.user .bubble { background: #eff6ff; border: 1px solid rgba(59,130,246,.2); color: #1e40af; }

.composer { display: flex; flex-direction: column; gap: 8px; padding: 10px; border-top: 1px solid rgba(16,185,129,.12); background: #fff; }

.image-preview {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 12px; background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border: 1px solid rgba(59,130,246,.2); border-radius: 10px;
  animation: slideDown .3s ease;
}
.image-info { display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0; }
.preview-img { width: 40px; height: 40px; border-radius: 8px; object-fit: cover; flex-shrink: 0; }
.image-details { display: flex; flex-direction: column; min-width: 0; }
.image-name { font-size: 13px; font-weight: 600; color: #1e40af; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.image-size { font-size: 12px; color: #6b7280; }
.remove-image { 
  width: 20px; height: 20px; border-radius: 50%; border: none; 
  background: rgba(239,68,68,.1); color: #dc2626; cursor: pointer;
  display: flex; align-items: center; justify-content: center; font-size: 14px;
  transition: all .2s ease; flex-shrink: 0;
}
.remove-image:hover { background: rgba(239,68,68,.2); transform: scale(1.1); }

.composer-input { display: flex; gap: 8px; }
.ipt { flex: 1; border-radius: 12px; border: 2px solid #e5e7eb; padding: 5px 6px; outline: none; transition: box-shadow .2s ease, border-color .2s ease; }
.ipt.ta {  max-height: 120px; resize: none; line-height: 1.4; }
.ipt:focus { border-color: #34d399; box-shadow: 0 0 0 3px rgba(16,185,129,.12); }

.composer-actions { display: flex; gap: 6px; align-items: center; }
.upload-btn { 
  width: 32px; height: 32px; border-radius: 12px; border: none; 
  background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
  color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all .2s ease; box-shadow: 0 4px 8px rgba(59,130,246,.3);
}
.upload-btn:hover { 
  background: linear-gradient(135deg, #1d4ed8, #1e40af); 
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(59,130,246,.4);
}
.upload-btn:disabled { 
  opacity: .5; cursor: not-allowed; transform: none; 
  box-shadow: 0 2px 4px rgba(59,130,246,.2);
}
.upload-icon { width: 18px; height: 18px; }

.send { height: 32px; padding: 0 16px; border-radius: 12px; border: none; background: linear-gradient(135deg,#10b981,#34d399); color: #fff; font-weight: 700; cursor: pointer; box-shadow: 0 8px 16px rgba(16,185,129,.24); }
.send:disabled { opacity: .6; cursor: not-allowed; box-shadow: none; }

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}



/* Loading 动画（圆形旋转） */
.loading-spinner { display: inline-block; width: 14px; height: 14px; margin-left: 8px; border-radius: 50%; border: 2px solid rgba(6,95,70,.22); border-top-color: rgba(16,185,129,.9); animation: spin 0.8s linear infinite; vertical-align: -2px; }
@keyframes spin { to { transform: rotate(360deg) } }
</style>

