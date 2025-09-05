<template>
  <transition name="fade-scale">
    <div v-if="visible" class="overlay">
      <div class="backdrop"/>

      <div class="panel" :class="{ 'show': stage >= 1 }">
        <div class="top">
          <div class="title">
            抽卡结果 <span class="sub">×{{ count }}</span>
          </div>
          <button class="close" @click="close">×</button>
        </div>

        <div class="grid" :class="{ 'grid-10': count === 10 }">
          <div v-for="(item, idx) in results" :key="item.id" class="cell" :style="badgeStyle(item, idx)" :class="{ 
            'glow': item.glow, 
            'enter': enteredIndex >= idx, 
            'r-sr': item.rarity==='SR', 
            'r-ur': item.rarity==='UR',
            [`rarity-${item.rarity?.toLowerCase()}`]: item.rarity
          }">
            <div class="card">
              <div class="back"></div>
              <div class="front">
                <div class="card-image">
                  <img v-if="item.image_url" 
                       :src="resolveImageUrl(item.image_url)" 
                       :alt="item.name"
                       @error="handleImageError">
                  <div v-else class="image-placeholder">
                    {{ item.name.charAt(0) }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 卡牌信息显示在卡片下方 -->
            <div class="card-info-below">
              <div class="rarity" :class="`rarity-${item.rarity.toLowerCase()}`">{{ item.rarity }}</div>
              <div class="name" :class="`rarity-${item.rarity.toLowerCase()}`">{{ item.name }}</div>
            </div>
            
            <div v-if="item.rarity==='UR'" class="beam"></div>
          </div>
        </div>

        <div class="actions">
          <el-button type="primary" @click="close">收起</el-button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  results: { type: Array, default: () => [] },
  count: { type: Number, default: 1 }
})
const emit = defineEmits(['close'])

const visible = ref(true)
const stage = ref(0)
const enteredIndex = ref(-1)
let timer = null
let flipTimer = null

