<template>
  <div class="interactive-card-stage" ref="stageRef" @mouseenter="onEnter" @mousemove="onMove" @mouseleave="onLeave">
    <div class="card-frame" ref="frameRef" :style="[cardTransformStyle, cardStyle]">
      <div class="card-art" ref="artRef">
                 <!-- 背景图片 -->
         <img 
           v-if="imageSrc" 
           :src="imageSrc" 
           :alt="altText || 'Card Image'"
           class="card-background"
           @load="onImageLoad"
           ref="imageRef"
         />
        
        <!-- GIF叠加层 -->
        <img 
          v-if="gifSrc && enableGif" 
          :src="gifSrc" 
          :alt="gifAlt || 'GIF Overlay'"
          class="gif-overlay"
        />
        
        <!-- 镭射叠加层 -->
        <img 
          v-if="laserSrc && enableLaser" 
          :src="laserSrc" 
          :alt="laserAlt || 'Laser Overlay'"
          class="laser-overlay"
        />
        
                 <!-- 插槽内容 -->
         <slot name="overlay"></slot>
       </div>
       
       <!-- 图片缩放控制器 -->
       <div v-if="enableImageScale" class="image-scale-controls">
         <button class="scale-btn" @click="zoomOut" title="缩小">−</button>
         <button class="scale-btn" @click="zoomIn" title="放大">+</button>
         <button class="scale-btn" @click="resetZoom" title="重置">↺</button>
       </div>
     </div>
   </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Props定义
/* global defineProps */
const props = defineProps({
  // 背景图片
  imageSrc: {
    type: String,
    default: ''
  },
  // 背景图片alt文本
  altText: {
    type: String,
    default: ''
  },
  // GIF叠加层
  gifSrc: {
    type: String,
    default: ''
  },
  // GIF alt文本
  gifAlt: {
    type: String,
    default: ''
  },
  // 镭射图片源
  laserSrc: {
    type: String,
    default: ''
  },
  // 镭射图片alt文本
  laserAlt: {
    type: String,
    default: ''
  },
    // 卡片尺寸模式
  sizeMode: {
    type: String,
    default: 'fixed' // 'fixed' | 'responsive' | 'auto'
  },
  // 固定宽度
  width: {
    type: String,
    default: 'clamp(220px, 42vw, 300px)'
  },
  // 宽高比
  aspectRatio: {
    type: String,
    default: '3/6'
  },
  // 自动尺寸时的最大宽度
  maxWidth: {
    type: String,
    default: '600px'
  },
  // 自动尺寸时的最大高度
  maxHeight: {
    type: String,
    default: '800px'
  },
  // 图片缩放比例
  imageScale: {
    type: Number,
    default: 1.0
  },
  // 是否启用图片缩放
  enableImageScale: {
    type: Boolean,
    default: false
  },
  // 圆角
  borderRadius: {
    type: String,
    default: '16px'
  },
  // 最大倾斜角度
  maxTilt: {
    type: Number,
    default: 18
  },
  // 交互范围缩放
  rangeScale: {
    type: Number,
    default: 1.6
  },
  // 悬停缩放
  hoverScale: {
    type: Number,
    default: 1.03
  },
  // 是否启用悬停效果
  enableHoverEffect: {
    type: Boolean,
    default: true
  },
  // 是否启用动画
  enableAnimation: {
    type: Boolean,
    default: true
  },
  // 是否启用银色轮廓
  enableSilverOutline: {
    type: Boolean,
    default: true
  },
  // 是否启用GIF叠加层
  enableGif: {
    type: Boolean,
    default: true
  },
  // 是否启用镭射效果
  enableLaser: {
    type: Boolean,
    default: true
  }
})

// 3D 跟随状态
const stageRef = ref(null)
const frameRef = ref(null)
const artRef = ref(null)
const tiltX = ref(0)
const tiltY = ref(0)
const scale = ref(1)
const rafId = ref(0)

