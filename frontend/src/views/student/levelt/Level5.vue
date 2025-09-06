<template>
  <div class="level5-wrap">
    <button class="library-fixed" @click="goLibrary" aria-label="生物图书馆">
      <img :src="srcLibrary" class="library-icon" alt="library" />
      <span class="library-text">生物图书馆</span>
    </button>
    <div class="map" ref="mapRef" :style="{ width: mapWidth + 'px', height: mapHeight + 'px' }">
    <div class="background-image"></div>
      <svg class="links" :viewBox="svgViewBox" preserveAspectRatio="none">
        <template v-for="(seg, i) in segments" :key="i">
          <path :d="seg.d" class="seg" />
        </template>
      </svg>
      <div v-for="n in 20" :key="n" class="node"
           :class="nodeClass(n)"
           :style="nodeStyle(n)"
           @click="onNodeClick(n)"
           @mouseenter="hover=n" @mouseleave="hover=0">
        <img :src="imgFor(n)" class="btn-img" :alt="`关卡5-${n}`" />
        <div class="label"><strong>5-{{ n }}</strong></div>
        <span v-if="n===20" class="tag">BOSS</span>
      </div>
    </div>

    <!-- 完成提示弹窗 -->
    <div v-if="showModal" class="modal" @click="showModal=false">
      <div class="modal-card" @click.stop>
        <div class="modal-title">已完成</div>
        <div class="modal-body">{{ modalText }}</div>
        <button class="modal-ok" @click="showModal=false">好的</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const mapRef = ref(null)
const hover = ref(0)

// 视口高度和地图高度（减去顶部 75px）
const viewportH = ref(window.innerHeight)
const mapHeight = computed(() => Math.max(300, viewportH.value - 75))

function onResize(){ viewportH.value = window.innerHeight }

// 起伏参数
const amplitude = computed(() => Math.round(mapHeight.value * 0.08))
const cycles = 2.6
const omega = (2 * Math.PI * cycles) / 19
const phase = -Math.PI / 2

// 节点间距与基线
const stepX = 360
const nodeSize = 120
const baseY = computed(() => Math.round(mapHeight.value * 0.458))

// 交替上下排列
function posOf(n){
  const i = n - 1
  const x = i * stepX + 120
  const offset = (i % 2 === 0) ? -amplitude.value : amplitude.value
  const y = baseY.value + offset
  return { x, y }
}

function catmullRomToBezier(p0, p1, p2, p3, t = 0.25){
  const c1x = p1.x + (p2.x - p0.x) * t
  const c1y = p1.y + (p2.y - p0.y) * t
  const c2x = p2.x - (p3.x - p1.x) * t
  const c2y = p2.y - (p3.y - p1.y) * t
  return { c1x, c1y, c2x, c2y }
}

const segments = computed(()=>{
  const arr = []
  for (let i=1;i<20;i++){
    const p0 = i-1 >= 1 ? posOf(i-1) : posOf(i)
    const p1 = posOf(i)
    const p2 = posOf(i+1)
    const p3 = i+2 <= 20 ? posOf(i+2) : posOf(i+1)
    const { c1x, c1y, c2x, c2y } = catmullRomToBezier(p0, p1, p2, p3, 0.25)
    const d = `M ${p1.x} ${p1.y} C ${c1x} ${c1y}, ${c2x} ${c2y}, ${p2.x} ${p2.y}`
    arr.push({ d })
  }
  return arr
})

const mapWidth = computed(()=>{ const last = posOf(20); return last.x + 220 })
const svgViewBox = computed(()=>`0 0 ${mapWidth.value} ${mapHeight.value}`)

const completed = new Set((() => { const arr = Array.from({length:18}, (_,i)=>i+1); try { const forceReset = localStorage.getItem('force-level5-19-reset') === '1'; if (!forceReset && localStorage.getItem('level5-19-complete') === '1') arr.push(19); if (localStorage.getItem('level5-20-complete') === '1') arr.push(20) } catch(e) { /* ignore */ } return arr })())

