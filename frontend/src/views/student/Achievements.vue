<template>
  <div class="achievements">
    <div class="header">
      <div class="title-section">
        <h2 class="main-title">成就殿堂</h2>
      </div>
      <div class="stats">
        <div class="stat" :class="{ 'stat-completed': completedCount > 0 }">
          <div class="stat-icon">🎯</div>
          <div class="stat-content">
            <span class="stat-num" :data-value="completedCount">{{ completedCount }}</span>
            <span class="stat-label">已完成</span>
          </div>
          <div class="stat-progress-ring">
            <svg viewBox="0 0 36 36">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                    :stroke-dasharray="`${(completedCount / totalCount) * 100}, 100`"/>
            </svg>
          </div>
        </div>
        <div class="stat" :class="{ 'stat-total': totalCount > 0 }">
          <div class="stat-icon">🌟</div>
          <div class="stat-content">
            <span class="stat-num" :data-value="totalCount">{{ totalCount }}</span>
            <span class="stat-label">总成就</span>
          </div>
          <div class="stat-pulse"></div>
        </div>
        <div class="stat" :class="{ 'stat-rate': completionRate > 0 }">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <span class="stat-num" :data-value="completionRate">{{ completionRate }}%</span>
            <span class="stat-label">完成率</span>
          </div>
          <div class="stat-bar" :style="{ width: completionRate + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- 分类筛选器 -->
    <div class="category-filter">
      <div class="filter-tabs">
        <button 
          v-for="category in categories" 
          :key="category.id"
          @click="selectedCategory = category.id"
          class="filter-tab"
          :class="{ active: selectedCategory === category.id }"
        >
          <span class="tab-icon">{{ category.icon }}</span>
          <span class="tab-name">{{ category.name }}</span>
        </button>
      </div>
    </div>

    <div class="achievements-grid">
      <div v-for="achievement in filteredAchievements" :key="achievement.id" 
           class="achievement" :class="{ completed: achievement.completed, 'just-unlocked': justUnlockedId===achievement.id }">
        <div class="achievement-icon">
          <span class="icon">{{ achievement.icon }}</span>
          <div v-if="achievement.completed" class="completed-badge">✓</div>
          <div class="category-tag">{{ achievement.category }}</div>
        </div>
        <div class="achievement-content">
          <div class="achievement-title">{{ achievement.title }}</div>
          <div class="achievement-desc">{{ achievement.description }}</div>
          <div class="achievement-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: achievement.progress + '%' }"></div>
            </div>
            <span class="progress-text">{{ achievement.current }}/{{ achievement.target }}</span>
          </div>
        </div>
        <div class="achievement-reward">
          <span class="reward-icon">🎁</span>
          <span class="reward-text">{{ achievement.reward }}</span>
          <button class="unlock-btn" v-if="!achievement.completed" @click="unlock(achievement)">解锁</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { dailyCheckinApi } from '@/api/dailyCheckin.js'
import { getUserCollectionStats } from '@/api/cards.js'

// 成就分类配置
const categories = ref([
  { id: 'all', name: '全部', icon: '🔄' },
  { id: '收藏', name: '收藏', icon: '📚' },
  { id: '卡组', name: '卡组', icon: '🏆' },
  { id: '日常', name: '日常', icon: '🔥' },
  { id: '解锁', name: '解锁', icon: '💎' },
  { id: '关卡', name: '关卡', icon: '🚀' }
])

  // 成就数据配置
