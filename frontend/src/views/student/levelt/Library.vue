<template>
  <div class="g-scroll" id="g-scroll"></div>
  <div class="g-wrapper">
    <div class="g-mask"></div>
    <div class="g-inner" ref="innerRef">
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
        <div class="g-item">Lorem ipsum dolor sit amet consectetur adipisicing elit.</div>
    </div>
</div>
</template>
<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const innerRef = ref(null)
let onScrollFallback

onMounted(() => {
  const supportsScrollTimeline = CSS && (
    CSS.supports('animation-timeline: scroll()') ||
    CSS.supports('(animation-timeline: box-move)')
  )
  if (!supportsScrollTimeline) {
    const root = document.getElementById('g-scroll')
    const el = innerRef.value
    const update = () => {
      const vh = window.innerHeight
      const max = vh + 100
      const total = root ? root.getBoundingClientRect().height - vh : document.documentElement.scrollHeight - vh
      const scrolled = window.scrollY || document.documentElement.scrollTop || 0
      const progress = Math.max(0, Math.min(1, total ? scrolled / total : 0))
      el && el.style.setProperty('--phase', `${Math.round(progress * max)}px`)
    }
    onScrollFallback = () => update()
    window.addEventListener('scroll', onScrollFallback, { passive: true })
    window.addEventListener('resize', onScrollFallback, { passive: true })
    update()
  }
})

onBeforeUnmount(() => {
  if (onScrollFallback) {
    window.removeEventListener('scroll', onScrollFallback)
    window.removeEventListener('resize', onScrollFallback)
  }
})
</script>
<style scoped>
@property --phase {
  syntax: '<length>';
  inherits: false;
  initial-value: 15px;
}

html, body {
    width: 100%;
    height: 100%;
    display: flex;
}

.g-scroll {
    width: 100%;
    height: 1000vh;
    position: relative;
}
.g-wrapper {
    position: fixed;
    top: -20%;
    width: 100vw;
    height: 100vh;
    perspective: 200px;
    transform-style: preserve-3d;
}

.g-mask {
    position: fixed;
    width: 100vw;
    height: 120vh;
    background: rgba(0,0,0,.5);
    backdrop-filter: blur(5px);
    transform: translateZ(0);
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
    animation-name: move;
    animation-duration: 1s;
    animation-timeline: box-move; /* 使用滚动时间线 */
}

@scroll-timeline box-move {
    source: selector("#g-scroll");
    orientation: "vertical";
}

.g-item {
    width: 300px;
    height: 200px;
    padding: 8px;
    box-sizing: border-box;
    color: #fff;
    background: #000;
    transform: rotateX(-90deg);
}

@keyframes move {
    0% {
        --phase: 0;
    }
    100% {
        --phase: calc(100vh + 100px);
    }
}
</style> 