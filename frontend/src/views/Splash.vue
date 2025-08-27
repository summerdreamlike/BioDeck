<template>
  <section class="splash" :class="{ leaving: exiting }" role="region" aria-label="启动页">
    <div class="brand" :class="{ shifted: shiftLeft }">
      <div class="logo-wrap">
        <div class="pulse"></div>
        <img :src="logo2" alt="Logo" class="logo-img" />
      </div>
      <div class="brand-text" :class="{ show: showTitle }">
        <!-- <h1 class="title">卡生卡物</h1>
        <p class="tagline">Build Your Knowledge Deck</p> -->
        <img :src="logo1" alt="Logo" class="title" />
      </div>
    </div>
    <p class="subtitle">正在加载，请稍候<span class="dots"><span>.</span><span>.</span><span>.</span></span></p>
  </section>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import logo2 from '../assets/img/Logo2.png'
import logo1 from '../assets/img/Logo1.png'

const router = useRouter()
let timer
let navTimer
const exiting = ref(false)
const showTitle = ref(false)
const shiftLeft = ref(false)

onMounted(() => {
  // 1) 先显示图片，稍后推动到左侧并展示标题
  timer = setTimeout(() => {
    shiftLeft.value = true
    showTitle.value = true
    // 2) 再等待一段时间后退出到登录页
    navTimer = setTimeout(() => {
      exiting.value = true
      setTimeout(() => router.push('/Login'), 500)
    }, 
    900)
  }, 900)
})

onUnmounted(() => {
  if (timer) {
    clearTimeout(timer)
  }
  if (navTimer) {
    clearTimeout(navTimer)
  }
})
</script>

<style scoped>
.splash {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #ecfdf5 0%, #ffffff 100%);
  color: #065f46;
  text-align: center;
  padding: 24px;
  transition: transform 0.6s ease, opacity 0.6s ease;
}

.splash.leaving { transform: translateY(-20vh); opacity: 0; }

.brand { display: flex; align-items: center; gap: 16px; margin-bottom: 8px; }
.brand { transition: transform .6s ease, opacity .6s ease; justify-content: center; flex-wrap: nowrap; }
.brand.shifted { transform: translateX(-40px); justify-content: flex-start; }

.logo-wrap {
  position: relative;
  width: 160px;
  height: 160px;
  margin-bottom: 16px;
}

.pulse {
  display: none;
}

.logo-img { 
  position: relative; 
  z-index: 1; 
  width: 100%; 
  height: 100%; 
  border-radius: 16px; 
  object-fit: contain; 
  box-shadow: none; 
}

.brand-text { display: flex; flex-direction: column; opacity: 0; transform: translateX(12px); transition: opacity .8s ease, transform .8s ease, max-width .8s ease, margin-left .8s ease; max-width: 0; overflow: hidden; margin-left: 0; white-space: nowrap; }
.brand-text.show { opacity: 1; transform: translateX(0); max-width: 300px; margin-left: 12px; }

/* .title {
  font-size: 48px;
  font-weight: 300;
  margin: 0;
  white-space: nowrap;
} */
.title {
  position: relative;
  width: 100%; 
  height: 50%;
  margin: 0;
  object-fit: contain;
  white-space: nowrap;
}
.tagline { margin: 4px 0 0; font-size: 14px; color: #047857; opacity: .6; }

.subtitle {
  font-size: 14px;
  color: #047857;
}

.dots { display: inline-flex; margin-left: 2px; }
.dots span { opacity: 0.2; animation: blink 1.4s infinite; }
.dots span:nth-child(2) { animation-delay: 0.2s; }
.dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes ripple {
  0%   { transform: scale(0.85); opacity: 0.9; }
  70%  { transform: scale(1.35); opacity: 0.1; }
  100% { transform: scale(1.4); opacity: 0; }
}

@keyframes spin { to { transform: rotate(360deg); } }

@keyframes blink {
  0%, 100% { opacity: 0.2; }
  50%      { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .pulse { animation: none; }
  .logo .ring { animation: none; }
  .dots span { animation: none; opacity: 1; }
}

@media (min-width: 768px) {
  .logo-wrap { width: 200px; height: 200px; }
  .title { font-size: 56px; }
}
</style>

