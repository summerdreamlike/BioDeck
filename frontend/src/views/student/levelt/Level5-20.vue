<template>
  <div class="page">
    <div class="bg"></div>

    <!-- 顶部信息条 -->
    <div class="topbar">
      <div class="stage">阶段：{{ stageLabel }}</div>
      <div class="energy" title="能量"><span class="energy-label">能量</span> ⚡ {{ energy }}</div>
    </div>

    <!-- 提示/公告 -->
    <transition name="fade">
      <div v-if="tip" class="tip">{{ tip }}</div>
    </transition>

    <!-- 合成光效 -->
    <transition name="zoom">
      <div v-if="showFusionFx" class="fusion-fx"></div>
    </transition>

    <!-- 主区域：仅场面，置中显示 -->
    <div class="board">
      <div class="zone field-zone" :class="{ 'field-drop': isOverField }">
        <div class="zone-title">场面</div>
        <div
          class="cards field"
          @dragenter.prevent="onDragOverField"
          @dragover.prevent="onDragOverField"
          @dragleave="onDragLeaveField"
          @drop="onDropToField"
        >
          <div v-for="(c, i) in field" :key="c.id" class="card placed">
            <img class="card-img" :src="imageOf(c.name)" :alt="c.name" />
            <div class="card-title"><span>{{ c.name }}</span></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部手牌栏 -->
    <div class="hand-dock">
      <div class="hand-title">手牌（仅拖拽到场面）</div>
      <div class="hand-cards">
        <div
          v-for="(c, i) in hand"
          :key="c.id"
          class="card hand"
          :class="{ disabled: !canPlay(c), dragging: draggingId===c.id }"
          draggable="true"
          @dragstart="onDragStart(c, $event)"
          @dragend="onDragEnd"
        >
          <img class="card-img intrinsic" :src="imageOf(c.name)" :alt="c.name" draggable="true" @dragstart.stop="onDragStart(c, $event)" />
          <div class="card-title">
            <span>{{ c.name }}</span>
            <small v-if="costOf(c) !== 0">消耗 {{ Math.abs(costOf(c)) }} 能量</small>
          </div>
        </div>
      </div>
    </div>

    <!-- BOSS 连点 -->
    <transition name="zoom">
      <div v-if="bossMode" class="boss-wrap">
        <div class="boss-hud">
          <div class="timer">{{ bossTimeLeft.toFixed(1) }}s</div>
          <div class="score">积分 +{{ bossScore }}</div>
        </div>
        <img class="boss" :class="{ hit: bossHit }" :src="imgBoss" alt="BOSS" @click="onBossClick($event)" @animationend="bossHit=false" />
        <div class="boss-tip">在 10 秒内连续点击 BOSS，每次 +20 积分！</div>

        <!-- 粒子溅射与飘字 -->
        <div class="fx-layer">
          <div v-for="b in bursts" :key="b.id" class="burst" :style="{ left: b.x+'px', top: b.y+'px' }">
            <i v-for="p in b.particles" :key="p.id" class="p" :style="{ '--tx': p.dx+'px', '--ty': p.dy+'px', '--h': p.h, '--d': p.d+'ms' }"></i>
          </div>
          <div v-for="f in floaters" :key="f.id" class="floater" :style="{ left: f.x+'px', top: f.y+'px' }">+20</div>
        </div>
      </div>
    </transition>

    <!-- 底部操作 -->
    <div class="footer">
      <button class="btn" @click="goBack">返回地图</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { cardApi } from '@/api/index'

const router = useRouter()

// ---------------- 资源加载：按名称直取 game 目录中的具体文件 ----------------
const placeholder = require('@/assets/img/Logo.png')
let imgBoss
try { imgBoss = require('@/assets/img/game/boss.png') } catch (e) { imgBoss = placeholder }

