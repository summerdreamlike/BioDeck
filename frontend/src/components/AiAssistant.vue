<template>
  <div class="ai-assistant" :style="{ left: pos.x + 'px', top: pos.y + 'px' }">
    <button
      class="fab"
      @click.prevent="onFabClick"
      @mousedown.prevent="onDown"
      @touchstart.prevent="onDown"
    >
      <svg viewBox="0 0 24 24" class="bot"><path fill="currentColor" d="M12 2a1 1 0 0 1 1 1v1.055A7.002 7.002 0 0 1 19 11v4a5 5 0 0 1-5 5h-4a5 5 0 0 1-5-5v-4a7.002 7.002 0 0 1 6-6.945V3a1 1 0 0 1 1-1Zm-5 9a1 1 0 1 0 0 2h1a1 1 0 1 0 0-2H7Zm9 0h-1a1 1 0 1 0 0 2h1a1 1 0 1 0 0-2ZM9 16a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2H9Z"/></svg>
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
            <svg viewBox="0 0 24 24" class="bot sm"><path fill="currentColor" d="M12 2a1 1 0 0 1 1 1v1.055A7.002 7.002 0 0 1 19 11v4a5 5 0 0 1-5 5h-4a5 5 0 0 1-5-5v-4a7.002 7.002 0 0 1 6-6.945V3a1 1 0 0 1 1-1Z"/></svg>
            生物 AI 助手
          </div>
          <button class="close" @click="toggle">×</button>
        </div>
        <div class="panel-body">
          <div ref="scrollRef" class="messages">
            <div v-for="(m, i) in messages" :key="i" :class="['msg', m.role]">
              <div class="bubble">
                <template v-if="m.loading">
                  <span>思考中…</span>
                  <span class="loading-spinner" aria-hidden="true"></span>
                </template>
                <template v-else>
                  {{ m.content }}
                </template>
              </div>
            </div>
          </div>
          <div class="composer" role="region" aria-label="输入区">
            <textarea
              v-model="input"
              class="ipt ta"
              :placeholder="loading ? '' : ''"
              rows="1"
              @keydown.enter.prevent="onEnter"
            />
            <button class="send" :disabled="!input || loading" @click="send">发送</button>
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
const messages = ref([
  { role: 'assistant', content: '你好，我是生物 AI 助手。可以问我细胞、遗传、生态等问题～' }
])
const scrollRef = ref(null)
const panelRef = ref(null)
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
  // 若没有明显分段，则按句号分段为更易读的形式（不再截断）
  if (!/\n/.test(text)) {
    const parts = text.split(/(?<=。|！|\?|？)/).map(s => s.trim()).filter(Boolean)
    if (parts.length) {
      text = parts.map((s, i) => `${i+1}. ${s}`).join('\n')
    }
  }
  return text
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

async function send(){
  if (!input.value || loading.value) return
  const question = input.value.trim()
  input.value = ''
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
  // 读取上次位置，默认右下角
  try {
    const saved = localStorage.getItem('aiAssistantPos')
    if (saved) {
      const p = JSON.parse(saved)
      pos.value = { x: p.x || 0, y: p.y || 0 }
    } else {
      pos.value = { x: window.innerWidth - 80, y: window.innerHeight - 90 }
    }
  } catch {
    pos.value = { x: window.innerWidth - 80, y: window.innerHeight - 90 }
  }
  try {
    const ss = localStorage.getItem('aiAssistantSize')
    if (ss) {
      const s = JSON.parse(ss)
      panelSize.value = { w: s.w || 360, h: s.h || Math.round(window.innerHeight * 0.62) }
    }
  } catch {
    panelSize.value = { w: 360, h: Math.round(window.innerHeight * 0.62) }
  }
  scrollToBottom()
  window.addEventListener('resize', placePanel)
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
}
</script>

<style scoped>
.ai-assistant { position: fixed; z-index: 4000; pointer-events: none; }
.ai-assistant > * { pointer-events: auto; }
.fab { width: 52px; height: 52px; border-radius: 50%; border: none; background: linear-gradient(135deg,#10b981,#34d399); color: #fff; box-shadow: 0 8px 18px rgba(16,185,129,.28); cursor: pointer; display: grid; place-items: center; transition: transform .18s ease, box-shadow .18s ease; }
.fab:hover { transform: translateY(-2px); box-shadow: 0 12px 24px rgba(16,185,129,.34); }
.bot { width: 22px; height: 22px; }
.bot.sm { width: 18px; height: 18px; }

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
.msg.assistant .bubble { background: #f0fdf4; border: 1px solid rgba(16,185,129,.2); color: #065f46; }
.msg.user .bubble { background: #eff6ff; border: 1px solid rgba(59,130,246,.2); color: #1e40af; }

.composer { display: flex; gap: 8px; padding: 10px; border-top: 1px solid rgba(16,185,129,.12); background: #fff; }
.ipt { flex: 1; border-radius: 12px; border: 1px solid #e5e7eb; padding: 3px 12px; outline: none; transition: box-shadow .2s ease, border-color .2s ease; }
.ipt.ta {  max-height: 120px; resize: none; line-height: 1.4; }
.ipt:focus { border-color: #34d399; box-shadow: 0 0 0 3px rgba(16,185,129,.12); }
.send { height: 30px; padding: 0 14px; border-radius: 12px; border: none; background: linear-gradient(135deg,#10b981,#34d399); color: #fff; font-weight: 700; cursor: pointer; box-shadow: 0 8px 16px rgba(16,185,129,.24); }
.send:disabled { opacity: .6; cursor: not-allowed; box-shadow: none; }

/* Loading 动画（圆形旋转） */
.loading-spinner { display: inline-block; width: 14px; height: 14px; margin-left: 8px; border-radius: 50%; border: 2px solid rgba(6,95,70,.22); border-top-color: rgba(16,185,129,.9); animation: spin 0.8s linear infinite; vertical-align: -2px; }
@keyframes spin { to { transform: rotate(360deg) } }
</style>

