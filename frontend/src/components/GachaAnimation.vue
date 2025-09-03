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
               :class="{ 
                 'fly-in': stage >= 2, 
                 'flip': stage >= 3,
                 [`rarity-${getGachaResults()[i-1]?.rarity?.toLowerCase()}`]: getGachaResults()[i-1]
               }"
               :style="{ '--delay': `${i * (props.count === 10 ? 0.02 : 0.04)}s` }">
            <div class="card-back"></div>
            <div class="card-front">
              <!-- 卡片正面显示结果 -->
                              <div class="card-content" v-if="getGachaResults()[i-1]">
                  <div class="card-image">
                    <img v-if="getGachaResults()[i-1].image_url" 
                         :src="resolveImageUrl(getGachaResults()[i-1].image_url)" 
                         :alt="getGachaResults()[i-1].name"
                         @error="handleImageError">
                    <div v-else class="image-placeholder">
                      {{ getGachaResults()[i-1].name.charAt(0) }}
                    </div>
                  </div>
                  <div class="glow-effect" v-if="getGachaResults()[i-1].glow"></div>
                </div>
                
                <!-- 卡牌信息显示在卡片下方 -->
                <div class="card-info-below" v-if="getGachaResults()[i-1]">
                  <div class="rarity" :class="`rarity-${getGachaResults()[i-1].rarity.toLowerCase()}`">
                    {{ getGachaResults()[i-1].rarity }}
                  </div>
                  <div class="name" :class="`rarity-${getGachaResults()[i-1].rarity.toLowerCase()}`">
                    {{ getGachaResults()[i-1].name }}
                  </div>
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
  count: { type: Number, default: 1 },
  results: { type: Array, default: () => [] } // 从父组件接收抽卡结果
})
const emit = defineEmits(['complete'])

const visible = ref(false)

// 监听父组件的显示状态
import { watch } from 'vue'
watch([() => props.count, () => props.results], ([newCount, newResults]) => {
  if (newCount > 0 && newResults && newResults.length > 0) {
    visible.value = true
    // 延迟启动动画，确保DOM已更新
    setTimeout(() => {
      startAnimation()
    }, 100)
  } else {
    visible.value = false
  }
}, { immediate: true })
const stage = ref(0)
let animationTimer = null

