<template>
  <div class="atlas">
    <div v-if="view==='shelf'" class="shelf-view">
      <div class="header">
        <h2>卡组图谱</h2>
        <div class="tools">
          <input class="search" v-model="q" type="search" placeholder="搜索卡组…" />
          <div class="arrows">
            <button class="arrow" @click="scrollLeft" title="上一组">◀</button>
            <button class="arrow" @click="scrollRight" title="下一组">▶</button>
          </div>
        </div>
        <div class="sub">左右滑动浏览不同卡组，点击进入查看卡牌</div>
      </div>
      <div class="shelf" ref="shelfRef">
        <div class="shelf-track">
          <div v-for="deck in filteredDecks" :key="deck.id" class="deck" @click="openDeck(deck)">
            <InteractiveCard
              :image-src="deck.cover"
              :alt-text="deck.name"
              :gif-src="sparklesGif"
              :size-mode="'responsive'"
              :width="'100%'"
              :aspect-ratio="'3/5'"
              :border-radius="'16px'"
              :max-tilt="15"
              :range-scale="1.4"
              :hover-scale="1.05"
              :enable-hover-effect="true"
              :enable-animation="true"
              :enable-silver-outline="true"
              :enable-gif="true"
            >
              <template #overlay>
                <div class="deck-overlay">
                  <div class="cover-mask"></div>
                  <div class="cover-title">
                    <span class="emoji">{{ deck.emoji }}</span>
                    <span class="name">{{ deck.name }}</span>
                  </div>
                </div>
              </template>
            </InteractiveCard>
            <div class="book-shadow"></div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="detail-view">
      <div class="detail-header">
        <button class="back" @click="view='shelf'">← 返回书架</button>
        <div class="title">
          <span class="emoji">{{ activeDeck?.emoji }}</span>
          <span>{{ activeDeck?.name }}</span>
        </div>
      </div>
      <div class="cards-grid">
        <div v-for="card in cards" :key="card.id" class="card" :class="{ locked: !card.unlocked }">
          <InteractiveCard
            :image-src="card.cover || ''"
            :gif-src="sparklesGif"
            :alt-text="card.name"
            :size-mode="'fixed'"
            :width="'140px'"
            :aspect-ratio="'3/4'"
            :border-radius="'14px'"
            :max-tilt="12"
            :range-scale="1.3"
            :hover-scale="1.02"
            :enable-hover-effect="true"
            :enable-animation="true"
            :enable-silver-outline="true"
            :enable-gif="true"
          >
            <template #overlay>
              <div class="card-overlay">
                <div class="card-cover">
                  <span class="c-emoji">{{ card.emoji }}</span>
                </div>
                <div class="card-name">{{ card.name }}</div>
                <div v-if="!card.unlocked" class="lock">
                  <span class="lock-ico">🔒</span>
                  <span class="lock-text">未解锁</span>
                </div>
              </div>
            </template>
          </InteractiveCard>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import InteractiveCard from '@/components/InteractiveCard.vue'
import sparklesGif from '@/assets/gif/sparkles.gif'

const view = ref('shelf')
const shelfRef = ref(null)
const q = ref('')
const activeDeck = ref(null)
const cards = ref([])