function nodeClass(n){
  return { done: completed.has(n), boss: n===20, hover: hover.value===n }
}

function nodeStyle(n){
  const p = posOf(n)
  return {
    left: (p.x - 42) + 'px',
    top: (p.y - 45) + 'px'
  }
}

// 按钮图案（运行时动态载入，避免模块缺失崩溃）
const placeholder = new URL('@/assets/img/Logo.png', import.meta.url).href
const srcBtn2 = ref(placeholder)
const srcBtn1 = ref(placeholder)
const srcBoss = ref(placeholder)
const srcLibrary = ref(placeholder)

onMounted(async () => {
  try { const m = await import('@/assets/img/levelt/button-2.png'); srcBtn2.value = (m && (m.default || m)) } catch (e) { console.warn('button-2.png not found, using placeholder') }
  try { const m = await import('@/assets/img/levelt/button-1.png'); srcBtn1.value = (m && (m.default || m)) } catch (e) { console.warn('button-1.png not found, using placeholder') }
  try { const m = await import('@/assets/img/levelt/button-boss.png'); srcBoss.value = (m && (m.default || m)) } catch (e) { console.warn('button-boss.png not found, using placeholder') }
  try { const m = await import('@/assets/img/levelt/library.png'); srcLibrary.value = (m && (m.default || m)) } catch (e) {
    // 内置透明SVG书本占位
    srcLibrary.value = 'data:image/svg+xml;utf8,%3Csvg xmlns%3D%22http%3A//www.w3.org/2000/svg%22 width%3D%2272%22 height%3D%2272%22 viewBox%3D%220 0 72 72%22%3E%3Cg fill%3D%22none%22 stroke%3D%22%232783f6%22 stroke-width%3D%224%22%3E%3Crect x%3D%2212%22 y%3D%2214%22 rx%3D%228%22 ry%3D%228%22 width%3D%2222%22 height%3D%2244%22/%3E%3Crect x%3D%2238%22 y%3D%2214%22 rx%3D%228%22 ry%3D%228%22 width%3D%2222%22 height%3D%2244%22/%3E%3Cpath d%3D%22M12 22h22M38 22h22%22/%3E%3C/g%3E%3C/svg%3E'
  }
})

function imgFor(n){
  if (n <= 18) return srcBtn2.value
  if (n === 19) return srcBtn1.value
  return srcBoss.value
}

// 完成弹窗
const showModal = ref(false)
const modalText = ref('')

function onNodeClick(n){
  if (n<=18){
    modalText.value = `关卡5-${n} 已完成，请继续下一关！`
    showModal.value = true
    return
  }
  if (n===19){ if (completed.has(19)) { modalText.value = `关卡5-19 已完成，请继续下一关！`; showModal.value = true; return } router.push('/StudentSide/levelt/level5-19'); return }
  if (n===20){ if (completed.has(20)) { modalText.value = `关卡5-20 已完成，恭喜通关！`; showModal.value = true; return } router.push('/StudentSide/levelt/level5-20') }
}

function goLibrary(){ router.push('/StudentSide/levelt/library') }

let wheelHandler
let wrapper
onMounted(()=>{
  window.addEventListener('resize', onResize)
  wrapper = document.querySelector('.level5-wrap')
  if (wrapper){
    wrapper.classList.add('h-scroll-container')
    wheelHandler = (e)=>{
      if (e.ctrlKey) return
      if (Math.abs(e.deltaY) >= Math.abs(e.deltaX)){
        wrapper.scrollLeft += e.deltaY
        e.preventDefault()
      }
    }
    wrapper.addEventListener('wheel', wheelHandler, { passive:false })
  }
})