// 图片尺寸状态
const imageNaturalSize = ref({ width: 0, height: 0 })
const imageLoaded = ref(false)

// 当前缩放比例
const currentScale = ref(1.0)

// 进入事件
function onEnter() {
  if (!props.enableHoverEffect) return
  scale.value = props.hoverScale
  if (artRef.value) {
    artRef.value.style.setProperty('--per', '0%')
    artRef.value.style.setProperty('--gold-opacity', '0')
  }
}

// 移动事件
function onMove(e) {
  if (!props.enableHoverEffect) return
  
  const frame = frameRef.value
  const art = artRef.value
  if (!frame || !art) return

  // 倾斜用 frame 尺寸
  const fr = frame.getBoundingClientRect()
  const cx = fr.left + fr.width / 2
  const cy = fr.top + fr.height / 2
  const rx = (fr.width / 2) * props.rangeScale
  const ry = (fr.height / 2) * props.rangeScale
  const nx = Math.max(-1, Math.min(1, (e.clientX - cx) / rx))
  const ny = Math.max(-1, Math.min(1, (e.clientY - cy) / ry))
  const targetTiltX = -ny * props.maxTilt
  const targetTiltY = nx * props.maxTilt

  // 高光用 art 尺寸（更贴合视觉）
  const ar = art.getBoundingClientRect()
  const per = Math.max(0, Math.min(100, ((e.clientX - ar.left) / ar.width) * 100))

  // rAF 插值更新，提升稳定度与精度
  cancelAnimationFrame(rafId.value)
  rafId.value = requestAnimationFrame(() => {
    tiltX.value += (targetTiltX - tiltX.value) * 0.25
    tiltY.value += (targetTiltY - tiltY.value) * 0.25
    
    // 设置高光位置
    art.style.setProperty('--per', `${per}%`)
    
    // 确保银色轮廓跟随高光位置
    if (props.enableSilverOutline && per > 5) {
      art.style.setProperty('--gold-opacity', '1')
    } else {
      art.style.setProperty('--gold-opacity', '0')
    }
  })
}

// 离开事件
function onLeave() {
  if (!props.enableHoverEffect) return
  cancelAnimationFrame(rafId.value)
  tiltX.value = 0
  tiltY.value = 0
  scale.value = 1
  if (artRef.value) {
    artRef.value.style.setProperty('--per', '0%')
    artRef.value.style.setProperty('--gold-opacity', '0')
  }
}

// 计算变换样式
const cardTransformStyle = computed(() => ({
  transform: `rotateX(${tiltX.value}deg) rotateY(${tiltY.value}deg) scale(${scale.value})`
}))

// 图片加载处理
function onImageLoad(e) {
  const img = e.target
  imageNaturalSize.value = {
    width: img.naturalWidth,
    height: img.naturalHeight
  }
  imageLoaded.value = true
  // 重置缩放比例
  currentScale.value = 1.0
}

// 计算缩放后的图片尺寸
function getScaledImageSize() {
  if (!imageLoaded.value) return { width: 0, height: 0 }
  
  const { width: imgWidth, height: imgHeight } = imageNaturalSize.value
  let scaledWidth = imgWidth
  let scaledHeight = imgHeight
  
  // 使用当前缩放比例
  if (props.enableImageScale) {
    scaledWidth = imgWidth * currentScale.value
    scaledHeight = imgHeight * currentScale.value
  } else if (props.imageScale !== 1.0) {
    scaledWidth = imgWidth * props.imageScale
    scaledHeight = imgHeight * props.imageScale
  }
  
  return { width: scaledWidth, height: scaledHeight }
}

// 缩放控制函数
function zoomIn() {
  currentScale.value = Math.min(currentScale.value * 1.2, 3.0) // 最大3倍
}

function zoomOut() {
  currentScale.value = Math.max(currentScale.value / 1.2, 0.3) // 最小0.3倍
}

function resetZoom() {
  currentScale.value = 1.0
}