const CARD_IMAGES = {}
function reg(name, rel){
  try { const m = require(`../../assets/img/game/${rel}`); CARD_IMAGES[name] = (m && (m.default || m)) } catch (e) { CARD_IMAGES[name] = placeholder }
}
// 按你的文件名逐个登记
reg('叶绿体', '叶绿体.jpg')
reg('光能', '光能.jpg')
reg('水分子', '水.jpg')
reg('二氧化碳', '二氧化碳.jpg')
reg('Rubisco酶', '酶.jpg')
reg('类囊体膜', '类囊体膜.jpg')
reg('基质', '基质.png')
reg('ATP', 'ATP.png')
reg('NADPH', 'NADPH.png')
// 可能没有对应图的卡（如 氧气、葡萄糖）将回退占位图

function imageOf(name){ return CARD_IMAGES[name] || placeholder }

// ---------------- 基础状态 ----------------
const stage = ref(1) // 1: 搭建场所, 2: 光反应, 3: 暗反应, 4: 结算
const energy = ref(4)
const tip = ref('目标一：搭建光合作用场所')

const hand = ref([]) // { id, name }
const field = ref([])
let uid = 1

function addHand(name){ hand.value.push({ id: uid++, name }) }
function addField(name){ field.value.push({ id: uid++, name }) }
function clearBoard(){ hand.value = []; field.value = [] }

const stageLabel = computed(()=>{
  return stage.value === 1 ? '搭建场所' : stage.value === 2 ? '光反应' : stage.value === 3 ? '暗反应' : '结算'
})

// 费用规则
function costOf(card){
  const n = card.name
  if (stage.value === 1){
    if (n === '叶绿体') return -2
    if (n === '类囊体膜') return -1
    if (n === '基质') return -1
    return 0
  }
  if (stage.value === 2){
    if (n === 'ATP') return -1
    if (n === 'NADPH') return -1
    return 0
  }
  if (stage.value === 3){
    if (n === '二氧化碳') return -5
    return 0
  }
  return 0
}

function canPlay(card){
  const cost = costOf(card)
  return energy.value + cost >= 0
}

// 拖拽交互
const draggingId = ref(null)
const isOverField = ref(false)
function onDragStart(card, e){
  if (!canPlay(card)) return e.preventDefault()
  draggingId.value = card.id
  try { e.dataTransfer.setData('text/plain', String(card.id)) } catch(_){ /* ignore */ }
  e.dataTransfer.effectAllowed = 'move'
}
function onDragEnd(){ draggingId.value = null; isOverField.value = false }
function onDragOverField(e){ isOverField.value = true; try { e.dataTransfer.dropEffect = 'move' } catch(_){ /* ignore */ } }
function onDragLeaveField(){ isOverField.value = false }
function onDropToField(e){
  e.preventDefault()
  isOverField.value = false
  let id
  try {
    const raw = e.dataTransfer.getData('text/plain')
    id = Number(raw)
  } catch(_) {
    id = draggingId.value
  }
  if (!id && draggingId.value) id = draggingId.value
  const card = hand.value.find(c => c.id === id)
  if (card) play(card)
}

// 合成光效
const showFusionFx = ref(false)
function triggerFusionFx(duration = 700){
  showFusionFx.value = true
  setTimeout(()=>{ showFusionFx.value = false }, duration)
}

// ---------------- 阶段流程 ----------------
function enterStage1(){
  stage.value = 1
  tip.value = '目标一：搭建光合作用场所（将卡牌拖拽到场面区）'
  clearBoard()
  ;['叶绿体','水分子','光能','二氧化碳','Rubisco酶'].forEach(addHand)
}

function enterStage2(){
  stage.value = 2
  tip.value = '目标二：完成光反应（本阶段赠与 +3 能量；ATP 产出2，NADPH 产出3）'
  energy.value += 3
  clearBoard()
  ;['水分子','光能'].forEach(addHand)
}

function enterStage3(){
  stage.value = 3
  tip.value = '目标三：暗反应（打出二氧化碳消耗5能量，再打出酶）'
  clearBoard()
  ;['二氧化碳','Rubisco酶'].forEach(addHand)
}

function enterSettle(){
  stage.value = 4
  tip.value = '恭喜完成全部流程！进入BOSS连点挑战'
  clearBoard()
  startBoss()
}

