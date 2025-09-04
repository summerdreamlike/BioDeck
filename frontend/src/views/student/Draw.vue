<template>
  <div class="page">
    <div class="points">
      <span class="label">积分</span>
      <span class="value">{{ points }}</span>
      <el-button class="gain gbtn-mini" size="small" type="success" plain @click="addPoints(1000)">+1000</el-button>
      
      <!-- 积分变化动画 -->
      <transition name="points-change">
        <div v-if="pointsChange.show" class="points-change-animation" :class="pointsChange.type">
          {{ pointsChange.type === 'add' ? '+' : '-' }}{{ pointsChange.value }}
        </div>
      </transition>
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
      :laser-src="laserSrc"
      :enable-laser="true"
      :laser-alt="'镭射效果'"
    />

    <div class="actions">
      <el-button class="gbtn one" type="primary" size="large" :disabled="points < 100 || isDrawing" @click="startDraw(1)">
        <el-icon style="margin-right:6px"><CreditCard/></el-icon>
        一抽（100）
      </el-button>
      <el-button class="gbtn ten" type="warning" size="large" :disabled="points < 900 || isDrawing" @click="startDraw(10)">
        <el-icon style="margin-right:6px"><CreditCard/></el-icon>
        十抽（900）
      </el-button>
    </div>

    <GachaAnimation v-if="showAnimation" :count="lastCount" :results="drawResults" @complete="onAnimationComplete"/>
    <GachaOverlay v-if="showOverlay" :results="drawResults" :count="lastCount" @close="onOverlayClose"/>
  </div>
  
</template>

<script setup>
import { ref, onMounted, nextTick, onBeforeUnmount } from 'vue'
import { ElMessage } from 'element-plus'
import { CreditCard } from '@element-plus/icons-vue'
import InteractiveCard from '@/components/InteractiveCard.vue'
import GachaAnimation from '@/components/GachaAnimation.vue'
import GachaOverlay from '@/components/GachaOverlay.vue'
import cardImage from '@/assets/img/Decks/background.png'
import sparklesGif from '@/assets/gif/sparkles.gif'
import laserSrc from '@/assets/img/镭射.png'
import { cardApi } from '@/api'

const points = ref(0)
const isDrawing = ref(false)
const showAnimation = ref(false)
const showOverlay = ref(false)
const drawResults = ref([])
const lastCount = ref(0)
const userCards = ref([]) // 用户拥有的卡牌

// 添加积分变化动画
const pointsAnimation = ref(false)
const pointsChange = ref({ show: false, value: 0, type: 'add' })

// 显示积分变化动画
function showPointsChange(amount, type = 'add') {
  pointsChange.value = {
    show: true,
    value: amount,
    type: type
  }
  
  // 3秒后隐藏动画
  setTimeout(() => {
    pointsChange.value.show = false
  }, 3000)
}

// 监听积分变化事件
function handlePointsUpdated(event) {
  const { points, change, totalPoints, type } = event.detail
  console.log('收到积分更新事件:', { points, change, totalPoints, type })
  
  // 更新积分显示
  if (totalPoints !== undefined) {
    // 优先使用后端返回的总积分
    points.value = totalPoints
    console.log(`使用后端总积分更新显示: ${totalPoints}`)
  } else {
    // 否则使用计算后的积分
    points.value = points
    console.log(`使用计算积分更新显示: ${points}`)
  }
  
  // 如果是签到获得的积分，显示动画
  if (type === 'daily_checkin') {
    showPointsChange(change, 'add')
    ElMessage.success(`签到积分已同步！当前积分: ${points.value}`)
  }
}

async function loadUserPoints(){
  try {
    // 从后端获取用户积分
    const response = await cardApi.getUserPoints()
    
    if ((response && response.data && typeof response.data.points === 'number') || 
        (response && response.code === 0 && response.data && typeof response.data.points === 'number')) {
      points.value = response.data.points
      
      // 同步到本地存储
      localStorage.setItem('userPoints', points.value.toString())
    } else {
      points.value = 100 // 默认积分
      localStorage.setItem('userPoints', '100')
    }
  } catch (error) {
    console.error('获取用户积分失败:', error)
    points.value = 100 // 默认积分
    localStorage.setItem('userPoints', '100')
  }
}