// 计算卡片样式
const cardStyle = computed(() => {
  if (props.sizeMode === 'responsive') {
    return {
      width: '100%',
      aspectRatio: props.aspectRatio,
      borderRadius: props.borderRadius
    }
  } else if (props.sizeMode === 'auto' && imageLoaded.value) {
    // 根据图片缩放后的尺寸计算，但限制最大尺寸
    const { width: imgWidth, height: imgHeight } = getScaledImageSize()
    const aspectRatio = imgWidth / imgHeight
    
    // 计算合适的尺寸，保持图片比例
    let finalWidth = imgWidth
    let finalHeight = imgHeight
    
    // 限制最大宽度和高度
    if (finalWidth > parseInt(props.maxWidth)) {
      finalWidth = parseInt(props.maxWidth)
      finalHeight = finalWidth / aspectRatio
    }
    
    if (finalHeight > parseInt(props.maxHeight)) {
      finalHeight = parseInt(props.maxHeight)
      finalWidth = finalHeight * aspectRatio
    }
    
    return {
      width: `${finalWidth}px`,
      height: `${finalHeight}px`,
      borderRadius: props.borderRadius
    }
  } else {
    // 固定尺寸模式
    return {
      width: props.width,
      aspectRatio: props.aspectRatio,
      borderRadius: props.borderRadius
    }
  }
})
</script>

<style scoped>
.interactive-card-stage {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 34px 3% 12px;
  perspective: 900px;
}

.card-frame {
  position: relative;
  background: linear-gradient(145deg, #eef2f7, #ffffff, #f0f4ff, #ffffff);
  background-size: 200% 200%;
  box-shadow: 0 20px 40px rgba(0,0,0,.08), inset 0 0 0 1px rgba(0,0,0,.04);
  overflow: hidden;
  transition: transform .22s cubic-bezier(.22,.61,.36,1), box-shadow .22s, background-position 3s ease-in-out;
  transform-style: preserve-3d;
  animation: subtleFloat 6s ease-in-out infinite;
}

/* 自动尺寸模式下的特殊处理 */
.card-frame[style*="height"] {
  aspect-ratio: unset;
}

/* 图片缩放控制器 */
.image-scale-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
  z-index: 10;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.interactive-card-stage:hover .image-scale-controls {
  opacity: 1;
}

.scale-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.scale-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.scale-btn:active {
  transform: scale(0.95);
}

.card-art {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  overflow: hidden;
}

.card-background {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
}

.gif-overlay {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  mix-blend-mode: screen;
  pointer-events: none;
  opacity: 0.9;
  border-radius: inherit;
  z-index: 1;
}

/* 镭射叠加层 - 只在有高光时显示，不阻挡背景图片 */
.laser-overlay {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  mix-blend-mode: soft-light;
  pointer-events: none;
  border-radius: inherit;
  z-index: 3;
  opacity: 0;
  transition: opacity 0.3s ease;
  /* 使用CSS变量控制显示区域 */
  mask: linear-gradient(120deg,
    transparent calc(var(--per, 0%) - 30%),
    rgba(255,255,255,0.1) calc(var(--per, 0%) - 25%),
    rgba(255,255,255,0.3) calc(var(--per, 0%) - 20%),
    rgba(255,255,255,0.6) calc(var(--per, 0%) - 15%),
    rgba(255,255,255,0.8) calc(var(--per, 0%) - 10%),
    rgba(255,255,255,1) calc(var(--per, 0%) - 5%),
    rgba(255,255,255,1) var(--per, 0%),
    rgba(255,255,255,1) calc(var(--per, 0%) + 5%),
    rgba(255,255,255,0.8) calc(var(--per, 0%) + 10%),
    rgba(255,255,255,0.6) calc(var(--per, 0%) + 15%),
    rgba(255,255,255,0.3) calc(var(--per, 0%) + 20%),
    rgba(255,255,255,0.1) calc(var(--per, 0%) + 25%),
    transparent calc(var(--per, 0%) + 30%));
  mask-size: 200% 200%;
  mask-position: calc(var(--per, 0%) - 100%) 50%;
}

/* 当有高光时显示镭射效果，但透明度较低 */
.card-art[style*="--per: 0%"] .laser-overlay {
  opacity: 0;
}

.card-art[style*="--per"] .laser-overlay {
  opacity: 0.3;
}

/* 高光覆层使用 --per 控制位置 */
.card-art::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: inherit;
  background: 
    /* 左上到右下的斜向高光 - 明亮版 */
    linear-gradient(120deg,
      transparent calc(var(--per, 0%) - 25%),
      rgba(255,255,255,.2) calc(var(--per, 0%) - 20%),
      rgba(255,255,255,.3) calc(var(--per, 0%) - 15%),
      rgba(255,255,255,.5) calc(var(--per, 0%) - 10%),
      rgba(255,255,255,.6) calc(var(--per, 0%) - 8%),
      rgba(255,255,255,.75) calc(var(--per, 0%) - 4%),
      rgba(255,255,255,.75) var(--per, 0%),
      rgba(255,255,255,.75) calc(var(--per, 0%) + 4%),
      rgba(255,255,255,.6) calc(var(--per, 0%) + 8%),
      rgba(255,255,255,.5) calc(var(--per, 0%) + 10%),
      rgba(255,255,255,.3) calc(var(--per, 0%) + 15%),
      rgba(255,255,255,.2) calc(var(--per, 0%) + 20%),
      transparent calc(var(--per, 0%) + 25%));
  mix-blend-mode: soft-light;
  filter: blur(0.3px);
  animation: shimmer 2s ease-in-out infinite;
  z-index: 1;
}