// 出牌主逻辑
function play(card){
  if (!canPlay(card)) return
  const name = card.name
  const cost = costOf(card)
  energy.value += cost
  hand.value = hand.value.filter(c => c.id !== card.id)
  addField(card.name)

  if (stage.value === 1){
    if (name === '叶绿体'){
      if (!hand.value.some(h=>h.name==='类囊体膜')) addHand('类囊体膜')
      if (!hand.value.some(h=>h.name==='基质')) addHand('基质')
    }
    const have = new Set(field.value.map(f=>f.name))
    if (have.has('叶绿体') && have.has('类囊体膜') && have.has('基质')){
      triggerFusionFx()
      setTimeout(()=>{
        clearBoard()
        tip.value = '场所搭建完成，进入光反应'
        enterStage2()
      }, 420)
    }
    return
  }

  if (stage.value === 2){
    const have = new Set(field.value.map(f=>f.name))
    if (have.has('水分子') && have.has('光能')){
      if (!hand.value.some(h=>h.name==='ATP') && !have.has('ATP')) addHand('ATP')
      if (!hand.value.some(h=>h.name==='NADPH') && !have.has('NADPH')) addHand('NADPH')
      if (!field.value.some(f=>f.name==='氧气')) addField('氧气')
      triggerFusionFx()
      tip.value = '已生成 ATP、NADPH 与 氧气。打出 ATP 与 NADPH（各-1 能量）。'
    }

    if (name === 'ATP') energy.value += 2
    if (name === 'NADPH') energy.value += 3

    const okEnergy = energy.value >= 5
    const haveO2 = field.value.some(f=>f.name==='氧气')
    const paidATP = field.value.some(f=>f.name==='ATP')
    const paidNADPH = field.value.some(f=>f.name==='NADPH')
    if (okEnergy && haveO2 && paidATP && paidNADPH){
      setTimeout(()=> enterStage3(), 380)
    }
    return
  }

  if (stage.value === 3){
    const have = new Set(field.value.map(f=>f.name))
    if (have.has('二氧化碳') && (name==='酶' || name==='Rubisco酶' || have.has('Rubisco酶') || have.has('酶'))){
      addField('葡萄糖')
      triggerFusionFx(900)
      setTimeout(()=> enterSettle(), 620)
    }
  }
}

// ---------------- BOSS 连点与积分提交 + 粒子与飘字 ----------------
const bossMode = ref(false)
const bossScore = ref(0)
const bossTimeLeft = ref(10.0)
const bossHit = ref(false)
let bossTimer
let bossTicker

const bursts = ref([]) // {id,x,y,particles:[{id,dx,dy,h,d}]}
const floaters = ref([]) // {id,x,y}

function spawnBurst(x, y){
  const id = 'b' + Math.random().toString(36).slice(2)
  const count = 14
  const particles = Array.from({ length: count }, (_, i) => {
    const angle = (Math.PI * 2 * i) / count + Math.random() * 0.6
    const dist = 40 + Math.random() * 32
    return { id: id + '-' + i, dx: Math.cos(angle) * dist, dy: Math.sin(angle) * dist, h: Math.floor(120 + Math.random()*140), d: 350 + Math.random()*200 }
  })
  bursts.value.push({ id, x, y, particles })
  setTimeout(()=>{ bursts.value = bursts.value.filter(b=>b.id!==id) }, 600)
}

function spawnFloater(x, y){
  const id = 'f' + Math.random().toString(36).slice(2)
  floaters.value.push({ id, x, y })
  setTimeout(()=>{ floaters.value = floaters.value.filter(f=>f.id!==id) }, 800)
}