async function addPoints(amount){
  const v = Number(amount) || 0
  if (v <= 0) return
  
  try {
    // 调用后端API增加积分
    const response = await cardApi.addPoints(v)
    
    if ((response && response.data && typeof response.data.points === 'number') || 
        (response && response.code === 0 && response.data && typeof response.data.points === 'number')) {
      // 更新前端积分显示
      points.value = response.data.points
      
      // 显示积分变化动画
      showPointsChange(v, 'add')
      
      ElMessage.success(`获得 ${v} 积分！`)
    } else {
      ElMessage.error('积分增加失败')
    }
  } catch (error) {
    console.error('积分增加失败:', error)
    ElMessage.error('积分增加失败，请重试')
  }
}

async function startDraw(count){
  if (isDrawing.value) return
  const cost = count === 10 ? 900 : 100
  if (points.value < cost){
    ElMessage.warning('积分不足')
    return
  }
  
  try {
    isDrawing.value = true
    lastCount.value = count
    
    // 调用后端抽卡API
    const apiFunction = count === 10 ? cardApi.tenDraw : cardApi.singleDraw
    const response = await apiFunction()
    
          if (response.success || response.code === 0) {
        // 计算积分变化
        const cost = count === 10 ? 900 : 100
        const oldPoints = points.value
        const newPoints = response.data.remaining_points
        
        // 更新积分
        points.value = newPoints
        
        // 触发积分减少动画
        pointsChange.value = { show: true, value: cost, type: 'subtract' }
        setTimeout(() => {
          pointsChange.value.show = false
        }, 1500)
        
        // 保存抽卡结果并添加到用户卡组
        if (count === 10) {
          // 十连抽：draws是数组，每个元素包含card属性和其他信息
          drawResults.value = response.data.draws.map(item => item.card)
          // 将新卡牌添加到用户卡组
          userCards.value.push(...drawResults.value)
        } else {
          // 单抽：response.data直接是卡牌信息
          drawResults.value = [response.data.card || response.data]
          // 将新卡牌添加到用户卡组
          userCards.value.push(...drawResults.value)
        }
      
      // 显示抽卡动画
      showAnimation.value = true
      
      // 强制触发响应式更新
      await nextTick()
    } else {
      ElMessage.error(response.message || '抽卡失败')
    }
  } catch (error) {
    console.error('抽卡失败:', error)
    ElMessage.error('抽卡失败，请稍后重试')
  } finally {
    isDrawing.value = false
  }
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

// 组件挂载时加载用户积分和卡组
onMounted(() => {
  loadUserPoints()
  
  // 注册积分变化事件监听器
  window.addEventListener('points-updated', handlePointsUpdated)
})

onBeforeUnmount(() => {
  // 清理积分变化事件监听器
  window.removeEventListener('points-updated', handlePointsUpdated)
})

// 加载用户卡组
async function loadUserCards() {
  try {
    const response = await cardApi.getUserCollection()
    if (response.success && response.data) {
      userCards.value = response.data
    }
  } catch (error) {
    console.error('获取用户卡组失败:', error)
  }
}


</script>

<style scoped>
.page{ padding:16px; min-height:100%; position:relative;background: rgba(176, 176, 176, 0.858); }
.points{ position:absolute; right:16px; top:12px; display:flex; align-items:center; gap:8px; background:rgba(255,255,255,0.75); backdrop-filter: blur(6px); border-radius:999px; padding:6px 12px; box-shadow:0 6px 20px rgba(0,0,0,.08); z-index:10; }
.points .label{ font-size:12px; color:#666; }
.points .value{ font-weight:700; color:#333; }
.points :deep(.el-button.gbtn-mini){ padding:4px 8px; }

/* 积分变化动画 */

.points-change-animation {
  position: absolute;
  top: -20px;
  right: 0;
  font-size: 14px;
  font-weight: 600;
  color: #10b981;
  pointer-events: none;
  z-index: 20;
}

.points-change-animation.add {
  color: #10b981;
}

.points-change-animation.subtract {
  color: #ef4444;
}

.points-change-enter-active {
  animation: pointsChangeIn 1.5s ease-out;
}

.points-change-leave-active {
  animation: pointsChangeOut 0.3s ease-in;
}

@keyframes pointsChangeIn {
  0% {
    opacity: 0;
    transform: translateY(0) scale(0.8);
  }
  20% {
    opacity: 1;
    transform: translateY(-10px) scale(1.2);
  }
  80% {
    opacity: 1;
    transform: translateY(-20px) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateY(-30px) scale(0.8);
  }
}

@keyframes pointsChangeOut {
  0% {
    opacity: 1;
    transform: translateY(-30px) scale(0.8);
  }
  100% {
    opacity: 0;
    transform: translateY(-40px) scale(0.6);
  }
}



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


