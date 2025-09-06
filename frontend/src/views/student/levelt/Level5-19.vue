<template>
  <div class="lv519" :style="{ backgroundImage: `url('${bgUrl}')` }">
    <div class="overlay">
      <h1 class="title">第19关 · 光能选择</h1>
      <p class="rule goal" data-text="目标：结算时手牌同时拥有『CO₂』『H₂O』，且获得『ATP』。">目标：结算时手牌同时拥有『CO₂』『H₂O』，且获得『ATP』。</p>
      <div class="zones">
                  <div class="play-zone cards" :class="{ droppable: dragging }" @dragover.prevent @drop="dropToPlay">
            <div v-for="(c,i) in board" :key="'p-'+c+'-'+i" class="card small" draggable="true" @dragstart="onDragStartFromBoard(c,i)" @dragend="onDragEnd" @dblclick="returnToHand(i)">
              <InteractiveCard :image-src="srcOf(c)" :size-mode="'fixed'" :width="'160px'" :aspect-ratio="'3/5'" :enable-hover-effect="true" :enable-animation="false" :enable-silver-outline="false" :enable-gif="false" :enable-laser="false" :enable-diagonal-light="false" />
              <span class="label">{{ c }}</span>
            </div>
          </div>
      </div>

      <div class="actions top-actions">
        <button class="btn" :disabled="searched" @click="openPicker">从牌库找牌（仅一次）</button>
        <button class="btn ghost" @click="reset">重置</button>
      </div>

      <div class="hand">
        <div class="hand-title"> </div>
                  <div class="cards" @dragover.prevent @drop="onDropToHand">
            <div v-for="(c,i) in hand" :key="c+'-'+i" class="card" :style="arcStyle(i, hand.length)" draggable="true" @dragstart="onDragStart(c,i)" @dragend="onDragEnd" @click="play(c,i)">
              <InteractiveCard :image-src="srcOf(c)" :size-mode="'fixed'" :width="'160px'" :aspect-ratio="'3/5'" :enable-hover-effect="true" :enable-animation="false" :enable-silver-outline="false" :enable-gif="false" :enable-laser="false" :enable-diagonal-light="false" />
              <span class="label">{{ c }}</span>
            </div>
          </div>
      </div>
    </div>

    <!-- 选牌弹窗 -->
    <teleport to="body">
      <div v-if="picker.show" class="picker-drawer" @click.self="picker.show=false">
              <div class="picker-panel" style="width:420px">
          <button class="picker-x" @click="picker.show=false">×</button>
          <div class="picker-title">从牌库选择 1 张卡加入手牌</div>
        <div class="picker-grid two">
          <div v-for="it in picker.items.filter(x=>!x.stolen)" :key="it.name" class="picker-item" @click="chooseCard(it)">
            <InteractiveCard :image-src="it.url" :size-mode="'fixed'" :width="'160px'" :aspect-ratio="'3/5'" :enable-hover-effect="true" :enable-animation="false" :enable-silver-outline="false" :enable-gif="false" :enable-laser="false" :enable-diagonal-light="false" />
            <div class="nm">{{ it.name }}</div>
          </div>
        </div>
          <button class="picker-close" @click="picker.show=false">关闭</button>
        </div>
      </div>
    </teleport>

    <div v-if="boss.show" class="boss" :style="{ backgroundImage:`url('${bossUrl}')` }">
      <div class="boss-say">这张牌就归我啦！</div>
  <img v-if="bossCarry && bossCarryUrl" class="boss-carry" :src="bossCarryUrl" alt="ATP" />
</div>

    <div v-if="win" class="win">
      <div class="box">
        <h2>通关成功</h2>
        <p>恭喜获得 ATP，并保留 CO₂ 与 H₂O ！</p>
        <button class="btn" @click="toBoss">进入20关</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import InteractiveCard from '@/components/InteractiveCard.vue'

const router = useRouter()

const hand = ref([])
const board = ref([])
const searched = ref(false)
const win = ref(false)

// 拖拽状态
const dragging = ref(false)
let dragItem = { name: '', index: -1 }

const bgUrl = ref('')
const bossUrl = ref('')
const bossCarryUrl = ref('')
const bossCarry = ref(false)

const ctxDecks = (()=>{ try { return require.context('@/assets/img/Decks', true, /\.(png|jpe?g|svg)$/) } catch(e){ return null } })()
const ctxAll = (()=>{ try { return require.context('@/assets/img/all-decks', true, /\.(png|jpe?g|svg)$/) } catch(e){ return null } })()

