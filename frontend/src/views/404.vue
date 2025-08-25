<template>
  <section class="not-found" role="region" aria-labelledby="notFoundTitle" aria-describedby="notFoundDesc">
    <div class="decor decor-1" aria-hidden="true"></div>
    <div class="decor decor-2" aria-hidden="true"></div>
    <div class="card">
      <div class="code" aria-label="404">
        <span>4</span>
        <span>0</span>
        <span>4</span>
      </div>
      <h2 id="notFoundTitle" class="title">哎呀，页面走丢了</h2>
      <p id="notFoundDesc" class="subtitle">您访问的页面不存在或已被移动。请检查链接是否正确，或返回首页继续浏览。</p>
      <div class="actions">
        <el-button class="ghost-btn" round @click="goHome">
          <ElIconHouse class="btn-icon" aria-hidden="true" />
          回到首页
        </el-button>
        <el-button class="ghost-btn" round @click="goBack">
          <ElIconArrowLeft class="btn-icon" aria-hidden="true" />
          返回上一页
        </el-button>
      </div>
    </div>
  </section>
  
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('/dashboard')
}

function goBack() {
  router.back()
}
</script>

<style scoped>
.not-found {
  position: relative;
  min-height: 100vh;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
  background: radial-gradient(800px 400px at 15% 10%, rgba(34, 197, 94, 0.12), transparent),
              radial-gradient(800px 500px at 85% 90%, rgba(16, 185, 129, 0.12), transparent),
              linear-gradient(180deg, #f9fffb 0%, #ecfdf5 100%);
  color: #1f2937;
  overflow: hidden;
}

.decor {
  position: absolute;
  filter: blur(8px);
  opacity: 0.12;
  pointer-events: none;
  animation: float 10s ease-in-out infinite;
  z-index: -2;
}

.decor-1 {
  width: 260px;
  height: 260px;
  top: -40px;
  left: -40px;
  background: conic-gradient(from 180deg at 50% 50%, #86efac, #34d399, #a7f3d0, #86efac);
  border-radius: 50%;
}

.decor-2 {
  width: 320px;
  height: 320px;
  right: -60px;
  bottom: -60px;
  background: conic-gradient(from 0deg at 50% 50%, #bbf7d0, #6ee7b7, #86efac, #bbf7d0);
  border-radius: 50%;
  animation-duration: 14s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-12px) rotate(6deg); }
}

.card {
  position: relative;
  width: 100%;
  max-width: 720px;
  padding: 40px 28px;
  background: #ffffff;
  border: 1px solid rgba(16, 185, 129, 0.18);
  border-radius: 16px;
  box-shadow: 0 16px 32px rgba(16, 185, 129, 0.12), 0 10px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  text-align: center;
  z-index: 0;
  isolation: isolate;
}

/* 确保文字与按钮永远在毛玻璃之上 */
.card > * {
  position: relative;
  z-index: 2;
}

.code {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(8px, 2.5vw, 16px);
  font-size: clamp(64px, 12vw, 136px);
  font-weight: 800;
  letter-spacing: 2px;
  line-height: 1;
  margin-bottom: 12px;
  color: #22d1a0;
  text-shadow: none;
  position: relative;
  z-index: 3;
}

.code span {
  display: inline-block;
  transform-origin: 50% 60%;
  animation: wobble 3.2s ease-in-out infinite;
}

.code span:nth-child(2) {
  animation-delay: 0.15s;
}

.code span:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes wobble {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-6px) rotate(-2deg); }
  75% { transform: translateY(6px) rotate(2deg); }
}

.title {
  font-size: 22px;
  font-weight: 700;
  color: #065f46;
  margin: 4px 0 8px;
}

.subtitle {
  font-size: 12px;
  font-weight: 550;
  color: #4b5563;
  margin: 0 auto 18px;
  max-width: 530px;
}

.actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 8px;
}

.btn-icon {
  margin-right: 6px;
  vertical-align: middle;
}

/* 统一按钮为透明幽灵样式 */
.ghost-btn {
  background-color: transparent !important;
  border: 1px solid #10b981 !important; /* emerald-500 */
  color: #065f46 !important; /* teal-900 深色文字 */
  height: 42px;
  padding: 0 18px;
  border-radius: 999px;
  font-weight: 600;
}

.ghost-btn:hover,
.ghost-btn:focus {
  background-color: rgba(16, 185, 129, 0.08) !important;
  border-color: #10b981 !important;
}

.ghost-btn:active {
  background-color: rgba(16, 185, 129, 0.16) !important;
}

.ghost-btn:focus-visible {
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25) !important;
}

@media (min-width: 640px) {
  .card { padding: 56px 48px; }
  .code { gap: 16px; }
  .title { font-size: 26px; }
  .subtitle { font-size: 12px; }
}

@media (max-width: 420px) {
  .actions {
    flex-direction: column;
  }
  .actions .el-button {
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .decor {
    animation: none;
  }
  .code span {
    animation: none;
  }
}
</style>