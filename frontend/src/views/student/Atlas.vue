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
              :gif-src="getGifSrc(deck)"
              :size-mode="'responsive'"
              :width="'100%'"
              :aspect-ratio="'3/5'"
              :border-radius="'16px'"
              :max-tilt="getMaxTilt(deck)"
              :range-scale="getRangeScale(deck)"
              :hover-scale="getHoverScale(deck)"
              :enable-hover-effect="true"
              :enable-animation="true"
              :enable-silver-outline="getSilverOutline(deck)"
              :enable-gif="getEnableGif(deck)"
              :enable-diagonal-light="getEnableDiagonalLight(deck)"
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
        <button class="back" @click="view='shelf'">← 返回</button>
        <div class="title">
          <span>{{ activeDeck?.name }}</span>
        </div>
      </div>
      <div class="cards-grid">
        <div v-for="card in cards" :key="card.id" class="card" :class="{ locked: !card.unlocked, flipped: card.isFlipped }" @click="flipCard(card)">
          <div class="card-inner">
            <!-- 卡片正面 -->
            <div class="card-front">
              <InteractiveCard
                :image-src="card.cover || ''"
                :gif-src="getGifSrc(card)"
                :alt-text="card.name"
                :size-mode="'fixed'"
                :width="'180px'"
                :aspect-ratio="'3/5'"
                :border-radius="'16px'"
                :max-tilt="getMaxTilt(card)"
                :range-scale="getRangeScale(card)"
                :hover-scale="getHoverScale(card)"
                :enable-hover-effect="true"
                :enable-animation="true"
                :enable-silver-outline="getSilverOutline(card)"
                :enable-gif="getEnableGif(card)"
                :enable-diagonal-light="getEnableDiagonalLight(card)"
              >
              </InteractiveCard>
                          <!-- 卡片正面覆盖层 - 只在已解锁时显示 -->
            <div v-if="card.unlocked" class="card-front-overlay">
              <div class="card-name"> </div>
              <div class="flip-hint"> </div>
            </div>
            
            <!-- 未解锁卡片的锁定覆盖层 -->
            <div v-if="!card.unlocked" class="card-lock-overlay">
              <div class="lock-icon">🔒</div>
              <div class="lock-text">未解锁</div>
              <div class="lock-subtitle">获取后解锁</div>
            </div>
            

            </div>
            
            <!-- 卡片背面 -->
            <div class="card-back">
              <div class="card-back-content">
                <div class="card-back-title">{{ card.name }}</div>
                <div class="card-back-description">{{ card.description }}</div>
                <div class="flip-hint">点击翻转回正面</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import InteractiveCard from '@/components/InteractiveCard.vue'
import sparklesGif from '@/assets/gif/sparkles.gif'
import { getUserCards, getAllCards } from '@/api/cards.js'

const view = ref('shelf')
const shelfRef = ref(null)
const q = ref('')
const activeDeck = ref(null)
const cards = ref([])

// 用户卡片数据
const userCards = ref([])
const allCards = ref([])
const loading = ref(false)

