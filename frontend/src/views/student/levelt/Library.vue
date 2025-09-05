<template>
  <div class="g-scroll"></div>
    <div class="g-wrapper">
    <div class="g-inner" ref="innerRef">
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
        <div class="g-item"></div>
    </div>
</div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const innerRef = ref(null)
let phase = 0
let target = 0
let raf = 0
const speed = 0.15
const minPhase = 0
let maxPhase = 0

function clamp(v,a,b){ return Math.max(a, Math.min(b, v)) }

function onWheel(e){
  e.preventDefault()
  target = clamp(target + (e.deltaY||0) * speed, minPhase, maxPhase)
  tick()
}

function tick(){
  cancelAnimationFrame(raf)
  phase += (target - phase) * 0.08
  const el = innerRef.value
  if (el) el.style.setProperty('--phase', `${Math.round(phase)}px`)
  if (Math.abs(target - phase) > 0.5){ raf = requestAnimationFrame(tick) }
}

function onResize(){
  const vh = window.innerHeight
  // 最大推进距离与视口相关，留出 200px 余量
  maxPhase = Math.round(vh + 200)
}

onMounted(() => {
  document.body.style.overflow = 'hidden'
  onResize()
  // 初始化更近的起始距离并立即应用，避免首屏错位
  phase = target = Math.min(150, maxPhase)
  const elInit = innerRef.value
  if (elInit) elInit.style.setProperty('--phase', `${Math.round(phase)}px`)
  window.addEventListener('resize', onResize, { passive:true })
  window.addEventListener('wheel', onWheel, { passive:false })
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  window.removeEventListener('resize', onResize)
  window.removeEventListener('wheel', onWheel)
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
    overflow-y: auto;
}
.g-wrapper {
    position: fixed;
    top: -20%;
    width: 100vw;
    height: 100vh;
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

.g-item {
    width: 300px;
    height: 100px;
    background: #000;
    transform: rotateX(-90deg);
}

</style>