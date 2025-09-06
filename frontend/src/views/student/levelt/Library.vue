<template>
  <div class="g-scroll"></div>
    <div class="g-wrapper">
    <div class="g-mask"></div>
    <div class="g-inner" ref="innerRef">
        <div class="g-item" v-for="(item, idx) in items" :key="idx" @click="openNew(item.url)">
          <div class="g-title">{{ item.title }}</div>
        </div>
    </div>
</div>
<teleport to="body">
  <div v-if="showViewer" class="ppt-modal" @click.self="closePpt">
    <div class="ppt-dialog">
      <button class="ppt-close" @click="closePpt">×</button>
      <div class="top-actions">
        <button class="open-new" v-if="officeUrl" @click.stop="openNew">在新标签打开PDF</button>
      </div>
      <iframe v-if="viewerMode==='office' && officeUrl" class="ppt-frame" :src="officeUrl" frameborder="0" allowfullscreen></iframe>
      <div v-else class="slides">
        <img v-if="slides.length" class="slide-img" :src="slides[current]" alt="slide" />
        <div v-else class="slide-empty">未找到本地幻灯片图片</div>
        <button class="nav prev" @click="prev" :disabled="!slides.length">‹</button>
        <button class="nav next" @click="next" :disabled="!slides.length">›</button>
        <div class="pager" v-if="slides.length">{{ current + 1 }} / {{ slides.length }}</div>
      </div>
    </div>
  </div>
</teleport>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const innerRef = ref(null)
let phase = 0
let target = 0
let raf = 0
const speed = 0.13
const minPhase = 0
let maxPhase = 0

const showViewer = ref(false)
const viewerMode = ref('office')
const officeUrl = ref('')
const slides = ref([])
const current = ref(0)

// 通过数据驱动卡片的标题与PDF路径，便于后期单独修改
const items = ref([
  { title: '光合作用与能量转化', url: '/ppt/光合作用与能量转化.pdf' },
  { title: '光合作用与能量转化', url: '/ppt/光合作用与能量转化.pdf' },
  { title: '光合作用与能量转化', url: '/ppt/光合作用与能量转化.pdf' },
  { title: '光合作用与能量转化', url: '/ppt/光合作用与能量转化.pdf' },
  { title: '光合作用与能量转化', url: '/ppt/光合作用与能量转化.pdf' },
  { title: '光合作用与能量转化', url: '/ppt/光合作用与能量转化.pdf' }
])

function openPpt(){ showViewer.value = true; viewerMode.value = officeUrl.value ? 'office' : 'local' }
function closePpt(){ showViewer.value = false }
function buildPdfUrl(path){ return path + '#toolbar=1&navpanes=0&statusbar=0&view=FitH' }
function openNew(url){ const link = url ? buildPdfUrl(url) : officeUrl.value; if (link) window.open(link, '_blank') }
function next(){ if (slides.value.length) current.value = (current.value + 1) % slides.value.length }
function prev(){ if (slides.value.length) current.value = (current.value - 1 + slides.value.length) % slides.value.length }

function onKey(e){
  if (!showViewer.value) return
  if (e.key === 'ArrowRight') next()
  else if (e.key === 'ArrowLeft') prev()
  else if (e.key === 'Escape') closePpt()
}

function clamp(v,a,b){ return Math.max(a, Math.min(b, v)) }

function onWheel(e){
  e.preventDefault()
  target = clamp(target + (e.deltaY||0) * speed, minPhase, maxPhase)
  tick()
}

function tick(){
  cancelAnimationFrame(raf)
  phase += (target - phase) * 0.06
  const el = innerRef.value
  if (el) el.style.setProperty('--phase', `${Math.round(phase)}px`)
  if (Math.abs(target - phase) > 0.5){ raf = requestAnimationFrame(tick) }
}

function onResize(){
  const vh = window.innerHeight
  // 最大推进距离与视口相关，留出 150px 余量
  maxPhase = Math.round(vh + 150)
}

