<template>
  <div class="view-wrap" :class="[transitionName, { 'is-transitioning': isTransitioning }]">
    <router-view v-slot="{ Component }">
      <transition :name="transitionName" mode="out-in"
        @before-enter="onBefore" @after-enter="onAfter"
        @before-leave="onBefore" @after-leave="onAfter">
        <component :is="Component" />
      </transition>
    </router-view>
    <div class="overlay" aria-hidden="true"></div>
  </div>
  
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const transitionName = computed(() => route.meta?.transition || 'fade')
const isTransitioning = ref(false)

function onBefore() { isTransitioning.value = true }
function onAfter() { isTransitioning.value = false }
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .35s cubic-bezier(.2,.8,.2,1); }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Splash -> Login: 上出下入更顺滑 */
.splash-enter-active, .splash-leave-active { transition: transform .5s cubic-bezier(.2,.8,.2,1), opacity .5s cubic-bezier(.2,.8,.2,1); will-change: transform, opacity; }
.splash-enter-from { transform: translateY(10vh) scale(.98); opacity: 0; }
.splash-leave-to { transform: translateY(-12vh) scale(1.02); opacity: 0; }

.login-enter-active, .login-leave-active { transition: transform .5s cubic-bezier(.2,.8,.2,1), opacity .5s cubic-bezier(.2,.8,.2,1); will-change: transform, opacity; }
.login-enter-from { transform: translateY(12vh) scale(.98); opacity: 0; }
.login-leave-to { transform: translateY(10vh) scale(1.02); opacity: 0; }

.view-wrap { position: relative; min-height: 100vh; }
.overlay { position: fixed; inset: 0; pointer-events: none; opacity: 0; transition: opacity .45s cubic-bezier(.2,.8,.2,1); z-index: 10;
  background: radial-gradient(60% 40% at 20% 15%, rgba(16,185,129,.10), transparent 60%),
              radial-gradient(50% 40% at 80% 85%, rgba(167,243,208,.10), transparent 60%),
              linear-gradient(180deg, rgba(255,255,255,.70), rgba(255,255,255,.55));
}
.is-transitioning .overlay { opacity: .35; }
</style>