// 解析图片URL
function resolveImageUrl(url) {
  if (!url) return ''
  
  try {
    // 使用require动态导入图片
    const cleanPath = url.replace(/^assets\//, '')
    return require(`@/assets/${cleanPath}`)
  } catch (error) {
    console.warn('图片加载失败:', url, error)
    return ''
  }
}

// 处理图片加载失败
function handleImageError(event) {
  // 隐藏失败的图片，显示占位符
  event.target.style.display = 'none'
  const placeholder = event.target.nextElementSibling
  if (placeholder) {
    placeholder.style.display = 'flex'
  }
}

// 使用父组件传递的真实抽卡结果
function getGachaResults() {
  return props.results.map((card, index) => {
    // 确保card对象存在
    if (!card) {
      return null
    }
    
    return {
      ...card,
      id: card.id || card.card_id || card.name || `${Date.now()}-${index}`,
      glow: card.rarity === 'UR' || card.rarity === 'SR',
      color: getRarityColor(card.rarity)
    }
  }).filter(Boolean) // 过滤掉空值
}

// 根据稀有度获取颜色
function getRarityColor(rarity) {
  const colorMap = {
    'B': '#9BA0A3',   
    'A': '#7FEE77',    
    'R': '#40C3FC',    
    'SR': '#DA34EA',   
    'UR': '#E9E635'   
  }
  return colorMap[rarity] || '#b5c0d0'
}

function startAnimation() {
  let currentStage = 0
  
  const stages = [
    { duration: 500 },   // 标题出现
    { duration: props.count === 10 ? 800 : 600 },   // 卡片飞入
    { duration: 500 },   // 卡片翻转
    { duration: 500 }    // 光效爆发
  ]
  
  stages.forEach((stageInfo, index) => {
    setTimeout(() => {
      currentStage = index + 1
      stage.value = currentStage
      
      if (currentStage === 4) {
        // 动画完成，触发抽卡
        setTimeout(() => {
          emit('complete', getGachaResults())
        }, 500)
      }
    }, stages.slice(0, index).reduce((acc, s) => acc + s.duration, 0))
  })
}

onMounted(() => {
  document.body.style.overflow = 'hidden'
  // 不在这里启动动画，让watch来处理
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
          margin: 80px 0 150px 0; /* 增加上下间距，为文字显示留出更多空间 */
          display: flex;
          gap: 45px;
          flex-wrap: wrap;
          justify-content: center;
          max-width: 800px;
          /* 十抽时优化性能 */
          will-change: transform;
          transform: translateZ(0);
        }



.card {
  width: 120px;
  height: 190px;
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
          background: center/cover no-repeat;
          border: none;
          border-radius: 12px;
        }
        
        /* 稀有度对应的卡牌背面 */
        .card.rarity-b .card-back {
          background-image: url('@/assets/img/Decks/background.png');
        }
        .card.rarity-a .card-back {
          background-image: url('@/assets/img/Decks/background.png');
        }
        .card.rarity-r .card-back {
          background-image: url('@/assets/img/Decks/background.png');
        }
        .card.rarity-sr .card-back {
          background-image: url('@/assets/img/Decks/background.png');
        }
        .card.rarity-ur .card-back {
          background-image: url('@/assets/img/Decks/background.png');
        }

        .card-front {
          background: linear-gradient(145deg, #ffffff, #f8fafc);
          border: none;
          transform: rotateY(180deg);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0px;
        }
        
        /* 确保稀有度边框在翻转时也能显示 */
        .card.rarity-b .card-front,
        .card.rarity-a .card-front,
        .card.rarity-r .card-front,
        .card.rarity-sr .card-front,
        .card.rarity-ur .card-front {
          border: none;
        }

.card-content {
  text-align: center;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

        .card-image {
          width: 100%;
          height: 100%;
          border-radius: 8px;
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #f8fafc;
        }

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #e2e8f0, #cbd5e1);
  color: #64748b;
  font-size: 24px;
  font-weight: bold;
  border-radius: 6px;
}

        .card-info-below {
          position: absolute;
          bottom: -60px;
          left: 50%;
          transform: translateX(-50%);
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0px;
          background: transparent;
          color: #fafafa;
          padding: 15px 16px;
          border-radius: 10px;
          min-width: 100px;
          z-index: 10;
        }
        
        .card-info-below .rarity {
          font-size: 13px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        
        .card-info-below .name {
          font-size: 14px;
          font-weight: 500;
          text-align: center;
          line-height: 1.2;
          max-width: 120px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          color: #333;
        }
        
        /* 稀有度颜色 */
        .card-info-below .rarity.rarity-b { 
          color: #9BA0A3; 
        }
        .card-info-below .rarity.rarity-a { 
          color: #7FEE77; 
        }
        .card-info-below .rarity.rarity-r { 
          color: #40C3FC; 
        }
        .card-info-below .rarity.rarity-sr { 
          color: #DA34EA; 
        }
        .card-info-below .rarity.rarity-ur { 
          color: #E9E635; 
        }
        
        /* 稀有度名称颜色 */
        .card-info-below .name.rarity-b { 
          color: #9BA0A3; 
        }
        .card-info-below .name.rarity-a { 
          color: #7FEE77; 
        }
        .card-info-below .name.rarity-r { 
          color: #40C3FC; 
        }
        .card-info-below .name.rarity-sr { 
          color: #DA34EA; 
        }
        .card-info-below .name.rarity-ur { 
          color: #E9E635; 
        }
        

        


.rarity {
  font-weight: 800;
  font-size: 14px;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.rarity-b { color: #b5c0d0; }
.rarity-a { color: #6dd5ed; }
.rarity-r { color: #a770ef; }
.rarity-sr { color: #fdbb2d; }
.rarity-ur { color: #ff6b6b; }

.name {
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
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
  height: 500px;
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
  .cards-container { gap: 5px; }
  .card { width: 80px; height: 120px; }
}
</style>