const achievements = ref([
  // 收藏类成就
  {
    id: 1,
    title: '初级收藏家',
    description: '收集10张不同卡牌',
    icon: '📚',
    current: 0,
    target: 10,
    progress: 0,
    completed: false,
    reward: '解锁稀有卡牌',
    category: '收藏',
    apiKey: 'total_cards'
  },
  {
    id: 6,
    title: '收藏达人',
    description: '拥有5张SR卡牌',
    icon: '⭐',
    current: 0,
    target: 5,
    progress: 0,
    completed: false,
    reward: '专属成就徽章',
    category: '收藏',
    apiKey: 'sr_cards'
  },
  {
    id: 9,
    title: '收藏狂人',
    description: '收集50张卡牌',
    icon: '🃏',
    current: 0,
    target: 50,
    progress: 0,
    completed: false,
    reward: '收藏大师',
    category: '收藏',
    apiKey: 'total_cards'
  },
  {
    id: 16,
    title: '传奇收藏家',
    description: '收集所有UR卡牌',
    icon: '🌟',
    current: 0,
    target: 5,
    progress: 0,
    completed: false,
    reward: '传奇之光',
    category: '收藏',
    apiKey: 'ur_cards'
  },
  
  // 卡组类成就
  {
    id: 2,
    title: '卡组大师',
    description: '完成3个完整卡组',
    icon: '🏆',
    current: 0,
    target: 3,
    progress: 0,
    completed: false,
    reward: '特殊卡组封面',
    category: '卡组',
    apiKey: 'complete_decks'
  },
  
  // 日常类成就
  {
    id: 3,
    title: '连续登录',
    description: '连续登录7天',
    icon: '🔥',
    current: 0,
    target: 7,
    progress: 0,
    completed: false,
    reward: '每日抽卡次数+1',
    category: '日常',
    apiKey: 'consecutive_days'
  },
  {
    id: 14,
    title: '时间旅行者',
    description: '连续登录一个月',
    icon: '⏰',
    current: 0,
    target: 30,
    progress: 0,
    completed: false,
    reward: '时间徽章',
    category: '日常',
    apiKey: 'consecutive_days'
  },
  
  // 解锁类成就
  {
    id: 4,
    title: '完美解锁',
    description: '解锁30张卡牌',
    icon: '💎',
    current: 0,
    target: 30,
    progress: 0,
    completed: false,
    reward: '限定头像框',
    category: '解锁',
    apiKey: 'total_cards'
  },
  {
    id: 19,
    title: '解锁专家',
    description: '解锁50张卡牌',
    icon: '🔓',
    current: 0,
    target: 50,
    progress: 0,
    completed: false,
    reward: '解锁大师',
    category: '解锁',
    apiKey: 'total_cards'
  },
  
  // 关卡类成就
  {
    id: 5,
    title: '知识探索者',
    description: '完成所有普通关卡',
    icon: '🚀',
    current: 118,
    target: 154,
    progress: 0,
    completed: false,
    reward: '高级卡牌包',
    category: '关卡'
  },
  {
    id: 8,
    title: '挑战者',
    description: '完成所有BOSS关卡',
    icon: '🔥',
    current: 6,
    target: 8,
    progress: 0,
    completed: false,
    reward: '挑战者称号',
    category: '关卡'
  },
  {
    id: 20,
    title: '关卡征服者',
    description: '完成所有关卡',
    icon: '🏁',
    current: 125,
    target: 160,
    progress: 0,
    completed: false,
    reward: '征服者称号',
    category: '关卡'
  }
])

// 筛选器状态
const selectedCategory = ref('all')
const justUnlockedId = ref(null)

// 计算属性
const filteredAchievements = computed(() => {
  if (selectedCategory.value === 'all') {
    return achievements.value
  }
  return achievements.value.filter(achievement => achievement.category === selectedCategory.value)
})

const completedCount = computed(() => {
  return achievements.value.filter(achievement => achievement.completed).length
})

const totalCount = computed(() => {
  return achievements.value.length
})

const completionRate = computed(() => {
  if (totalCount.value === 0) return 0
  return Math.round((completedCount.value / totalCount.value) * 100)
})

// 从后端获取连续登录天数
async function loadConsecutiveDays() {
  try {
    const response = await dailyCheckinApi.getStatus()
    if (response && response.data) {
      const consecutiveDays = response.data.consecutive_days || 0
      
      // 更新相关成就的数据
      achievements.value.forEach(achievement => {
        if (achievement.apiKey === 'consecutive_days') {
          achievement.current = consecutiveDays
        }
      })
      
      // 计算所有成就进度
      calculateAllProgress()
    }
  } catch (error) {
    console.error('获取连续登录天数失败:', error)
  }
}

// 加载卡片收集数据
async function loadCollectionData() {
  try {
    const response = await getUserCollectionStats()
    
    if (response && response.data && response.data.data) {
      const stats = response.data.data
      
      // 更新相关成就的数据
      achievements.value.forEach(achievement => {
        if (achievement.apiKey) {
          switch (achievement.apiKey) {
            case 'total_cards':
              achievement.current = stats.total_cards || 0
              break
            case 'sr_cards':
              achievement.current = stats.rarity_stats?.SR || 0
              break
            case 'ur_cards':
              achievement.current = stats.rarity_stats?.UR || 0
              break
            case 'complete_decks': {
              // 计算完整卡组数量（每个稀有度至少有一张卡）
              const completeDecks = Object.values(stats.rarity_stats || {}).filter(count => count > 0).length
              achievement.current = completeDecks
              break
            }
          }
        }
      })
      
      // 计算所有成就进度
      calculateAllProgress()
    }
  } catch (error) {
    console.error('获取卡片收集数据失败:', error)
  }
}

// 计算所有成就的进度
function calculateAllProgress() {
  achievements.value.forEach(achievement => {
    if (achievement.current !== undefined && achievement.target !== undefined) {
      achievement.progress = Math.min(Math.round((achievement.current / achievement.target) * 100), 100)
      achievement.completed = achievement.current >= achievement.target
    }
  })
}

// 解锁成就
function unlock(achievement) {
  if (achievement.completed) return
  
  // 这里可以添加解锁逻辑
  console.log('解锁成就:', achievement.title)
  
  // 模拟解锁成功
  achievement.completed = true
  justUnlockedId.value = achievement.id
  
  // 3秒后清除解锁状态
  setTimeout(() => { 
    justUnlockedId.value = null 
  }, 3000)
}

// 组件挂载时加载数据
onMounted(() => {
  loadConsecutiveDays()
  loadCollectionData()
  // 初始化时计算所有成就进度
  calculateAllProgress()
})
</script>

