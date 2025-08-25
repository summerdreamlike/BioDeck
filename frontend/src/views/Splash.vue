<template>
  <section class="splash" :class="{ leaving: exiting }" role="region" aria-label="启动页">
    <div class="brand">
      <div class="logo-wrap">
        <div class="pulse"></div>
        <div class="logo">
          <span class="glyph">生</span>
          <span class="ring" aria-hidden="true"></span>
        </div>
      </div>
      <h1 class="title">卡生卡物</h1>
    </div>
    <p class="subtitle">正在加载，请稍候<span class="dots"><span>.</span><span>.</span><span>.</span></span></p>
  </section>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
let timer
let navTimer
const exiting = ref(false)

onMounted(() => {
  // 短暂展示后进入主应用
  timer = setTimeout(() => {
    exiting.value = true
    // 等待退出动画完成再跳转
    navTimer = setTimeout(() => router.push('/Login'), 600)
  }, 1000)
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

.logo-wrap {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 16px;
}

.pulse {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(16,185,129,0.18), rgba(16,185,129,0.04) 60%, transparent 70%);
  animation: ripple 2s infinite ease-out;
}

.logo {
  position: relative;
  z-index: 1;
  width: 120px;
  height: 120px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #10b981, #34d399);
  color: #ffffff;
  font-size: 64px;
  font-weight: 800;
  box-shadow: 0 16px 32px rgba(16, 185, 129, 0.25);
  transform: translateZ(0);
  overflow: hidden;
}

.logo .glyph { position: relative; z-index: 2; }

.logo .ring {
  position: absolute;
  width: 160px;
  height: 160px;
  border-radius: 50%;
  border: 4px solid rgba(255,255,255,0.25);
  box-shadow: 0 0 20px rgba(255,255,255,0.2) inset;
  animation: spin 3.2s linear infinite;
}

.title {
  font-size: 40px;
  font-weight: 700;
  margin: 0;
}

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
</style>