function startBoss(){
  bossMode.value = true
  bossScore.value = 0
  bossTimeLeft.value = 10.0
  bossTimer && clearTimeout(bossTimer)
  bossTicker && clearInterval(bossTicker)

  const startAt = performance.now()
  bossTicker = setInterval(()=>{
    const elapsed = (performance.now() - startAt) / 1000
    bossTimeLeft.value = Math.max(0, 10 - elapsed)
  }, 50)
  bossTimer = setTimeout(async ()=>{
    clearInterval(bossTicker)
    bossMode.value = false
    tip.value = `挑战结束，本次获得积分 +${bossScore.value}`
    try {
      if (bossScore.value > 0){
        await cardApi.addPoints(bossScore.value)
      }
    } catch (e) { /* 静默失败 */ }
    try { localStorage.setItem('level5-20-complete', '1') } catch(e){ /* ignore */ }
    setTimeout(()=> router.push('/StudentSide/levelt/level5'), 900)
  }, 10000)
}

function onBossClick(e){
  if (!bossMode.value) return
  bossScore.value += 20
  bossHit.value = true
  // 点击坐标 -> 相对窗口定位
  const x = e.clientX
  const y = e.clientY
  spawnBurst(x, y)
  spawnFloater(x, y - 10)
}

function goBack(){ router.push('/StudentSide/levelt/level5') }

onMounted(()=>{ enterStage1() })

onBeforeUnmount(()=>{ clearTimeout(bossTimer); clearInterval(bossTicker) })
</script>

<style scoped>
.page { position: relative; min-height: calc(100vh - 75px); padding: 16px 18px 100px; overflow: hidden; }
.bg { position: absolute; inset: 0; background: url('@/assets/img/game/game-background.png') center / cover no-repeat; filter: saturate(.98) brightness(.98); z-index: 0; }

