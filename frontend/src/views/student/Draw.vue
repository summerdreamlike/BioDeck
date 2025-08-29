<template>
  <div class="page">
    <div class="points">
      <span class="label">积分</span>
      <span class="value">{{ points }}</span>
      <el-button class="gain gbtn-mini" size="small" type="success" plain @click="addPoints(100)">+100</el-button>
    </div>

    <div class="gacha-stage" ref="stageRef" @mouseenter="onEnter" @mousemove="onMove" @mouseleave="onLeave">
      <div class="card-frame" ref="frameRef" :style="cardTransformStyle">
        <div class="card-art" ref="artRef">
          <img class="gif-stars" :src="starsGif" alt=""/>
        </div>
      </div>
    </div>

    <div class="actions">
      <el-button class="gbtn one" type="primary" size="large" :disabled="points < 10 || isDrawing" @click="startDraw(1)">
        <el-icon style="margin-right:6px"><CreditCard/></el-icon>
        一抽（10）
      </el-button>
      <el-button class="gbtn ten" type="warning" size="large" :disabled="points < 100 || isDrawing" @click="startDraw(10)">
        <el-icon style="margin-right:6px"><CreditCard/></el-icon>
        十抽（100）
      </el-button>
    </div>

    <GachaAnimation v-if="showAnimation" :count="lastCount" @complete="onAnimationComplete"/>
    <GachaOverlay v-if="showOverlay" :results="drawResults" :count="lastCount" @close="onOverlayClose"/>
  </div>
  
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { CreditCard } from '@element-plus/icons-vue'
import GachaAnimation from '@/components/GachaAnimation.vue'
import GachaOverlay from '@/components/GachaOverlay.vue'
import starsGif from '@/assets/gif/sparkles.gif'

const STORAGE_KEY = 'gacha_points'
const DEFAULT_POINTS = 200

const points = ref(loadPoints())
const isDrawing = ref(false)
const showAnimation = ref(false)
const showOverlay = ref(false)
const drawResults = ref([])
const lastCount = ref(0)

function loadPoints(){
  const raw = localStorage.getItem(STORAGE_KEY)
  const n = Number(raw)
  return Number.isFinite(n) && n >= 0 ? n : DEFAULT_POINTS
}

function savePoints(value){
  points.value = value
  localStorage.setItem(STORAGE_KEY, String(value))
}

function addPoints(amount){
  const v = Number(amount) || 0
  if (v <= 0) return
  savePoints(points.value + v)
  ElMessage.success(`已获得 ${v} 积分`)
}

async function startDraw(count){
  if (isDrawing.value) return
  const cost = count === 10 ? 100 : 10
  if (points.value < cost){
    ElMessage.warning('积分不足')
    return
  }
  isDrawing.value = true
  savePoints(points.value - cost)
  lastCount.value = count
  showAnimation.value = true
}

function onAnimationComplete(results){
  showAnimation.value = false
  drawResults.value = results
  showOverlay.value = true
  isDrawing.value = false
}

function onOverlayClose(){
  showOverlay.value = false
}

// 3D 跟随（扩大交互范围） + 高光跟随（--per）
const stageRef = ref(null)
const frameRef = ref(null)
const artRef = ref(null)
const tiltX = ref(0)
const tiltY = ref(0)
const scale = ref(1)
const maxTilt = 18
const rangeScale = 1.6
const rafId = ref(0)

function onEnter(){
  scale.value = 1.03
  if (artRef.value) artRef.value.style.setProperty('--per', '0%')
}
function onMove(e){
  const frame = frameRef.value
  const art = artRef.value
  if (!frame || !art) return

  // 倾斜用 frame 尺寸
  const fr = frame.getBoundingClientRect()
  const cx = fr.left + fr.width / 2
  const cy = fr.top + fr.height / 2
  const rx = (fr.width / 2) * rangeScale
  const ry = (fr.height / 2) * rangeScale
  const nx = Math.max(-1, Math.min(1, (e.clientX - cx) / rx))
  const ny = Math.max(-1, Math.min(1, (e.clientY - cy) / ry))
  const targetTiltX = -ny * maxTilt
  const targetTiltY =  nx * maxTilt

  // 高光用 art 尺寸（更贴合视觉）
  const ar = art.getBoundingClientRect()
  const per = Math.max(0, Math.min(100, ((e.clientX - ar.left) / ar.width) * 100))

  // rAF 插值更新，提升稳定度与精度
  cancelAnimationFrame(rafId.value)
  rafId.value = requestAnimationFrame(() => {
    tiltX.value += (targetTiltX - tiltX.value) * 0.25
    tiltY.value += (targetTiltY - tiltY.value) * 0.25
    art.style.setProperty('--per', `${per}%`)
  })
}
function onLeave(){
  cancelAnimationFrame(rafId.value)
  tiltX.value = 0; tiltY.value = 0; scale.value = 1
  if (artRef.value) artRef.value.style.setProperty('--per', '0%')
}