const nameKeywords = {
  'CO₂': ['二氧化碳', 'CO2'],
  'H₂O': ['水', 'H2O'],
  'O₂': ['氧气', 'O2'],
  '光能': ['光能'],
  '葡萄糖': ['葡萄糖', 'Glucose'],
  'ATP': ['ATP']
}

function findInContext(ctx, keywords){
  if (!ctx) return ''
  const keys = ctx.keys()
  for (const kw of keywords){
    const k = keys.find(x => x.includes(kw) && !x.includes('/backside/') && !/background\.png$/i.test(x))
    if (k) { try { return ctx(k) } catch (e) { /* ignore */ } }
  }
  return ''
}

function srcOf(name){
  const kws = nameKeywords[name] || [name]
  let url = findInContext(ctxDecks, kws)
  if (!url) url = findInContext(ctxAll, kws)
  if (!url){
    try { const ph = require('@/assets/img/Logo.png'); url = (ph && (ph.default||ph)) } catch { url = '' }
  }
  return typeof url === 'string' ? url : String(url)
}

onMounted(()=>{
  // background（取消回退，仅使用 game-background.png）
  try { const b = require('@/assets/img/game/game-background.png'); bgUrl.value = (b.default||b) } catch { bgUrl.value = '' }
  // 初始化手牌
  hand.value = ['CO₂','H₂O']
  // 清除19关完成标记
  try { localStorage.removeItem('level5-19-complete'); localStorage.setItem('force-level5-19-reset','1') } catch(e){}
  // boss image
    try { const x = require('@/assets/img/game/boss.png'); bossUrl.value = (x.default||x) } catch {
     bossUrl.value = 'data:image/svg+xml;utf8,%3Csvg xmlns%3D%22http%3A//www.w3.org/2000/svg%22 width%3D%22120%22 height%3D%22120%22%3E%3Ccircle cx%3D%2260%22 cy%3D%2260%22 r%3D%2250%22 fill%3D%22%237b1fa2%22/%3E%3C/svg%3E'
   }
   try { const c = require('@/assets/img/all-decks/ATP.png'); bossCarryUrl.value = (c.default||c) } catch(e){ bossCarryUrl.value = '' }
})

const boss = ref({ show:false })

const picker = ref({ show:false, items:[] })

function openPicker(){
  if (searched.value) return
  // 构造 8 张卡：必须包含 光能 与 ATP，其余从 Decks 随机补足
  const need = ['光能','ATP']
  const pool = []
  for (const n of need){ pool.push({ name:n, url: srcOf(n), stolen:false }) }
  // 收集其他图片键
  const extra = []
  try {
    const keys = ctxDecks ? ctxDecks.keys() : []
    for (const k of keys){
      if (/光能|ATP/.test(k)) continue
      if (k.includes('/backside/')) continue
      if (/background\.png$/i.test(k)) continue
      extra.push(k)
    }
  } catch (e) { void e }
  // 随机挑 6 张
  for (let i=0;i<6 && extra.length;i++){
    const idx = Math.floor(Math.random() * extra.length)
    const k = extra.splice(idx,1)[0]
    try { const u = ctxDecks(k); pool.push({ name: k.replace(/.*\/(.*)\..*/, '$1'), url: (u && (u.default||u)), stolen:false }) } catch (e) { void e }
  }
  // 截断为 8 张
  picker.value.items = pool.slice(0,8)
  picker.value.show = true
  // 不自动偷走；等待用户点击 ATP 时再触发 BOSS 叼走
}

function chooseCard(item){
  if (!picker.value.show) return
  if (item.stolen) return
  // 点击 ATP 触发 BOSS 叼走：立即从列表移除，并让 BOSS 携带图片
  if (item.name === 'ATP'){
    item.stolen = true
    picker.value.items = picker.value.items.filter(x => !x.stolen)
    if (bossCarryUrl.value) bossCarry.value = true
    triggerBoss()
    return
  }
  hand.value.push(item.name)
  picker.value.show = false
  searched.value = true
}

function play(card, index){
  hand.value.splice(index,1)
  board.value.push(card)
  resolveBoard()
}

function onDragStart(card, index){
  dragging.value = true
  dragItem = { from: 'hand', name: card, index }
}
function onDragStartFromBoard(card, index){
  dragging.value = true
  dragItem = { from: 'board', name: card, index }
}
function onDragEnd(){
  dragging.value = false
  dragItem = { from: '', name: '', index: -1 }
}
function dropToPlay(){
  if (!dragging.value) return
  const { from, name, index } = dragItem
  if (index < 0 || from !== 'hand') return
  hand.value.splice(index,1)
  board.value.push(name)
  onDragEnd()
  resolveBoard()
}
function onDropToHand(){
  if (!dragging.value) return
  const { from, name, index } = dragItem
  if (index < 0 || from !== 'board') return
  board.value.splice(index,1)
  hand.value.push(name)
  onDragEnd()
}