// 使用本地 src/assets/img/Decks 下的图片作为封面
const deckCtx = require.context('../../assets/img/Decks', false, /\.(png|jpe?g|webp)$/)
const deckFiles = deckCtx.keys()
const emojiPool = ['🧬','⚡','🧪','🔬','🌿','📚','🧫','🧠']
const prettyName = (k) => {
  const base = k.replace(/^\.\//,'').replace(/\.[^.]+$/,'')
  return base.replace(/[_-]+/g,' ').replace(/\b\w/g, s => s.toUpperCase())
}
const decks = ref(deckFiles.map((k, i) => ({
  id: i + 1,
  name: prettyName(k),
  emoji: emojiPool[i % emojiPool.length],
  cover: deckCtx(k),
})))

const filteredDecks = computed(() => {
  const kw = q.value.trim().toLowerCase()
  if (!kw) return decks.value
  return decks.value.filter(d => d.name.toLowerCase().includes(kw))
})

// 书架交互：左右按钮与鼠标拖拽滚动
function scrollByDeck(count){
  const el = shelfRef.value?.querySelector('.shelf-track')
  if (!el) return
  const deckWidth = el.querySelector('.deck')?.getBoundingClientRect()?.width || 220
  el.scrollBy({ left: deckWidth * count, behavior: 'smooth' })
}
function scrollLeft(){ scrollByDeck(-1) }
function scrollRight(){ scrollByDeck(1) }

let isDown = false, startX = 0, startScroll = 0
function onDown(e){
  const el = shelfRef.value?.querySelector('.shelf-track')
  if (!el) return
  isDown = true
  startX = (e.touches ? e.touches[0].clientX : e.clientX)
  startScroll = el.scrollLeft
}
function onMove(e){
  if (!isDown) return
  const el = shelfRef.value?.querySelector('.shelf-track')
  if (!el) return
  const x = (e.touches ? e.touches[0].clientX : e.clientX)
  el.scrollLeft = startScroll - (x - startX)
}
function onUp(){ isDown = false }

onMounted(() => {
  const el = shelfRef.value?.querySelector('.shelf-track')
  if (!el) return
  el.addEventListener('mousedown', onDown)
  el.addEventListener('mousemove', onMove)
  el.addEventListener('mouseup', onUp)
  el.addEventListener('mouseleave', onUp)
  el.addEventListener('touchstart', onDown, { passive: true })
  el.addEventListener('touchmove', onMove, { passive: true })
  el.addEventListener('touchend', onUp, { passive: true })
})
onBeforeUnmount(() => {
  const el = shelfRef.value?.querySelector('.shelf-track')
  if (!el) return
  el.removeEventListener('mousedown', onDown)
  el.removeEventListener('mousemove', onMove)
  el.removeEventListener('mouseup', onUp)
  el.removeEventListener('mouseleave', onUp)
  el.removeEventListener('touchstart', onDown)
  el.removeEventListener('touchmove', onMove)
  el.removeEventListener('touchend', onUp)
})

function openDeck(deck){
  activeDeck.value = deck
  // 模拟卡牌：部分解锁，部分未解锁
  cards.value = Array.from({length: 18}, (_,i)=>({
    id: i+1,
    name: `${deck.name} · 卡牌 ${i+1}`,
    emoji: ['🧬','🧫','🧪','🔬','🧲','⚛️','🧯','🧱'][i%8],
    unlocked: i % 3 !== 0,
    cover: deck.cover // 使用卡组封面作为卡牌背景
  }))
  view.value = 'detail'
}
</script>

<style scoped>
/* 深色场景，突出内容 */
.atlas{ position: relative; min-height: 100vh; padding: 20px; color: #e5e7eb;
  background:
    radial-gradient(60% 40% at 20% 15%, rgba(59,130,246,.12), transparent 60%),
    radial-gradient(50% 40% at 80% 85%, rgba(16,185,129,.10), transparent 60%),
    linear-gradient(180deg, #0b1020 0%, #0f172a 100%);
}

.header{ margin-bottom: 14px; }
.header h2{ margin: 0 0 8px; font-weight: 700; color: #f9fafb; }
.tools{ display: flex; gap: 10px; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.search{ flex: 1; appearance: none; background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.14); color: #e5e7eb; padding: 8px 12px; border-radius: 12px; outline: none; transition: all .18s ease; }
.search::placeholder{ color: #9ca3af; }
.search:focus{ border-color: rgba(255,255,255,.28); box-shadow: 0 0 0 3px rgba(255,255,255,.14) inset; }
.arrows{ display: inline-flex; gap: 8px; }
.arrow{ appearance: none; border: 1px solid rgba(255,255,255,.18); color: #e5e7eb; background: rgba(255,255,255,.06); padding: 8px 10px; border-radius: 10px; cursor: pointer; transition: all .18s ease; }
.arrow:hover{ transform: translateY(-1px); background: rgba(255,255,255,.1); }
.header .sub{ color: #93a2b7; font-size: 13px; }

/* 书架：横向滚动 + 书影 */
.shelf{ overflow: hidden; border-radius: 18px; }
.shelf-track{ display: grid; grid-auto-flow: column; grid-auto-columns: clamp(180px, 22vw, 240px); gap: 18px;
  overflow-x: auto; padding: 18px; scroll-snap-type: x mandatory; }
.shelf-track::-webkit-scrollbar{ height: 8px; }
.shelf-track::-webkit-scrollbar-thumb{ background: rgba(255,255,255,.18); border-radius: 999px; }

.deck{ position: relative; scroll-snap-align: start; cursor: pointer; }

/* InteractiveCard overlay 样式 */
.deck-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  z-index: 10;
}

.cover-mask{ 
  position: absolute; 
  inset: 0; 
  background: linear-gradient(180deg, rgba(0,0,0,.15), rgba(0,0,0,.45)); 
  z-index: 1;
}

.cover-title{ 
  position: relative;
  left: 12px; 
  bottom: 10px; 
  right: 12px; 
  display: flex; 
  gap: 8px; 
  align-items: center; 
  color: #f9fafb; 
  text-shadow: 0 1px 2px rgba(0,0,0,.6);
  z-index: 2;
}

.emoji{ font-size: 18px; }
.name{ font-weight: 700; }
.book-shadow{ height: 10px; margin: 8px 12px 0; border-radius: 999px; background: radial-gradient(60% 100% at 50% -10%, rgba(0,0,0,.35), rgba(0,0,0,0)); filter: blur(2px); }

/* 详情：卡牌网格 */
.detail-header{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.back{ appearance: none; border: 1px solid rgba(255,255,255,.18); color: #e5e7eb; background: rgba(255,255,255,.06); padding: 6px 10px; border-radius: 10px; cursor: pointer;
  transition: all .18s ease; }
.back:hover{ transform: translateY(-1px); background: rgba(255,255,255,.1); }
.title{ display: inline-flex; gap: 8px; align-items: center; font-weight: 700; color: #f9fafb; }

.cards-grid{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 14px; }

/* InteractiveCard overlay 样式 */
.card-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.card-cover{ 
  height: 120px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  background: radial-gradient(50% 60% at 50% 35%, rgba(255,255,255,.08), rgba(255,255,255,0)); 
  border-radius: 10px; 
  margin-bottom: 8px; 
}

.c-emoji{ font-size: 40px; filter: drop-shadow(0 4px 8px rgba(0,0,0,.3)); }
.card-name{ font-size: 13px; color: #cbd5e1; text-align: center; }

.lock{ 
  position: absolute; 
  inset: 0; 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  justify-content: center; 
  gap: 6px; 
  background: rgba(15,23,42,.58);
  z-index: 20;
}

.lock-ico{ font-size: 20px; }
.lock-text{ font-size: 12px; color: #94a3b8; }

/* 移除旧的卡片样式，因为现在使用InteractiveCard */
.card { 
  position: relative; 
  background: transparent; 
  border: none; 
  padding: 0; 
  box-shadow: none; 
}

.card:hover { 
  transform: none; 
  box-shadow: none; 
  background: transparent; 
}

.card.locked .card-cover{ filter: grayscale(40%); opacity: .7; }

@media (max-width: 640px){
  .atlas{ padding: 14px; }
}
</style>