<style scoped>
/* 明亮主题：白色背景 */
.achievements {
  position: relative;
  min-height: 100vh;
  padding: 20px;
  color: #111827;
  background: #ffffff;
}

.header {
  margin-bottom: 24px;
}

.header h2 {
  margin: 0 0 16px;
  font-weight: 700;
  color: #0f172a;
  font-size: 28px;
}

.stats {
  display: flex;
  gap: 24px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 20px;
  background: rgba(15,23,42,.02);
  border: 1px solid rgba(15,23,42,.08);
  border-radius: 16px;
  backdrop-filter: blur(8px);
  transition: transform .18s ease, box-shadow .18s ease;
}

.stat:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0,0,0,.2);
}

.stat-num {
  font-size: 24px;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 分类筛选器 */
.category-filter {
  margin-bottom: 24px;
  padding: 12px 20px;
  background: rgba(15,23,42,.02);
  border: 1px solid rgba(15,23,42,.08);
  border-radius: 16px;
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  gap: 12px;
}

.filter-tabs {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 8px;
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  cursor: pointer;
  transition: all .2s ease;
  font-size: 14px;
  font-weight: 600;
  color: #4b5563;
  white-space: nowrap;
}

.filter-tab:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
}

.filter-tab.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.tab-icon {
  font-size: 18px;
}

.tab-name {
  font-size: 14px;
}

/* 成就网格 */
.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.achievement {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #ffffff;
  border: 1px solid rgba(15,23,42,.08);
  border-radius: 16px;
  backdrop-filter: blur(8px);
  transition: all .22s ease;
  position: relative;
  overflow: hidden;
}

.achievement:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 32px rgba(0,0,0,.12);
  border-color: rgba(15,23,42,.16);
}

.achievement.completed {
  background: linear-gradient(135deg, rgba(16,185,129,.08), rgba(16,185,129,.02));
  border-color: rgba(16,185,129,.25);
}

.achievement-icon {
  position: relative;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(50% 60% at 50% 35%, rgba(59,130,246,.10), rgba(59,130,246,0));
  border-radius: 16px;
  flex-shrink: 0;
}

.icon {
  font-size: 28px;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,.3));
}

.completed-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  background: #10b981;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(16,185,129,.4);
}

.category-tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #f3f4f6;
  color: #4b5563;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid #e5e7eb;
  backdrop-filter: blur(4px);
  z-index: 1;
}

.achievement-content {
  flex: 1;
  min-width: 0;
}

.achievement-title {
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 6px;
  font-size: 16px;
}

.achievement-desc {
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 12px;
  line-height: 1.4;
}

.achievement-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: rgba(15,23,42,.08);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #10b981);
  border-radius: 3px;
  transition: width .6s ease;
}


.achievement-reward {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px;
  background: rgba(15,23,42,.02);
  border-radius: 12px;
  border: 1px solid rgba(15,23,42,.08);
  min-width: 80px;
}

.unlock-btn{ margin-top: 6px; appearance: none; border: 1px solid rgba(59,130,246,.35); background: #fff; color: #1d4ed8; padding: 4px 8px; border-radius: 8px; cursor: pointer; transition: all .18s ease; font-size: 12px; }
.unlock-btn:hover{ background: #eff6ff; transform: translateY(-1px); }

/* 解锁动画：弹出 + 光晕划过 */
.achievement.just-unlocked{ animation: unlockPop .6s cubic-bezier(.2,.9,.25,1.2) both; }
.achievement.just-unlocked::after{
  content: ""; position: absolute; inset: -20%; background: radial-gradient(circle at 20% 20%, rgba(255,255,255,.8), rgba(255,255,255,0));
  animation: shine .8s ease forwards;
}
@keyframes unlockPop{ 0%{ transform: scale(.96); box-shadow: 0 0 0 rgba(0,0,0,0); } 60%{ transform: scale(1.02); } 100%{ transform: scale(1); box-shadow: 0 16px 32px rgba(0,0,0,.12); } }
@keyframes shine{ 0%{ transform: translateX(-60%) translateY(-60%) rotate(0deg); opacity: .9; } 100%{ transform: translateX(120%) translateY(120%) rotate(20deg); opacity: 0; } }

.reward-icon {
  font-size: 20px;
}

.reward-text {
  font-size: 11px;
  color: #94a3b8;
  text-align: center;
  line-height: 1.2;
}

/* 响应式 */
@media (max-width: 768px) {
  .achievements {
    padding: 16px;
  }
  
  .stats {
    gap: 16px;
  }
  
  .stat {
    padding: 12px 16px;
  }

  .category-filter {
    padding: 8px 12px;
    gap: 8px;
  }

  .filter-tab {
    padding: 6px 12px;
    font-size: 12px;
  }

  .tab-icon {
    font-size: 16px;
  }

  .tab-name {
    font-size: 12px;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .achievement {
    padding: 16px;
    gap: 12px;
  }
}
</style>


