<template>
  <transition name="fade">
    <div v-if="visible" class="animation-overlay">
      <div class="backdrop"/>
      
      <div class="stage">
        <!-- 抽卡标题 -->
        <div class="title" :class="{ 'show': stage >= 1 }">
          {{ count === 10 ? '十连抽卡' : '单抽' }}
        </div>
        
        <!-- 卡片动画区域 -->
        <div class="cards-container">
          <div v-for="i in count" :key="i" 
               class="card" 
               :class="{ 'fly-in': stage >= 2, 'flip': stage >= 3 }"
               :style="{ '--delay': `${i * 0.1}s` }">
            <div class="card-back"></div>
            <div class="card-front"></div>
          </div>
        </div>
        
        <!-- 光效 -->
        <div class="effects">
          <div class="light-burst" :class="{ 'active': stage >= 4 }"></div>
          <div class="particles" :class="{ 'active': stage >= 4 }">
            <span v-for="i in 20" :key="i" :style="{ '--delay': `${i * 0.05}s` }"></span>
          </div>
        </div>
        
        <!-- 进度条 -->
        <div class="progress" :class="{ 'show': stage >= 1 }">
          <div class="bar" :style="{ width: `${progress}%` }"></div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  count: { type: Number, default: 1 }
})
const emit = defineEmits(['complete'])

const visible = ref(true)
const stage = ref(0)
const progress = ref(0)
let animationTimer = null

// 模拟抽卡结果
async function simulateGacha() {
  const pool = [
    { rarity: 'N', name: '知识碎片', color: '#b5c0d0' },
    { rarity: 'R', name: '课堂灵感', color: '#6dd5ed' },
    { rarity: 'SR', name: '学术火花', color: '#a770ef' },
    { rarity: 'SSR', name: '灵光一现', color: '#fdbb2d' }
  ]
  const weights = [70, 22, 7, 1]
  const results = []
  
  for (let i = 0; i < props.count; i++) {
    const roll = Math.random() * 100
    let acc = 0
    let idx = 0
    for (let j = 0; j < weights.length; j++) {
      acc += weights[j]
      if (roll <= acc) { idx = j; break }
    }
    const base = pool[idx]
    results.push({ ...base, id: `${Date.now()}-${i}`, glow: base.rarity === 'SSR' || base.rarity === 'SR' })
  }
  
  return new Promise(resolve => setTimeout(() => resolve(results), 800))
}

function startAnimation() {
  let currentStage = 0
  const stages = [
    { duration: 800, progress: 20 },   // 标题出现
    { duration: 1200, progress: 40 },  // 卡片飞入
    { duration: 1000, progress: 60 },  // 卡片翻转
    { duration: 1500, progress: 80 },  // 光效爆发
    { duration: 1000, progress: 100 }  // 完成
  ]
  
  stages.forEach((stageInfo, index) => {
    setTimeout(() => {
      currentStage = index + 1
      stage.value = currentStage
      progress.value = stageInfo.progress
      
      if (currentStage === 5) {
        // 动画完成，触发抽卡
        setTimeout(async () => {
          try {
            const results = await simulateGacha()
            emit('complete', results)
          } catch (error) {
            console.error('抽卡失败:', error)
            emit('complete', [])
          }
        }, 500)
      }
    }, stages.slice(0, index).reduce((acc, s) => acc + s.duration, 0))
  })
}

onMounted(() => {
  document.body.style.overflow = 'hidden'
  startAnimation()
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  if (animationTimer) clearTimeout(animationTimer)
})
</script>