/* 闪银色轮廓 - 只在有高光时显示 */
.card-art::after {
  content: "";
  position: absolute;
  inset: -2px;
  pointer-events: none;
  border-radius: inherit;
  background: 
    linear-gradient(108deg, 
      transparent 0%,
      rgba(192, 192, 192, 0) 25%,
      rgba(192, 192, 192, 0.4) 35%,
      rgba(192, 192, 192, 0.7) 45%,
      rgba(192, 192, 192, 0.9) 50%,
      rgba(192, 192, 192, 0.7) 55%,
      rgba(192, 192, 192, 0.4) 65%,
      rgba(192, 192, 192, 0) 75%,
      transparent 100%);
  background-size: 200% 200%;
  background-position: calc(var(--per, 0%) - 100%) 50%;
  mix-blend-mode: soft-light;
  opacity: var(--gold-opacity, 0);
  transition: opacity 0.2s ease;
  filter: blur(1.5px);
  z-index: 2;
  animation: silverShimmer 3s ease-in-out infinite;
}

/* 动画关键帧 */
@keyframes subtleFloat {
  0%, 100% { 
    background-position: 0% 0%;
  }
  25% { 
    background-position: 100% 0%;
  }
  50% { 
    background-position: 100% 100%;
  }
  75% { 
    background-position: 0% 100%;
  }
}

@keyframes shimmer {
  0%, 100% { 
    opacity: 1;
    filter: blur(0.3px) brightness(1.5);
  }
  50% { 
    opacity: 1;
    filter: blur(0.4px) brightness(1.8);
  }
}

@keyframes silverShimmer {
  0%, 100% { 
    filter: blur(0.8px) brightness(1) saturate(1);
  }
  50% { 
    filter: blur(1.2px) brightness(1.4) saturate(1.1);
  }
}

/* 鼠标悬停时的额外动效 */
.card-frame:hover {
  animation-play-state: paused;
  box-shadow: 
    0 25px 50px rgba(0,0,0,.12), 
    0 8px 16px rgba(0,0,0,.08),
    inset 0 0 0 1px rgba(255,215,0,.1);
}

.card-frame:hover .card-art::before {
  animation: shimmer 1s ease-in-out infinite;
}

.card-frame:hover .card-art::after {
  animation: silverShimmer 1.5s ease-in-out infinite;
}
</style>

