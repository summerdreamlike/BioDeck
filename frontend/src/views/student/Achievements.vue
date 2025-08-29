<template>
  <div class="achievements">
    <div class="header">
      <h2>成就系统</h2>
      <div class="stats">
        <div class="stat">
          <span class="stat-num">{{ completedCount }}</span>
          <span class="stat-label">已完成</span>
        </div>
        <div class="stat">
          <span class="stat-num">{{ totalCount }}</span>
          <span class="stat-label">总成就</span>
        </div>
        <div class="stat">
          <span class="stat-num">{{ completionRate }}%</span>
          <span class="stat-label">完成率</span>
        </div>
      </div>
    </div>

    <div class="achievements-grid">
      <div v-for="achievement in achievements" :key="achievement.id" 
           class="achievement" :class="{ completed: achievement.completed, 'just-unlocked': justUnlockedId===achievement.id }">
        <div class="achievement-icon">
          <span class="icon">{{ achievement.icon }}</span>
          <div v-if="achievement.completed" class="completed-badge">✓</div>
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
import { ref, computed } from 'vue'

const achievements = ref([
  {
    id: 1,
    title: '初级收藏家',
    description: '收集10张不同卡牌',
    icon: '📚',
    current: 8,
    target: 10,
    progress: 80,
    completed: false,
    reward: '解锁稀有卡牌'
  },
  {
    id: 2,
    title: '卡组大师',
    description: '完成3个完整卡组',
    icon: '🏆',
    current: 2,
    target: 3,
    progress: 67,
    completed: false,
    reward: '特殊卡组封面'
  },
  {
    id: 3,
    title: '连续登录',
    description: '连续登录7天',
    icon: '🔥',
    current: 5,
    target: 7,
    progress: 71,
    completed: false,
    reward: '每日抽卡次数+1'
  },
  {
    id: 4,
    title: '完美解锁',
    description: '解锁100张卡牌',
    icon: '💎',
    current: 67,
    target: 100,
    progress: 67,
    completed: false,
    reward: '限定头像框'
  },
  {
    id: 5,
    title: '知识探索者',
    description: '完成所有基础关卡',
    icon: '🚀',
    current: 6,
    target: 8,
    progress: 75,
    completed: false,
    reward: '高级卡牌包'
  },
  {
    id: 6,
    title: '收藏达人',
    description: '拥有5张SSR卡牌',
    icon: '⭐',
    current: 3,
    target: 5,
    progress: 60,
    completed: false,
    reward: '专属成就徽章'
  }
])

const completedCount = computed(() => achievements.value.filter(a => a.completed).length)
const totalCount = computed(() => achievements.value.length)
const completionRate = computed(() => Math.round((completedCount.value / totalCount.value) * 100))

// 解锁动画：标记刚解锁的成就ID，触发一次性动画
const justUnlockedId = ref(null)
function unlock(a){
  if (a.completed) return
  a.completed = true
  a.progress = 100
  a.current = a.target
  justUnlockedId.value = a.id
  setTimeout(() => { justUnlockedId.value = null }, 900)
}
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

.progress-text {
  font-size: 12px;
  color: #94a3b8;
  min-width: 40px;
  text-align: right;
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