onMounted(async () => {
  document.body.style.overflow = 'hidden'
  onResize()
  // 初始化更近的起始距离并立即应用，避免首屏错位
  phase = target = Math.min(280, maxPhase)
  const elInit = innerRef.value
  if (elInit) elInit.style.setProperty('--phase', `${Math.round(phase)}px`)

  // 使用本地静态资源路径（public）直接打开PDF
  const publicPdf = '/ppt/光合作用与能量转化.pdf'
  officeUrl.value = buildPdfUrl(publicPdf)

  // // 载入本地图片作为降级方案
  // try {
  //   const req = require.context('../../../assets/img/pdf1.png', false, /\.(png|jpe?g)$/)
  //   const keys = req.keys().sort((a,b) => a.localeCompare(b, 'zh-Hans-CN', { numeric:true }))
  //   slides.value = keys.map(k => req(k))
  // } catch (err) {
  //   slides.value = []
  // }

  window.addEventListener('resize', onResize, { passive:true })
  window.addEventListener('wheel', onWheel, { passive:false })
  window.addEventListener('keydown', onKey)
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  window.removeEventListener('resize', onResize)
  window.removeEventListener('wheel', onWheel)
  window.removeEventListener('keydown', onKey)
  if (raf) cancelAnimationFrame(raf)
})
</script>

<style scoped>
html, body {
    width: 100%;
    height: 100%;
    display: flex;
    overflow: hidden;
}
.g-scroll {
    width: 100%;
    height: 100vh;
    overflow-x: hidden;
    position: relative;
    overflow-y: hidden;
    scrollbar-width: none;
    -ms-overflow-style: none;
}
.g-scroll::-webkit-scrollbar {
    width: 0;
    height: 0;
    display: none;
}
.g-wrapper {
    position: fixed;
    top: -25%;
    width: 100vw;
    height: 90vh;
    perspective: 200px;
    transform-style: preserve-3d;
}

.g-inner {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 10px;
    transform-style: preserve-3d;
    transform: translateY(calc(-50% + 100px)) translateZ(var(--phase)) rotateX(90deg);
    transform-origin: bottom center;
}

.g-title {
    position: relative;
    top: -24px;
    font-size: 10px;
    font-weight: 700;
    color: #000000;
    text-shadow: 0 2px 6px rgba(0,0,0,0.35);
    pointer-events: none;
}

/* 每张卡片上的标题样式，显示在图片上方 */
.g-item > .g-title {
    position: absolute;
    top: -18px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 12px;
    font-weight: 700;
    color: #000000;
    text-shadow: 0 1px 2px rgba(255,255,255,0.6);
    white-space: nowrap;
}

.g-item {
    position: relative;
    width: 200px;
    height: 150px;
    background: url('@/assets/img/pdf1.png') center / contain no-repeat #000;
    transform: rotateX(-90deg) scale(1.1);
    transition: transform 200ms ease;
    will-change: transform;
    border-radius: 8px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.25);
    cursor: pointer;
}
.g-item:hover {
    transform: rotateX(-90deg) translateY(-12px) scale(1.2);
}
.g-mask {
    position: fixed;
    width: 100vw;
    height: 100vh;
    backdrop-filter: blur(40px);
    transform: translateZ(0);
}

.ppt-modal {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
}
.ppt-dialog {
    position: relative;
    width: 90vw;
    height: 85vh;
    background: #000;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}
.ppt-close {
    position: absolute;
    top: 8px;
    right: 10px;
    width: 36px;
    height: 36px;
    border: none;
    border-radius: 18px;
    background: rgba(255,255,255,0.9);
    color: #000;
    font-size: 22px;
    line-height: 36px;
    cursor: pointer;
    z-index: 2;
}
.ppt-frame { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
.slides { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background:#111; }
.slide-img { max-width: 100%; max-height: 100%; object-fit: contain; }
.nav { position: absolute; top: 50%; transform: translateY(-50%); width: 44px; height: 44px; border-radius: 22px; border: none; background: rgba(255,255,255,0.9); color: #000; font-size: 24px; cursor: pointer; }
.prev { left: 12px; }
.next { right: 12px; }
.pager { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); color: #fff; background: rgba(0,0,0,0.4); padding: 4px 10px; border-radius: 12px; font-size: 12px; }
.top-actions { position: absolute; top: 10px; left: 12px; z-index: 3; }
.open-new { height: 32px; padding: 0 10px; border: none; border-radius: 6px; background: rgba(255,255,255,0.9); color: #000; cursor: pointer; }
</style>