function resolveBoard(){
  const have = new Set(board.value)
  if (have.has('光能') && have.has('CO₂') && have.has('H₂O')){
    board.value = []
    hand.value.push('葡萄糖','O₂')
    return
  }
  if (have.has('葡萄糖') && have.has('O₂')){
    board.value = []
    hand.value.push('ATP','CO₂','H₂O')
    checkWin()
  }
}

// 手牌圆弧布局：根据索引计算角度与下沉
function arcStyle(index, total){
  if (!total) return {}
  const mid = (total - 1) / 2
  const d = index - mid
  const angle = d * 6   // 单位角度（越大越弯）
  const drop = Math.abs(d) * 10 + 12 // 下沉像素（中间最低）
  return { transform: `translateY(${drop}px) rotate(${angle}deg) scale(var(--hoverScale, 1))` }
}

function checkWin(){
  const s = new Set(hand.value)
  if (s.has('ATP') && s.has('CO₂') && s.has('H₂O')){
    win.value = true
    try { localStorage.setItem('level5-19-complete','1') } catch (e) { void e }
  }
}

function toBoss(){
  router.push('/StudentSide/levelt/level5-20')
}

function reset(){
  hand.value = ['CO₂','H₂O']
  board.value = []
  searched.value = false
  win.value = false
  picker.value = { show:false, items:[] }
  boss.value.show = false
}

function triggerBoss(){
  boss.value.show = true
  // 仅播放叼走动画，不跳转；动画结束后隐藏
  setTimeout(()=>{ boss.value.show = false }, 2800)
}
</script>