const cardTransformStyle = computed(() => ({
  transform: `rotateX(${tiltX.value}deg) rotateY(${tiltY.value}deg) scale(${scale.value})`
}))
</script>

<style scoped>
.page{ padding:16px; min-height:100%; position:relative; }
.points{ position:absolute; right:16px; top:12px; display:flex; align-items:center; gap:8px; background:rgba(255,255,255,0.75); backdrop-filter: blur(6px); border-radius:999px; padding:6px 12px; box-shadow:0 6px 20px rgba(0,0,0,.08); }
.points .label{ font-size:12px; color:#666; }
.points .value{ font-weight:700; color:#333; }
.points :deep(.el-button.gbtn-mini){ padding:4px 8px; }

.gacha-stage{ display:flex; justify-content:center; align-items:center; padding:24px 0 12px; perspective: 1100px; }
.card-frame{ width: clamp(220px, 42vw, 300px); aspect-ratio: 3/6; border-radius:16px; background:linear-gradient(145deg,#eef2f7,#ffffff); position:relative; box-shadow: 0 20px 40px rgba(0,0,0,.08), inset 0 0 0 1px rgba(0,0,0,.04); overflow:hidden; transition: transform .22s cubic-bezier(.22,.61,.36,1), box-shadow .22s; transform-style: preserve-3d; }
.card-art{ position:absolute; inset:0; border-radius:inherit; background-image: url('@/assets/img/Decks/塔罗牌背面.jpg'); background-position:center; background-repeat:no-repeat; background-size: 100% auto; }

/* 高光覆层使用 --per 控制位置 */
.card-art::before{
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: inherit;
  background: linear-gradient(115deg,
    transparent calc(var(--per, 50%) - 22%),
    rgba(255,255,255,.55) var(--per, 50%),
    transparent calc(var(--per, 50%) + 22%));
  mix-blend-mode: color-dodge;
}

/* GIF 星星闪烁叠加层（模块导入） */
.gif-stars{ position:absolute; inset:0; width:100%; height:100%; object-fit: cover; mix-blend-mode: screen; pointer-events:none; opacity:.9; border-radius:inherit; z-index:1; }

.actions{ display:flex; justify-content:center; gap:16px; margin-top:60px; }

/* gradient buttons */
:deep(.el-button.gbtn){
  --c1: #6dd5ed; --c2:#2193b0;
  background: linear-gradient(135deg, var(--c1), var(--c2));
  border: none; border-radius: 999px; color:#fff; padding: 14px 22px;
  box-shadow: 0 10px 24px rgba(33,147,176,.28);
  transition: transform .2s ease, box-shadow .2s ease, filter .2s ease;
}
:deep(.el-button.gbtn.one){ --c1:#74ebd5; --c2:#ACB6E5; box-shadow:0 10px 24px rgba(116,235,213,.25); }
:deep(.el-button.gbtn.ten){ --c1:#f6d365; --c2:#fda085; box-shadow:0 10px 24px rgba(253,160,133,.28); }
:deep(.el-button.gbtn.is-disabled){ filter: grayscale(.35) brightness(.9); box-shadow:none; }
:deep(.el-button.gbtn:not(.is-disabled):hover){ transform: translateY(-1px); box-shadow:0 14px 30px rgba(0,0,0,.16); }
:deep(.el-button.gbtn:not(.is-disabled):active){ transform: translateY(0); filter: brightness(.96); }

:deep(.el-button.gbtn-mini){
  --c1:#34d399; --c2:#10b981;
  background: linear-gradient(135deg, var(--c1), var(--c2));
  border:none; border-radius: 999px; color:#fff; padding:6px 10px; height:auto;
  box-shadow: 0 6px 16px rgba(16,185,129,.28);
}

@media (max-width:768px){
  .points{ right:12px; top:10px; }
}
</style>


