<template>
  <div class="page">
    <div class="points">
      <span class="label">积分</span>
      <span class="value">{{ points }}</span>
      <el-button class="gain gbtn-mini" size="small" type="success" plain @click="addPoints(100)">+100</el-button>
    </div>

    <InteractiveCard
      :image-src="cardImage"
      alt-text="卡片背面"
      :gif-src="sparklesGif"
      gif-alt="特效-星星闪烁"
      size-mode="auto"
      width="clamp(220px, 42vw, 300px)"
      aspect-ratio="3/5"
      border-radius="16px"
      :image-scale="0.165"
    />

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
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { CreditCard } from '@element-plus/icons-vue'
import InteractiveCard from '@/components/InteractiveCard.vue'
import GachaAnimation from '@/components/GachaAnimation.vue'
import GachaOverlay from '@/components/GachaOverlay.vue'
import cardImage from '@/assets/img/Decks/background.png'
import sparklesGif from '@/assets/gif/sparkles.gif'

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


</script>

<style scoped>
.page{ padding:16px; min-height:100%; position:relative;background: rgba(176, 176, 176, 0.858); }
.points{ position:absolute; right:16px; top:12px; display:flex; align-items:center; gap:8px; background:rgba(255,255,255,0.75); backdrop-filter: blur(6px); border-radius:999px; padding:6px 12px; box-shadow:0 6px 20px rgba(0,0,0,.08); z-index:10; }
.points .label{ font-size:12px; color:#666; }
.points .value{ font-weight:700; color:#333; }
.points :deep(.el-button.gbtn-mini){ padding:4px 8px; }



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


