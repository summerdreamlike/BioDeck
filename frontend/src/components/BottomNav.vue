<template>
  <div class="nav-wrap" v-if="!hideNav">
    <div class="nav-bar">
      <button class="nav-item" :class="{ active: isActive('/StudentSide/Home') }" @click="go('/StudentSide/Home')">
        <i class="icon">🏁</i>
        <span class="label">闯关</span>
      </button>
      <button class="nav-item" :class="{ active: isActive('/StudentSide/draw') }" @click="go('/StudentSide/draw')">
        <i class="icon">🎴</i>
        <span class="label">抽卡</span>
      </button>
      <button class="nav-item" :class="{ active: isActive('/StudentSide/atlas') }" @click="go('/StudentSide/atlas')">
        <i class="icon">🗺️</i>
        <span class="label">卡组</span>
      </button>
      <button class="nav-item" :class="{ active: isActive('/StudentSide/achievements') }" @click="go('/StudentSide/achievements')">
        <i class="icon">🏆</i>
        <span class="label">成就</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const hideNav = computed(() => {
  const byMeta = !!(route.meta && route.meta.hideBottomNav)
  const byPath = /profile|UserProfile/i.test(route.path || '')
  return byMeta || byPath
})

function go(path){
  if (route.path !== path){
    router.push(path)
  }
}
function isActive(path){
  return route.path === path
}
</script>

<style scoped>
.nav-wrap{
  position: sticky; left: 50%; bottom: max(0px, env(safe-area-inset-bottom)); transform: translateX(-50%);
  width: 20vw; min-width: 360px; max-width: 560px; height: 85px;
  pointer-events: none; /* 仅导航条可交互 */
  z-index: 999;
}
.nav-bar{
  pointer-events: auto;
  margin: 0 auto 10px; height: 48px; padding: 8px 10px; border-radius: 16px;
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; align-items: center;
  background: rgba(255,255,255,0.5); 
  backdrop-filter: blur(24px) saturate(180%) contrast(110%);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(110%);
  border: 1px solid rgba(255,255,255,0.28);
  box-shadow: var(--shadow-elev);
  transition: opacity .22s ease, box-shadow .22s ease;
  overflow: hidden;
  transform: translateY(0) scale(1);
  opacity: 1;
}

.nav-item{
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  height: 100%; border: none; background: transparent; color: #1f2937; cursor: pointer;
  border-radius: 12px; transition: all .3s cubic-bezier(0.4, 0, 0.2, 1); outline: none; padding: 0 8px;
  transform: translateY(0) scale(1);
  position: relative;
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  transition: left 0.5s;
}

.nav-item:hover::before {
  left: 100%;
}

.nav-item:hover{ 
  background: rgba(255,255,255,0.25); 
  transform: translateY(-2px) scale(1.05); 
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.nav-item.active{ 
  background: rgba(64,158,255,0.25); 
  color: #1677ff; 
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 15px rgba(64,158,255,0.3);
}

.nav-item.active:hover {
  background: rgba(64,158,255,0.35);
  transform: translateY(-3px) scale(1.07);
  box-shadow: 0 12px 30px rgba(64,158,255,0.4);
}

.icon{ 
  font-size: 18px;
  line-height: 1;
  transition: all .3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: scale(1);
}

.nav-item:hover .icon {
  transform: scale(1.3);
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.2));
}

.nav-item.active .icon {
  transform: scale(1.1);
  filter: drop-shadow(0 2px 8px rgba(64,158,255,0.3));
}

.nav-item.active:hover .icon {
  transform: scale(1.4);
  filter: drop-shadow(0 4px 12px rgba(64,158,255,0.5));
}

.label{ 
  font-size: 14px;
  font-weight: 600; 
  opacity: 1; 
  transform: translateY(0); 
  transition: all .3s cubic-bezier(0.4, 0, 0.2, 1); 
  white-space: nowrap; 
}

.nav-item:hover .label {
  transform: translateY(-2px);
  color: #1677ff;
  text-shadow: 0 2px 4px rgba(22,119,255,0.2);
}

.nav-item.active .label {
  transform: translateY(-1px);
  text-shadow: 0 1px 3px rgba(64,158,255,0.3);
}

.nav-item.active:hover .label {
  transform: translateY(-3px);
  text-shadow: 0 2px 6px rgba(64,158,255,0.4);
}

/* 直接显示：按钮常显 */
.nav-bar .nav-item{ opacity: 1; pointer-events: auto; }

@media (max-width: 640px){
  .nav-wrap{ width: 88vw; min-width: 0; }
}
</style>