<style scoped>
.animation-overlay {
  position: fixed;
  inset: 0;
  z-index: 3000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.backdrop {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
}

.stage {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 48px;
  font-weight: 800;
  color: white;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.title.show {
  opacity: 1;
  transform: translateY(0);
}

.cards-container {
  position: relative;
  margin: 60px 0;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 600px;
}

.card {
  width: 80px;
  height: 120px;
  position: relative;
  transform-style: preserve-3d;
  transform: translateY(100vh) rotateY(0deg);
  transition: all 0.8s cubic-bezier(0.22, 0.61, 0.36, 1);
  transition-delay: var(--delay, 0s);
}

.card.fly-in {
  transform: translateY(0) rotateY(0deg);
}

.card.flip {
  transform: translateY(0) rotateY(180deg);
}

.card-back, .card-front {
  position: absolute;
  inset: 0;
  border-radius: 12px;
  backface-visibility: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.card-back {
  /* 使用塔罗牌背面图片 */
  background: center/cover no-repeat url('@/assets/img/Decks/塔罗牌背面.jpg');
  border: 2px solid rgba(255, 255, 255, 0.35);
}

.card-front {
  background: linear-gradient(145deg, #ffffff, #f8fafc);
  border: 2px solid rgba(255, 255, 255, 0.3);
  transform: rotateY(180deg);
}

.effects {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.light-burst {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.8), transparent);
  transform: translate(-50%, -50%);
  transition: all 1.5s ease-out;
}

.light-burst.active {
  width: 400px;
  height: 400px;
  opacity: 0;
}

.particles {
  position: absolute;
  inset: 0;
}

.particles span {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: white;
  opacity: 0;
  animation: particleFloat 2s ease-out infinite;
  animation-delay: var(--delay, 0s);
}

.particles.active span {
  opacity: 1;
}

@keyframes particleFloat {
  0% {
    transform: translate(0, 0) scale(0);
    opacity: 1;
  }
  100% {
    transform: translate(var(--x, 100px), var(--y, -100px)) scale(1);
    opacity: 0;
  }
}

.progress {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  width: 300px;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
  opacity: 0;
  transition: opacity 0.5s ease;
}

.progress.show {
  opacity: 1;
}

.progress .bar {
  height: 100%;
  background: linear-gradient(90deg, #74ebd5, #9face6);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 为粒子设置随机位置 */
.particles span:nth-child(1) { --x: 120px; --y: -80px; left: 20%; top: 60%; }
.particles span:nth-child(2) { --x: -100px; --y: -120px; left: 80%; top: 40%; }
.particles span:nth-child(3) { --x: 80px; --y: 100px; left: 30%; top: 80%; }
.particles span:nth-child(4) { --x: -120px; --y: 80px; left: 70%; top: 20%; }
.particles span:nth-child(5) { --x: 60px; --y: -100px; left: 40%; top: 50%; }
.particles span:nth-child(6) { --x: -80px; --y: -60px; left: 60%; top: 30%; }
.particles span:nth-child(7) { --x: 100px; --y: 120px; left: 25%; top: 70%; }
.particles span:nth-child(8) { --x: -60px; --y: 100px; left: 75%; top: 10%; }
.particles span:nth-child(9) { --x: 90px; --y: -80px; left: 35%; top: 45%; }
.particles span:nth-child(10) { --x: -90px; --y: -100px; left: 65%; top: 35%; }
.particles span:nth-child(11) { --x: 70px; --y: 90px; left: 45%; top: 75%; }
.particles span:nth-child(12) { --x: -70px; --y: 80px; left: 55%; top: 15%; }
.particles span:nth-child(13) { --x: 110px; --y: -70px; left: 15%; top: 55%; }
.particles span:nth-child(14) { --x: -110px; --y: -90px; left: 85%; top: 25%; }
.particles span:nth-child(15) { --x: 50px; --y: 110px; left: 50%; top: 85%; }
.particles span:nth-child(16) { --x: -50px; --y: 70px; left: 10%; top: 25%; }
.particles span:nth-child(17) { --x: 80px; --y: -60px; left: 90%; top: 65%; }
.particles span:nth-child(18) { --x: -80px; --y: 90px; left: 20%; top: 85%; }
.particles span:nth-child(19) { --x: 60px; --y: -110px; left: 80%; top: 15%; }
.particles span:nth-child(20) { --x: -60px; --y: 60px; left: 30%; top: 95%; }

@media (max-width: 768px) {
  .title { font-size: 32px; }
  .cards-container { gap: 12px; }
  .card { width: 60px; height: 90px; }
  .progress { width: 250px; bottom: 60px; }
}
</style>