<style scoped>
.lv519{
  min-height: calc(100vh - 75px);
  background: #eef5ef center / cover no-repeat;
  background-image: var(--bg); /* fallback */
  position: relative;
}
.lv519::before{
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.55);
}
.overlay{
  position: relative;
  z-index: 1;
  padding: 8px 24px 160px;
  display: grid;
  gap: 12px;
  min-height: calc(100vh - 170px);
}
.title{ font-size: 22px; font-weight: 900; color: #17543d; margin-top: 6px; }
.rule.goal{ position: fixed; top: 46px; left: 0; right: 0; z-index: 3; display: flex; justify-content: center; }
.rule.goal::after{ content: attr(data-text); }
.rule{ color: #14532d; font-size: 18px; font-weight: 900; text-align: center; background: rgba(255,255,255,.9); border: 2px solid #a7f3d0; padding: 8px 12px; border-radius: 12px; margin: 0 auto; width: fit-content; box-shadow: 0 8px 20px rgba(16,185,129,.18); }

.zones{
  display: grid;
  gap: 18px;
  max-width: 1280px;
  margin: -120px auto -40px;
}
.play-zone{ position: relative; bottom: 40%;min-height: 360px; min-width: 960px; display: flex; flex-wrap: wrap; align-items: center; justify-content: center; padding: 20px; border-radius: 16px; background: transparent; box-shadow: none; }
.cards{ display: flex; gap: 100px; flex-wrap: wrap; align-items: center; min-height: 122px; padding: 16px; border-radius: 12px; transition: box-shadow .18s ease, background-color .18s ease; }
.cards.droppable{ background: rgba(34,197,94,.08); box-shadow: inset 0 0 0 2px rgba(34,197,94,.35); }

.hand{ position: fixed; left: 0; right: 0; bottom: 0; background: transparent; padding: 0 18px 14px; border-top-left-radius: 16px; border-top-right-radius: 16px; backdrop-filter: none; box-shadow: none; z-index: 6; }
.hand-title{ font-weight: 800; color:#0f172a; margin-bottom: 6px; text-align: center; }
.hand .cards{ gap: 22px; min-height: 140px; align-items: flex-end; justify-content: center; position: relative; padding-top: 24px; }
/* 圆弧形摆放：使用极坐标映射到底部弧线 */
.hand .card{ position: relative; transform-origin: center bottom; transition: transform .18s ease, filter .18s ease; }
.hand .card:nth-child(n){ transform: translateY(calc(var(--arcY, 0px))) rotate(calc(var(--arcR, 0deg))) scale(var(--hoverScale,1)); }
.hand .card:hover{ --hoverScale: 1.18; filter: drop-shadow(0 10px 24px rgba(0,0,0,.22)); }

.card{ width: 120px; display: grid; justify-items: center; gap: 6px; cursor: grab; }
.card:active{ cursor: grabbing; }
.card.small{ width: 92px; cursor: default; }
.card img{ width: auto; height: auto; max-width: 180px; max-height: 140px; object-fit: contain; background: transparent; border-radius: 10px; box-shadow: 0 8px 18px rgba(0,0,0,.16); }
.card .label{ font-size: 20px; font-weight: 800; color:#0f172a; text-shadow: 0 1px 0 rgba(255,255,255,.6); }

.actions{ display:flex; gap: 10px; }
.top-actions{ position: fixed; left: 20%; transform: translateX(-50%); bottom: 28%; z-index: 7; }
.btn{ height: 34px; padding: 0 14px; border: none; border-radius: 8px; background: linear-gradient(135deg,#22c55e,#16a34a); color:#fff; font-weight: 800; cursor:pointer; box-shadow: 0 10px 22px rgba(16,185,129,.28); }
.btn:disabled{ opacity:.5; cursor:not-allowed; }
.btn.ghost{ background: #e5e7eb; color:#111827; box-shadow:none; }

.boss{
  position: fixed;
  top: 16%;
  left: -160px;
  width: 168px;
  height: 168px;
  background: center/contain no-repeat;
  z-index: 10;
  animation: fly 2.8s linear forwards;
  filter: drop-shadow(0 14px 26px rgba(0,0,0,.35));
}
.boss .boss-say{
  position: absolute;
  left: -10px;
  top: -36px;
  background: rgba(146, 21, 255, 0.96);
  color:#9f0000;
  border:2px solid #353535;
  border-radius: 10px;
  padding: 6px 10px;
  font-size: 20px;
  font-weight: 900;
  white-space: nowrap;
  box-shadow: 0 8px 22px rgba(16,185,129,.25);
  animation: sayFade 1.7s ease-out forwards;
}
.boss .boss-carry{
  position: absolute; bottom: -54px; left: 56%; transform: translateX(-50%) rotate(8deg) scale(.7);
  width: 92px; height: auto; object-fit: contain; filter: drop-shadow(0 8px 16px rgba(0,0,0,.25));
}
@keyframes fly{
  0%{ transform: translateX(0) translateY(0) rotate(-10deg); }
  75%{ transform: translateX(45vw) translateY(-12px) rotate(8deg); }
  90%{ transform: translateX(88vw) translateY(20px) rotate(6deg); }
  100%{ transform: translateX(105vw) translateY(-10px) rotate(0deg); }
}
@keyframes sayFade{
  0%   { opacity: 0; transform: translate(-6px,-6px) scale(.96); }
  15%  { opacity: 1; }
  100% { opacity: 0; transform: translate(-10px,-10px) scale(1); }
}
.win{ position: fixed; inset:0; display:grid; place-items:center; background: rgba(0,0,0,.45); z-index: 20; }
.box{ width: min(420px, 90vw); background:#fff; padding: 22px 20px; border-radius: 14px; text-align: center; box-shadow: 0 20px 44px rgba(0,0,0,.25); }
.box h2{ font-size: 20px; font-weight: 900; color:#065f46; margin-bottom: 8px; }
.box p{ color:#111827; margin-bottom: 12px; }

/* 右侧抽屉：固定在导航栏下方，右侧对齐 */
.picker-drawer{
  position: fixed;
  inset: 75px 0 0 0;      /* 顶部预留 75px 导航高度 */
  z-index: 60;
  display: flex;
  justify-content: flex-end;
  background: transparent; /* 需要半透明遮罩可改为 rgba(0,0,0,.2) */
}
/* 隐藏全局底部导航（请按实际类名调整） */
:global(.bottom-nav),
:global(.footer-nav){ display: none !important; }

/* 抽屉面板：固定宽度 420px，满高滚动 */
.picker-panel{
  width: 420px;
  height: calc(100vh - 75px);
  background: rgba(255,255,255,.96);
  border-left: 2px solid #c7e9c0;
  box-shadow: -14px 0 36px rgba(0,0,0,.18);
  padding: 12px 12px 16px 12px;
  overflow: auto;
  backdrop-filter: blur(2px);
  position: relative;
}
.picker-x{
  position: absolute; top: 8px; right: 10px; width: 28px; height: 28px; border-radius: 50%; border: none;
  background: rgba(0,0,0,.08); color: #111; font-size: 18px; cursor: pointer; line-height: 28px;
}
.picker-x:hover{ background: rgba(0,0,0,.12); }

/* 两列网格 */
.picker-grid.two{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

/* 抽屉内卡片图片：最大 160×120，自适应本身比例 */
.picker-img{
  width: auto;
  height: auto;
  max-width: 160px;
  max-height: 120px;
  object-fit: contain;
  display: block;
  margin: 0 auto;
}
</style>