// 获取用户卡片数据
const fetchUserCards = async () => {
  try {
    loading.value = true
    const [userCardsRes, allCardsRes] = await Promise.all([
      getUserCards(),
      getAllCards()
    ])
    
    userCards.value = userCardsRes.data.data.cards || []
    allCards.value = allCardsRes.data.data.cards || []
    
    // 更新deckData中的卡片解锁状态
    updateCardUnlockStatus()
  } catch (error) {
    console.error('获取卡片数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 更新卡片解锁状态
const updateCardUnlockStatus = () => {
  const userCardIds = new Set(userCards.value.map(card => card.card_id))
  
  deckData.forEach(deck => {
    deck.cards.forEach(card => {
      // 检查用户是否拥有此卡片
      card.isUnlocked = userCardIds.has(card.id)
      card.isFlipped = false
    })
  })
}



// 通用特效函数 - 根据等级ID获取特效参数
const getGifSrc = (item) => {
  // 判断是否为SR、UR等级
  const isSRUR = (typeof item.id === 'number' && (item.id === 4 || item.id === 5)) || 
                 (typeof item.id === 'string' && (item.id.startsWith('SR') || item.id.startsWith('UR')))
  return isSRUR ? sparklesGif : ''
}

const getMaxTilt = (item) => {
  // 判断等级
  const isB = (typeof item.id === 'number' && item.id === 1) || 
              (typeof item.id === 'string' && item.id.startsWith('B'))
  const isAR = (typeof item.id === 'number' && (item.id === 2 || item.id === 3)) || 
               (typeof item.id === 'string' && (item.id.startsWith('A') || item.id.startsWith('R')))
  const isSRUR = (typeof item.id === 'number' && (item.id === 4 || item.id === 5)) || 
                 (typeof item.id === 'string' && (item.id.startsWith('SR') || item.id.startsWith('UR')))
  
  if (isB) return 6      // B级：基础3D效果
  if (isAR) return 10    // A、R级：增强3D效果
  if (isSRUR) return 15  // SR、UR级：最强3D效果
  return 6
}

const getRangeScale = (item) => {
  const isB = (typeof item.id === 'number' && item.id === 1) || 
              (typeof item.id === 'string' && item.id.startsWith('B'))
  const isAR = (typeof item.id === 'number' && (item.id === 2 || item.id === 3)) || 
               (typeof item.id === 'string' && (item.id.startsWith('A') || item.id.startsWith('R')))
  const isSRUR = (typeof item.id === 'number' && (item.id === 4 || item.id === 5)) || 
                 (typeof item.id === 'string' && (item.id.startsWith('SR') || item.id.startsWith('UR')))
  
  if (isB) return 1.0    // B级：基础缩放
  if (isAR) return 1.3   // A、R级：中等缩放
  if (isSRUR) return 1.6 // SR、UR级：最大缩放
  return 1.0
}

const getHoverScale = (item) => {
  const isB = (typeof item.id === 'number' && item.id === 1) || 
              (typeof item.id === 'string' && item.id.startsWith('B'))
  const isAR = (typeof item.id === 'number' && (item.id === 2 || item.id === 3)) || 
               (typeof item.id === 'string' && (item.id.startsWith('A') || item.id.startsWith('R')))
  const isSRUR = (typeof item.id === 'number' && (item.id === 4 || item.id === 5)) || 
                 (typeof item.id === 'string' && (item.id.startsWith('SR') || item.id.startsWith('UR')))
  
  if (isB) return 1.02   // B级：基础悬浮缩放
  if (isAR) return 1.04  // A、R级：中等悬浮缩放
  if (isSRUR) return 1.06 // SR、UR级：最大悬浮缩放
  return 1.02
}

const getSilverOutline = (item) => {
  const isSRUR = (typeof item.id === 'number' && (item.id === 4 || item.id === 5)) || 
                 (typeof item.id === 'string' && (item.id.startsWith('SR') || item.id.startsWith('UR')))
  return isSRUR
}

const getEnableGif = (item) => {
  const isSRUR = (typeof item.id === 'number' && (item.id === 4 || item.id === 5)) || 
                 (typeof item.id === 'string' && (item.id.startsWith('SR') || item.id.startsWith('UR')))
  return isSRUR
}

const getEnableDiagonalLight = (item) => {
  const isB = (typeof item.id === 'number' && item.id === 1) || 
              (typeof item.id === 'string' && item.id.startsWith('B'))
  // B级卡不启用斜向光
  const result = !isB
  console.log(`斜向光控制 - ID: ${item.id}, 类型: ${typeof item.id}, 是否B级: ${isB}, 启用斜向光: ${result}`)
  return result
}

// 使用本地 src/assets/img/Decks/backside 下的图片作为封面
const deckCtx = require.context('../../assets/img/Decks/backside', false, /\.(png|jpe?g|webp)$/)

// 定义卡组数据，按B、A、R、SR、UR顺序排列
const deckData = [
  {
    id: 1,
    name: 'B级',
    emoji: '', // B级 - #9BA0A3
    cover: deckCtx('./B卡.png'),
    cards: [
      { id: 'B001', name: '协助扩散', description: '物质在载体蛋白协助下的扩散', image: require('../../assets/img/Decks/B卡/协助扩散.png') },
      { id: 'B002', name: '核糖体', description: '蛋白质合成的场所', image: require('../../assets/img/Decks/B卡/核糖体.png') },
      { id: 'B003', name: '种群密度', description: '单位面积内个体的数量', image: require('../../assets/img/Decks/B卡/种群密度.png') },
      { id: 'B004', name: '细胞学说奠基', description: '细胞学说的建立基础', image: require('../../assets/img/Decks/B卡/细胞学说奠基.png') },
      { id: 'B005', name: '水', description: '生命之源', image: require('../../assets/img/Decks/B卡/水.png') },
      { id: 'B006', name: '光能', description: '光合作用的能量来源', image: require('../../assets/img/Decks/B卡/光能.png') }
    ]
  },
  {
    id: 2,
    name: 'A级',
    emoji: '', // A级 - #7FEE77
    cover: deckCtx('./A卡.png'),
    cards: [
      { id: 'A001', name: '主动运输', description: '细胞主动运输物质的过程', image: require('../../assets/img/Decks/A卡/主动运输.png') },
      { id: 'A002', name: '单基因遗传病', description: '由单个基因突变引起的遗传疾病', image: require('../../assets/img/Decks/A卡/单基因遗传病.png') },
      { id: 'A003', name: '叶绿体', description: '植物细胞进行光合作用的场所', image: require('../../assets/img/Decks/A卡/叶绿体.png') },
      { id: 'A004', name: '点突变', description: 'DNA序列中单个碱基的改变', image: require('../../assets/img/Decks/A卡/点突变.png') },
      { id: 'A005', name: '生物催化剂', description: '加速生物化学反应的物质', image: require('../../assets/img/Decks/A卡/生物催化剂.png') },
      { id: 'A006', name: '磷脂双分子层', description: '细胞膜的基本结构', image: require('../../assets/img/Decks/A卡/磷脂双分子层.png') },
      { id: 'A007', name: '程序性死亡', description: '细胞程序性死亡过程', image: require('../../assets/img/Decks/A卡/程序性死亡.png') },
      { id: 'A008', name: '细胞膜', description: '细胞与外界的分界', image: require('../../assets/img/Decks/A卡/细胞膜.png') },
      { id: 'A009', name: '蛋白质', description: '生命活动的主要承担者', image: require('../../assets/img/Decks/A卡/蛋白质.png') },
      { id: 'A010', name: '赤霉素', description: '植物生长调节激素', image: require('../../assets/img/Decks/A卡/赤霉素.png') },
      { id: 'A011', name: '酸碱平衡', description: '维持体内酸碱平衡的机制', image: require('../../assets/img/Decks/A卡/酸碱平衡.png') },
      { id: 'A012', name: '氧气', description: '生命活动必需的气体', image: require('../../assets/img/Decks/A卡/氧气.png') }
    ]
  },
  {
    id: 3,
    name: 'R级',
    emoji: '', // R级 - #40C3FC
    cover: deckCtx('./R卡.png'),
    cards: [
      { id: 'R001', name: '分离定律', description: '孟德尔遗传学第一定律', image: require('../../assets/img/Decks/R卡/分离定律.png') },
      { id: 'R002', name: '反射弧', description: '神经反射的基本结构', image: require('../../assets/img/Decks/R卡/反射弧.png') },
      { id: 'R003', name: '多基因遗传病', description: '由多个基因共同作用的遗传疾病', image: require('../../assets/img/Decks/R卡/多基因遗传病.png') },
      { id: 'R004', name: '无氧呼吸', description: '不需要氧气的呼吸方式', image: require('../../assets/img/Decks/R卡/无氧呼吸.png') },
      { id: 'R005', name: '染色体异常遗传病', description: '由染色体异常引起的遗传疾病', image: require('../../assets/img/Decks/R卡/染色体异常遗传病.png') },
      { id: 'R006', name: '染色体结构变异', description: '染色体结构的改变', image: require('../../assets/img/Decks/R卡/染色体结构变异.png') },
      { id: 'R007', name: '激素调节', description: '激素对生命活动的调节', image: require('../../assets/img/Decks/R卡/激素调节.png') },
      { id: 'R008', name: '生长素', description: '植物生长调节激素', image: require('../../assets/img/Decks/R卡/生长素.png') },
      { id: 'R009', name: '线粒体', description: '细胞的能量工厂', image: require('../../assets/img/Decks/R卡/线粒体.png') },
      { id: 'R010', name: '细胞全能性', description: '细胞发育成完整个体的能力', image: require('../../assets/img/Decks/R卡/细胞全能性.png') },
      { id: 'R011', name: '能量货币', description: '细胞内的能量载体', image: require('../../assets/img/Decks/R卡/能量货币.png') },
      { id: 'R012', name: '食物链', description: '生物之间的食物关系', image: require('../../assets/img/Decks/R卡/食物链.png') },
      { id: 'R013', name: '类囊体膜', description: '叶绿体内进行光反应的膜结构', image: require('../../assets/img/Decks/R卡/类囊体膜.png') },
      { id: 'R014', name: '基质', description: '叶绿体内进行暗反应的场所', image: require('../../assets/img/Decks/R卡/基质.png') },
      { id: 'R015', name: 'NADPH', description: '光合作用中的还原剂', image: require('../../assets/img/Decks/R卡/NADPH.png') }
    ]
  },
  {
    id: 4,
    name: 'SR级',
    emoji: '', // SR级 - #DA34EA
    cover: deckCtx('./SR卡.png'),
    cards: [
      { id: 'SR001', name: '伴X遗传', description: '位于X染色体上的基因遗传', image: require('../../assets/img/Decks/SR卡/伴X遗传.png') },
      { id: 'SR002', name: '光反应', description: '光合作用的光依赖反应', image: require('../../assets/img/Decks/SR卡/光反应.png') },
      { id: 'SR003', name: '半保留复制', description: 'DNA复制的特点', image: require('../../assets/img/Decks/SR卡/半保留复制.png') },
      { id: 'SR004', name: '暗反应', description: '光合作用的碳固定反应', image: require('../../assets/img/Decks/SR卡/暗反应.png') },
      { id: 'SR005', name: '有丝分裂', description: '细胞分裂的主要方式', image: require('../../assets/img/Decks/SR卡/有丝分裂.png') },
      { id: 'SR006', name: '有氧呼吸', description: '需要氧气的呼吸方式', image: require('../../assets/img/Decks/SR卡/有氧呼吸.png') },
      { id: 'SR007', name: '染色体数目变异', description: '染色体数量的改变', image: require('../../assets/img/Decks/SR卡/染色体数目变异.png') },
      { id: 'SR008', name: '现代生物进化理论', description: '现代生物进化的理论体系', image: require('../../assets/img/Decks/SR卡/现代生物进化理论.png') },
      { id: 'SR009', name: '翻译', description: '蛋白质合成的过程', image: require('../../assets/img/Decks/SR卡/翻译.png') },
      { id: 'SR010', name: '自由组合定律', description: '孟德尔遗传学第二定律', image: require('../../assets/img/Decks/SR卡/自由组合定律.png') },
      { id: 'SR011', name: '转录', description: 'DNA到RNA的合成过程', image: require('../../assets/img/Decks/SR卡/转录.png') },
      { id: 'SR012', name: '食物网', description: '复杂的食物关系网络', image: require('../../assets/img/Decks/SR卡/食物网.png') }
    ]
  },
  {
    id: 5,
    name: 'UR级',
    emoji: '', // UR级 - #E9E635
    cover: deckCtx('./UR卡.png'),
    cards: [
      { id: 'UR001', name: '减数分裂', description: '生殖细胞形成时的特殊分裂', image: require('../../assets/img/Decks/UR卡/减数分裂.png') },
      { id: 'UR002', name: '物质循环', description: '生物圈中物质循环过程', image: require('../../assets/img/Decks/UR卡/物质循环.png') },
      { id: 'UR003', name: '生物多样性', description: '地球生物多样性', image: require('../../assets/img/Decks/UR卡/生物多样性.png') },
      { id: 'UR004', name: '能量流动', description: '生态系统能量流动', image: require('../../assets/img/Decks/UR卡/能量流动.png') },
      { id: 'UR005', name: '自然选择', description: '生物进化的主要机制', image: require('../../assets/img/Decks/UR卡/自然选择.png') },
      { id: 'UR006', name: '葡萄糖', description: '细胞的主要能源物质', image: require('../../assets/img/Decks/UR卡/葡萄糖.png') }
    ]
  }
]

const decks = ref(deckData)

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
  
  // 获取用户卡片数据
  fetchUserCards()
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
  // 使用真实的卡牌数据，包含解锁状态
  cards.value = deck.cards.map((card, index) => ({
    id: card.id,
    name: card.name,
    description: card.description, // 添加描述语
    unlocked: card.isUnlocked, // 根据用户拥有状态决定是否解锁
    cover: card.image, // 使用真实的卡牌图片
    isFlipped: false // 初始状态为正面
  }))
  view.value = 'detail'
}

function flipCard(card){
  // 只有已解锁的卡片才能翻转
  if (card.unlocked) {
    card.isFlipped = !card.isFlipped
  }
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
  gap: 16px; 
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
.back{ appearance: none; border: 1px solid rgba(255,255,255,.18); color: #e5e7eb; background: rgba(255,255,255,.06); padding: 6px 5px; border-radius: 10px; cursor: pointer;
  transition: all .18s ease; }
.back:hover{ transform: translateY(-1px); background: rgba(255,255,255,.1); }
.title{ display: inline-flex; gap: 8px; align-items: center; font-weight: 700; color: #f9fafb; }

.cards-grid{ 
  display: grid; 
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); 
  gap: 30px; 
  margin-top: 20px; /* 上方边距，避免遮挡按钮 */
}

/* 卡片翻转样式 */
.card {
  perspective: 1000px;
  cursor: pointer;
  width: 180px; /* 以正面InteractiveCard的宽度为准 */
  height: 300px; /* 确保高度足够，包含InteractiveCard的完整高度 */
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.card.flipped .card-inner {
  transform: rotateY(180deg);
}

.card-front, .card-back {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 16px;
  overflow: visible; /* 改为visible，不裁剪内容 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-back {
  transform: rotateY(180deg);
  background: #ffffff; /* 改为白色背景 */
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000000; /* 改为黑色文字 */
  border: 2px solid #e5e7eb; /* 添加边框 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  height: 100%; /* 确保高度填满容器 */
}

.card-front-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 16px;
  color: white;
  border-radius: 16px;
  pointer-events: none;
  z-index: 10;
}

.card-name {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.8);
}

.flip-hint {
  font-size: 14px;
  opacity: 0.9;
  text-shadow: 0 0px 2px rgba(65, 65, 65, 0.909);
}

.debug-info {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 10px;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(0, 0, 0, 0.5);
  padding: 2px 6px;
  border-radius: 4px;
  pointer-events: none;
}



.card-back-content {
  padding: 20px;
  text-align: center;
  width: 100%;
  max-width: 160px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-back-title {
  font-size: 18px;
  font-weight: 700;
  color: #000000; /* 改为黑色 */
  margin-bottom: 16px;
}

.card-back-description {
  font-size: 14px;
  color: #374151; /* 改为深灰色，提高可读性 */
  line-height: 1.5;
  margin-bottom: 20px;
}

.flip-hint {
  font-size: 12px;
  color: #6b7280; /* 改为中灰色 */
  opacity: 0.9;
}


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

.card.locked .card-cover{ 
  filter: grayscale(70%) brightness(0.6); 
  opacity: 0.7; 
}

/* 未解锁卡片的整体样式 */
.card.locked {
  cursor: not-allowed;
}



/* 未解锁卡片禁用悬浮效果 */
.card.locked .card-front .InteractiveCard {
  transform: none !important;
  transition: none !important;
}

.card.locked:hover {
  transform: none !important;
  box-shadow: none !important;
}

/* 未解锁卡片的锁定覆盖层 */
.card-lock-overlay {
  position: absolute;
  top: 8px;
  left: -2px;
  right: -2px;
  bottom: -14px;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  z-index: 30;
  pointer-events: auto;
  box-shadow: inset 0 0 0 2px rgba(255, 255, 255, 0.2);
}

.lock-icon {
  font-size: 52px;
  margin-bottom: 16px;
  filter: drop-shadow(0 3px 6px rgba(0, 0, 0, 0.6));
  animation: lockPulse 2s ease-in-out infinite;
}

.lock-text {
  font-size: 18px;
  font-weight: 700;
  color: #fbbf24;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9);
  margin-bottom: 6px;
  letter-spacing: 0.5px;
}

.lock-subtitle {
  font-size: 13px;
  color: #d1d5db;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
  opacity: 0.9;
  font-weight: 500;
}

/* 锁定图标脉冲动画 */
@keyframes lockPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}



@media (max-width: 640px){
  .atlas{ padding: 14px; }
  .cards-grid{ 
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); 
    gap: 20px; 
    margin-top: 15px;
  }
  .card{ width: 160px; height: 267px; }
  .card-back-content{ padding: 16px; }
  .card-back-title{ font-size: 16px; margin-bottom: 12px; }
  .card-back-description{ font-size: 12px; margin-bottom: 16px; }
  
  /* 移动端锁定覆盖层样式 */
  .lock-icon {
    font-size: 40px;
    margin-bottom: 12px;
  }
  
  .lock-text {
    font-size: 15px;
    margin-bottom: 4px;
  }
  
  .lock-subtitle {
    font-size: 12px;
  }
  

}
</style>


