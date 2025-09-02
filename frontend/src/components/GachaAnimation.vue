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
               :style="{ '--delay': `${i * (props.count === 10 ? 0.02 : 0.04)}s` }">
            <div class="card-back"></div>
            <div class="card-front">
              <!-- 卡片正面显示结果 -->
              <div class="card-content" v-if="results[i-1]">
                <div class="rarity" :class="`rarity-${results[i-1].rarity.toLowerCase()}`">
                  {{ results[i-1].rarity }}
                </div>
                <div class="name">{{ results[i-1].name }}</div>
                <div class="glow-effect" v-if="results[i-1].glow"></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 光效 -->
        <div class="effects">
          <div class="light-burst" :class="{ 'active': stage >= 4 }"></div>
          <div class="particles" :class="{ 'active': stage >= 4 }">
            <span v-for="i in 12" :key="i" :style="{ '--delay': `${i * 0.03}s` }"></span>
          </div>
        </div>
        

      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

/* global defineProps, defineEmits */
const props = defineProps({
  count: { type: Number, default: 1 }
})
const emit = defineEmits(['complete'])

const visible = ref(true)
const stage = ref(0)
const results = ref([])
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
  
  return new Promise(resolve => setTimeout(() => resolve(results), 100))
}

function startAnimation() {
  let currentStage = 0
  
  const stages = [
    { duration: 500 },   // 标题出现
    { duration: props.count === 10 ? 800 : 600 },   // 卡片飞入
    { duration: 500 },   // 卡片翻转
    { duration: 500 }    // 光效爆发
  ]
  
  // 预先获取抽卡结果，避免动画过程中的阻塞
  simulateGacha().then(gachaResults => {
    results.value = gachaResults
  }).catch(error => {
    console.error('抽卡失败:', error)
    results.value = []
  })
  
  stages.forEach((stageInfo, index) => {
    setTimeout(() => {
      currentStage = index + 1
      stage.value = currentStage
      
      if (currentStage === 4) {
        // 动画完成，触发抽卡
        setTimeout(() => {
          emit('complete', results.value)
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
  transition: all 0.45s cubic-bezier(0.22, 0.61, 0.36, 1);
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
  max-width: 800px;
  /* 十抽时优化性能 */
  will-change: transform;
  transform: translateZ(0);
}



.card {
  width: 120px;
  height: 160px;
  position: relative;
  transform-style: preserve-3d;
  transform: translateY(100vh) rotateY(0deg);
  transition: all 0.45s cubic-bezier(0.22, 0.61, 0.36, 1);
  transition-delay: var(--delay, 0s);
  /* 十抽时优化性能 */
  will-change: transform;
  backface-visibility: hidden;
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
  background: center/cover no-repeat url('@/assets/img/Decks/background.png');
  border: 2px solid rgba(255, 255, 255, 0.35);
}

.card-front {
  background: linear-gradient(145deg, #ffffff, #f8fafc);
  border: 2px solid rgba(255, 255, 255, 0.3);
  transform: rotateY(180deg);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
}

.card-content {
  text-align: center;
  width: 100%;
}

.rarity {
  font-weight: 800;
  font-size: 14px;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.rarity-n { color: #b5c0d0; }
.rarity-r { color: #6dd5ed; }
.rarity-sr { color: #a770ef; }
.rarity-ssr { color: #fdbb2d; }

.name {
  font-size: 12px;
  font-weight: 600;
  color: #2b2f36;
  line-height: 1.2;
}

.glow-effect {
  position: absolute;
  inset: -4px;
  border-radius: 12px;
  background: radial-gradient(80% 80% at 50% 50%, rgba(255,255,255,.6), rgba(255,255,255,0));
  filter: blur(6px);
  opacity: 0.8;
  pointer-events: none;
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
  transition: all 0.45s ease-out;
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
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: white;
  opacity: 0;
  animation: particleFloat 1.5s ease-out infinite;
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
    transform: translate(var(--x, 80px), var(--y, -80px)) scale(1);
    opacity: 0;
  }
}



.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 为粒子设置随机位置 */
.particles span:nth-child(1) { --x: 100px; --y: -60px; left: 20%; top: 60%; }
.particles span:nth-child(2) { --x: -80px; --y: -100px; left: 80%; top: 40%; }
.particles span:nth-child(3) { --x: 60px; --y: 80px; left: 30%; top: 80%; }
.particles span:nth-child(4) { --x: -100px; --y: 60px; left: 70%; top: 20%; }
.particles span:nth-child(5) { --x: 50px; --y: -80px; left: 40%; top: 50%; }
.particles span:nth-child(6) { --x: -60px; --y: -50px; left: 60%; top: 30%; }
.particles span:nth-child(7) { --x: 80px; --y: 100px; left: 25%; top: 70%; }
.particles span:nth-child(8) { --x: -50px; --y: 80px; left: 75%; top: 10%; }
.particles span:nth-child(9) { --x: 70px; --y: -60px; left: 35%; top: 45%; }
.particles span:nth-child(10) { --x: -70px; --y: -80px; left: 65%; top: 35%; }
.particles span:nth-child(11) { --x: 60px; --y: 70px; left: 45%; top: 75%; }
.particles span:nth-child(12) { --x: -60px; --y: 60px; left: 55%; top: 15%; }

@media (max-width: 768px) {
  .title { font-size: 32px; }
  .cards-container { gap: 12px; }
  .card { width: 80px; height: 120px; }
}
</style>