// 解析图片URL
function resolveImageUrl(url) {
  if (!url) return ''
  
  try {
    // 检查是否为图片文件
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
    const isImage = imageExtensions.some(ext => url.toLowerCase().includes(ext))
    
    if (!isImage) {
      console.warn('非图片文件:', url)
      return ''
    }
    
    // 使用require动态导入图片
    // 移除开头的assets/，因为require会从src/assets开始查找
    const cleanPath = url.replace(/^\/assets\//, '')
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

function badgeStyle(item, idx){
  const delay = `${Math.min(60 + idx * 40, 340)}ms`
  return { background: `linear-gradient(145deg, ${item.color}33, ${item.color}aa)`, '--delay': delay }
}

function close(){
  visible.value = false
  clear()
  setTimeout(() => emit('close'), 200)
}

function runEnter(){
  clear()
  stage.value = 1
  enteredIndex.value = -1
  let i = 0
  timer = setInterval(() => {
    enteredIndex.value = i
    i++
    if (i >= props.results.length){ clear() }
  }, Math.max(60, 200 - props.results.length * 15))
  // 翻面节奏
  let k = 0
  flipTimer = setInterval(() => {
    const nodes = document.querySelectorAll('.cell.enter .card')
    if (k < nodes.length){ nodes[k].classList.add('flip') }
    k++
    if (k >= props.results.length){ clearFlip() }
  }, 80)
}

function clear(){
  if (timer) { clearInterval(timer); timer = null }
}
function clearFlip(){ if (flipTimer){ clearInterval(flipTimer); flipTimer = null } }

watch(() => props.results, () => runEnter(), { immediate: true })

onMounted(() => {
  document.body.style.overflow = 'hidden'
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  clear(); clearFlip()
})
</script>

<style scoped>
.overlay{ position:fixed; inset:0; z-index: 3000; display:flex; align-items:center; justify-content:center; }
.backdrop{ position:absolute; inset:0; background: rgba(15,16,20,.58); backdrop-filter: blur(6px); }
.panel{ position:relative; width:min(980px, 92vw); max-height: 86vh; background: #fff; border-radius:16px; padding:16px; box-shadow: 0 24px 80px rgba(0,0,0,.25); transform: translateY(12px) scale(.98); opacity:0; transition: transform .28s cubic-bezier(.22,.61,.36,1), opacity .28s; display:flex; flex-direction:column; }
.panel.show{ transform: translateY(0) scale(1); opacity:1; }
.top{ display:flex; align-items:center; justify-content:space-between; }
.title{ font-weight:800; font-size:20px; }
.sub{ font-size:14px; color:#667085; margin-left:6px; }
.close{ border:none; width:32px; height:32px; border-radius:8px; cursor:pointer; background:#f2f4f7; }
.close:hover{ background:#eaecf0; }

.grid{ display:grid; grid-template-columns: repeat(5, 1fr); gap:60px 30px; padding:16px 4px 70px 4px; overflow:auto; }
.grid.grid-10{ grid-template-columns: repeat(5, 1fr); }
.cell{ position:relative; border-radius:12px; padding:6px; background:#eef2f7; box-shadow: none; transform: translateY(8px); opacity:0; transition: transform .25s, opacity .25s; }
.cell.enter{ transform: translateY(0); opacity:1; transition-delay: var(--delay, 0ms); }
.cell.glow::after{ content:''; position:absolute; inset:-2px; border-radius:12px; pointer-events:none; background: radial-gradient(80% 80% at 50% 50%, rgba(255,255,255,.6), rgba(255,255,255,0)); filter: blur(8px); opacity:.9; }

.card{ position:relative; height:260px; border-radius:1px; transform-style: preserve-3d; transition: transform .4s cubic-bezier(.22,.61,.36,1); box-shadow: 0 4px 12px rgba(0,0,0,.08); }
.card.flip{ transform: rotateY(180deg); }
.card .back, .card .front{ position:absolute; inset:0; backface-visibility: hidden; border-radius:10px; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:4px; }
.card .back{ 
  background: center/cover no-repeat;
}

/* 稀有度对应的卡牌背面 */
.cell.rarity-b .card .back {
  background-image: url('@/assets/img/Decks/backside/B卡.png');
  border-radius: 10px;
}
.cell.rarity-a .card .back {
  background-image: url('@/assets/img/Decks/backside/A卡.png');
  border-radius: 10px;
}
.cell.rarity-r .card .back {
  background-image: url('@/assets/img/Decks/backside/R卡.png');
  border-radius: 10px;
}
.cell.rarity-sr .card .back {
  background-image: url('@/assets/img/Decks/backside/SR卡.png');
  border-radius: 10px;
}
.cell.rarity-ur .card .back {
  background-image: url('@/assets/img/Decks/backside/UR卡.png');
  border-radius: 10px;
}
.card .front{ transform: rotateY(180deg); background: linear-gradient(145deg,#ffffff,#f8fafc); }

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
  border-radius: 10px;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #e2e8f0, #cbd5e1);
  color: #64748b;
  font-size: 16px;
  font-weight: bold;
  border-radius: 6px;
}

.card-info-below {
  position: absolute;
  bottom: -55px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  background: transparent;
  color: #333;
  padding: 10px 12px;
  border-radius: 8px;
  min-width: 80px;
  z-index: 10;
}

.card-info-below .rarity {
  font-size: 18px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-info-below .name {
  font-size: 18px;
  font-weight: 600;
  text-align: center;
  line-height: 1.2;
  max-width: 200px;
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





.rarity{ font-weight:800; letter-spacing:.5px; font-size:12px; }
.name{ color:#2b2f36; font-weight:600; font-size:10px; text-align:center; line-height:1.2; max-width:70px; }

/* 稀有度颜色 */
.rarity-b { color: #b5c0d0; }
.rarity-a { color: #6dd5ed; }
.rarity-r { color: #a770ef; }
.rarity-sr { color: #fdbb2d; }
.rarity-ur { color: #ff6b6b; }

.r-sr .card{ box-shadow: 0 8px 20px rgba(167,112,239,.18), inset 0 0 0 1px rgba(167,112,239,.25); }
.r-ur .card{ box-shadow: 0 10px 24px rgba(255,107,107,.28), inset 0 0 0 1px rgba(255,107,107,.35); }
.card .beam{ position:absolute; left:50%; bottom:-10%; width:24%; height:140%; transform: translateX(-50%); pointer-events:none; background: linear-gradient(to top, rgba(255,107,107,.0), rgba(255,107,107,.7), rgba(255,107,107,0)); filter: blur(4px); animation: beamUp 1.2s ease forwards; }
@keyframes beamUp{ from{ opacity:0; transform: translateX(-50%) scaleY(.4);} 30%{ opacity:1;} to{ opacity:0; transform: translateX(-50%) scaleY(1);} }

.actions{ display:flex; justify-content:center; padding:0 0 4px; }

.fade-scale-enter-from, .fade-scale-leave-to{ opacity:0; transform: scale(.96); }
.fade-scale-enter-active, .fade-scale-leave-active{ transition: all .28s ease; }

@media (max-width:768px){
  .panel{ width:94vw; padding:12px; }
  .grid{ grid-template-columns: repeat(2, 1fr); }
}
</style>