.topbar { position: relative; z-index: 2; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.stage { font-weight: 900; color: #065f46; background: rgba(255,255,255,.7); padding: 6px 10px; border-radius: 10px; box-shadow: 0 6px 16px rgba(0,0,0,.08); }
.energy { font-weight: 900; color: #0f172a; background: rgba(255,255,255,.9); padding: 6px 12px; border-radius: 999px; box-shadow: 0 8px 20px rgba(0,0,0,.12); display: inline-flex; align-items: center; gap: 6px; }
.energy-label{ color:#065f46; font-weight: 900; }

.tip { position: relative; z-index: 2; margin: 8px 0 12px; background: rgba(255,255,255,.86); border: 2px solid #86efac; color: #14532d; padding: 10px 12px; border-radius: 12px; font-weight: 700; box-shadow: 0 10px 24px rgba(16,185,129,.18); }
.fade-enter-active,.fade-leave-active{ transition: opacity .18s ease; } .fade-enter-from,.fade-leave-to{ opacity: 0; }

/* 合成光效层 */
.fusion-fx { position: fixed; inset: 0; z-index: 20; pointer-events: none; background: radial-gradient(1200px 600px at 50% 60%, rgba(187,247,208,.55), rgba(187,247,208,0) 60%), radial-gradient(800px 400px at 50% 60%, rgba(59,130,246,.25), rgba(59,130,246,0) 60%); animation: fusion .7s ease-out; }
@keyframes fusion { 0%{ opacity: 0; transform: scale(1.02);} 20%{ opacity: 1;} 100%{ opacity: 0; transform: scale(1); } }

/* 置中场面 */
.board { position: relative; z-index: 2; min-height: 56vh; display: grid; place-items: center; }
.zone { background: rgba(255,255,255,.86); border-radius: 14px; padding: 10px; box-shadow: 0 14px 30px rgba(0,0,0,.12); transition: box-shadow .18s ease, transform .18s ease; }
.zone-title { font-weight: 900; color: #0f172a; margin: 0 0 8px; text-shadow: 0 1px 0 rgba(255,255,255,.6); }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; }
.card { background: linear-gradient(135deg, #ffffff, #f3f9f4); border: 2px solid #c7e9c0; border-radius: 12px; overflow: hidden; cursor: pointer; box-shadow: 0 8px 20px rgba(0,0,0,.12); transition: transform .16s ease, box-shadow .16s ease; }
.card:hover { transform: translateY(-4px) scale(1.02); box-shadow: 0 14px 30px rgba(0,0,0,.18); }
.card.disabled { opacity: .6; cursor: not-allowed; filter: grayscale(.1); }
.card.dragging { transform: rotate(-2deg) scale(1.05); box-shadow: 0 16px 40px rgba(0,0,0,.22); }
.card-img { width: 100%; height: 92px; object-fit: cover; display: block; }
.card-img.intrinsic{ width: auto; height: auto; max-height: 100px; max-width: 150px; object-fit: contain; }
.card-title { padding: 6px 8px; display: flex; align-items: baseline; justify-content: space-between; color: #065f46; font-weight: 800; }
.field .card { cursor: default; }
.field .card:hover { transform: none; box-shadow: 0 8px 20px rgba(0,0,0,.12); }
.field-drop { box-shadow: 0 18px 40px rgba(16,185,129,.28), inset 0 0 0 2px rgba(16,185,129,.45); transform: translateY(-2px); }

/* 底部手牌栏 */
.hand-dock{ position: fixed; left: 16px; right: 16px; bottom: 16px; z-index: 4; background: rgba(255,255,255,.92); border: 2px solid #c7e9c0; border-radius: 14px; box-shadow: 0 18px 44px rgba(0,0,0,.22); padding: 8px; }
.hand-title{ font-weight: 900; color: #0f172a; margin: 0 0 6px; }
.hand-cards{ display: flex; gap: 10px; overflow-x: auto; padding-bottom: 4px; }
.card.hand{ background: transparent; border: none; box-shadow: none; }

/* BOSS */
.boss-wrap { position: fixed; inset: 0; z-index: 30; display: grid; place-items: center; background: rgba(0,0,0,.5); backdrop-filter: blur(2px); }
.boss-hud { position: absolute; top: 18px; left: 18px; display: flex; gap: 10px; }
.timer, .score { background: rgba(255,255,255,.96); padding: 6px 10px; border-radius: 10px; font-weight: 900; color: #0f172a; box-shadow: 0 10px 22px rgba(0,0,0,.18); }
.boss { width: min(36vw, 380px); max-width: 440px; height: auto; filter: drop-shadow(0 16px 36px rgba(0,0,0,.38)); animation: float 2s ease-in-out infinite; cursor: pointer; }
.boss.hit { animation: hit .16s ease; }
.boss-tip { position: absolute; bottom: 22px; background: rgba(255,255,255,.96); color: #0f172a; padding: 8px 12px; border-radius: 999px; font-weight: 800; box-shadow: 0 10px 22px rgba(0,0,0,.18); }
@keyframes float { 0%,100%{ transform: translateY(0) } 50%{ transform: translateY(-10px) } }
@keyframes hit { from { transform: scale(.96); } to { transform: scale(1.06); } }
.zoom-enter-active,.zoom-leave-active{ transition: opacity .18s ease; } .zoom-enter-from,.zoom-leave-to{ opacity: 0; }

/* 点击粒子与飘字层 */
.fx-layer { position: fixed; inset: 0; pointer-events: none; }
.burst { position: absolute; width: 0; height: 0; }
.p { position: absolute; left: 0; top: 0; width: 8px; height: 8px; border-radius: 999px; background: hsl(var(--h,150), 90%, 60%); transform: translate(-50%, -50%); animation: shoot var(--d, 420ms) ease-out forwards; box-shadow: 0 2px 8px rgba(0,0,0,.2); }
@keyframes shoot { from { opacity: .95; transform: translate(-50%,-50%) scale(1);} to { opacity: 0; transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(.6);} }

.floater { position: absolute; transform: translate(-50%, -50%); color: #10b981; font-weight: 900; text-shadow: 0 2px 10px rgba(16,185,129,.35); animation: rise .8s ease-out forwards; }
@keyframes rise { from { opacity: 0; transform: translate(-50%, -30%); } 30% { opacity: 1; } to { opacity: 0; transform: translate(-50%, -120%); } }

.footer { margin-top: 14px; display: flex; justify-content: center; position: relative; z-index: 2; }
.btn { height: 36px; padding: 0 16px; border: none; border-radius: 10px; background: linear-gradient(135deg,#10b981,#34d399); color: #fff; font-weight: 800; cursor: pointer; box-shadow: 0 10px 22px rgba(16,185,129,.28); }
</style> 