onBeforeUnmount(()=>{
  window.removeEventListener('resize', onResize)
  if (wrapper){
    wrapper.removeEventListener('wheel', wheelHandler)
    wrapper.classList.remove('h-scroll-container')
  }
})
</script>

<style scoped>
.level5-wrap { position: relative; height: calc(100vh - 75px); overflow-y: hidden; overflow-x: auto; }
.background-image { position: absolute; left: 0; bottom: 0; width: 100%; height: 100%; background-image: url('@/assets/img/levelt/levelt5-background.jpg'); background-size: auto 100%; background-repeat: repeat-x; background-position: 0 0; z-index: 0; }

.library-fixed { position: fixed; left: 22px; top: 46px; z-index: 6; padding: 0; border: none; background: transparent; cursor: pointer; }
.library-icon { width: 72px; height: 72px; object-fit: contain; display: block; filter: drop-shadow(0 8px 18px rgba(0,0,0,.22)); transition: transform .18s ease, filter .18s ease; }
.library-fixed:hover .library-icon { transform: translateY(-2px) scale(1.06); filter: drop-shadow(0 12px 26px rgba(0,0,0,.28)); }
.library-text{font-size: 14px; color: #1d1d1dad; font-weight: 600;}

.map { position: relative; min-width: 1200px; z-index: 1; }
.links { position: absolute; inset: 0; pointer-events: none; z-index: 1; }
.seg { fill: none; stroke: rgba(59,130,246,.6); stroke-width: 3; stroke-dasharray: 7 8; filter: drop-shadow(0 1px 0 rgba(0,0,0,.08)); }

.node { position: absolute; display: flex; flex-direction: column; align-items: center; z-index: 2; cursor: pointer; }
.btn-img { width: 122px; height: auto; display: block; filter: drop-shadow(0 6px 14px rgba(0,0,0,.18)); transition: transform .18s ease, filter .18s ease; }
.node.hover .btn-img { transform: translateY(-4px) scale(1.03); filter: drop-shadow(0 10px 22px rgba(0,0,0,.22)); }
.label { margin-top: 6px; color: #0f172a; font-weight: 800; font-size: 14px; letter-spacing: .3px; text-shadow: 0 1px 0 rgba(255,255,255,.6); }

.node.boss .btn-img { width: 230px; }
.node.boss.hover .btn-img { transform: translateY(-8px) scale(1.4); filter: drop-shadow(0 14px 28px rgba(220,38,38,.5)); }
.node.boss .label { font-size: 20px; margin-top: 8px; }
.node.boss .tag { font-size: 14px; padding: 4px 12px; bottom: -34px; background: #f59e0b; color: #fff;border-radius: 999px;padding: 2px 8px;margin-top: 5px;}

/* 弹窗 */
.modal { position: fixed; inset: 0; background: rgba(0,0,0,.45); display: grid; place-items: center; z-index: 50; }
.modal-card { width: min(380px, 86vw); background: #fff; border-radius: 14px; padding: 18px 18px 14px; box-shadow: 0 18px 44px rgba(0,0,0,.22); animation: pop .18s ease-out; }
.modal-title { font-weight: 900; font-size: 18px; color: #065f46; margin-bottom: 6px; }
.modal-body { color: #0f172a; line-height: 1.6; margin-bottom: 12px; }
.modal-ok { width: 100%; height: 36px; border: none; border-radius: 10px; background: linear-gradient(135deg,#10b981,#34d399); color: #fff; font-weight: 800; cursor: pointer; box-shadow: 0 10px 22px rgba(16,185,129,.28); }
@keyframes pop { from { transform: translateY(6px) scale(.98); opacity: 0; } to { transform: translateY(0) scale(1); opacity: 1; } }

/* 隐藏滚动条（仅在本页生效） */
:global(.h-scroll-container){ -ms-overflow-style: none; scrollbar-width: none; }
:global(.h-scroll-container::-webkit-scrollbar){ width: 0; height: 0; }
</style>


