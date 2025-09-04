<template>
  <div class="daily-checkin-overlay" v-if="visible" @click="handleOverlayClick">
    <div class="daily-checkin-modal" @click.stop>
      <!-- 签到成功动画 -->
      <div v-if="showSuccess" class="success-animation">
        <div class="success-icon">🎉</div>
        <div class="success-title">签到成功！</div>
        <div class="success-subtitle">获得 {{ rewardPoints }} 积分</div>
        <div class="streak-info">
          <span class="streak-label">连续登录</span>
          <span class="streak-days">{{ consecutiveDays }} 天</span>
        </div>
      </div>
      
      <!-- 签到界面 -->
      <div v-else class="checkin-content">
        <div class="modal-header">
          <h2 class="title">每日签到</h2>
          <div class="close-btn" @click="$emit('close')">×</div>
        </div>
        
        <div class="checkin-body">
          <!-- 连续登录天数显示 -->
          <div class="streak-display">
            <div class="streak-icon">🔥</div>
            <div class="streak-text">
              <span class="streak-label">连续登录</span>
              <span class="streak-number">{{ consecutiveDays }}</span>
              <span class="streak-unit">天</span>
            </div>
          </div>
          
          <!-- 签到按钮 -->
          <div class="checkin-button-container">
            <button 
              class="checkin-button" 
              :class="{ 'checking': isChecking, 'checked': hasCheckedToday }"
              @click="performCheckin"
              :disabled="isChecking || hasCheckedToday"
            >
              <span v-if="!hasCheckedToday && !isChecking" class="button-text">
                <span class="icon">📅</span>
                立即签到
              </span>
              <span v-else-if="isChecking" class="button-text">
                <span class="icon">⏳</span>
                签到中...
              </span>
              <span v-else class="button-text">
                <span class="icon">✅</span>
                今日已签到
              </span>
            </button>
          </div>
          
          <!-- 奖励信息 -->
          <div class="reward-info">
            <div class="reward-item">
              <span class="reward-icon">💰</span>
              <span class="reward-text">签到奖励：{{ rewardPoints }} 积分</span>
            </div>
            <div class="reward-item">
              <span class="reward-icon">🎁</span>
              <span class="reward-text">连续登录额外奖励</span>
            </div>
          </div>
          
          <!-- 签到日历 -->
          <div class="checkin-calendar">
            <h4 class="calendar-title">本月签到记录</h4>
            <div class="calendar-grid">
              <div 
                v-for="day in calendarDays" 
                :key="day.date" 
                class="calendar-day"
                :class="{
                  'checked': day.checked,
                  'today': day.isToday,
                  'future': day.isFuture
                }"
              >
                <span class="day-number">{{ day.day }}</span>
                <span v-if="day.checked" class="check-mark">✓</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { dailyCheckinApi } from '@/api/dailyCheckin.js'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'points-earned'])

// 状态变量
const isChecking = ref(false)
const hasCheckedToday = ref(false)
const consecutiveDays = ref(0)
const showSuccess = ref(false)
const rewardPoints = ref(1000)
const calendarDays = ref([])

// 计算属性
const currentMonth = computed(() => {
  const now = new Date()
  return {
    year: now.getFullYear(),
    month: now.getMonth() + 1
  }
})

// 获取签到状态
async function getCheckinStatus() {
  try {
    const response = await dailyCheckinApi.getStatus()
    if (response && response.data) {
      hasCheckedToday.value = response.data.checked_today || false
      consecutiveDays.value = response.data.consecutive_days || 0
      generateCalendarDays()
    }
  } catch (error) {
    console.error('获取签到状态失败:', error)
    // 如果API调用失败，使用默认值
    hasCheckedToday.value = false
    consecutiveDays.value = 0
    generateCalendarDays()
  }
}

// 执行签到
async function performCheckin() {
  if (isChecking.value || hasCheckedToday.value) return
  
  isChecking.value = true
  
  try {
    const response = await dailyCheckinApi.checkin()
    if (response && response.data) {
      // 更新状态
      hasCheckedToday.value = true
      consecutiveDays.value = response.data.consecutive_days || 0
      rewardPoints.value = response.data.points_earned || 1000
      
      // 显示成功动画
      showSuccess.value = true
      
      // 通知父组件积分变化 - 传递完整的积分信息
      emit('points-earned', {
        points: response.data.points_earned || 1000,
        totalPoints: response.data.total_points || 0,
        consecutiveDays: response.data.consecutive_days || 0,
        type: 'daily_checkin'
      })
      
      // 3秒后自动关闭
      setTimeout(() => {
        showSuccess.value = false
        emit('close')
      }, 1000)
      
      ElMessage.success('签到成功！获得 ' + rewardPoints.value + ' 积分')
    }
  } catch (error) {
    console.error('签到失败:', error)
    ElMessage.error('签到失败，请重试')
  } finally {
    isChecking.value = false
  }
}

// 生成日历数据
function generateCalendarDays() {
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth()
  const today = now.getDate()
  
  // 获取当月第一天和最后一天
  const firstDay = new Date(currentYear, currentMonth, 1)
  const lastDay = new Date(currentYear, currentMonth + 1, 0)
  const daysInMonth = lastDay.getDate()
  
  // 获取第一天是星期几
  const firstDayWeekday = firstDay.getDay()
  
  const days = []
  
  // 添加前面的空白天数
  for (let i = 0; i < firstDayWeekday; i++) {
    days.push({ day: '', checked: false, isToday: false, isFuture: false })
  }
  
  // 添加当月天数
  for (let i = 1; i <= daysInMonth; i++) {
    const isToday = i === today
    const isFuture = i > today
    const checked = isToday ? hasCheckedToday.value : false // 简化处理，实际应该从后端获取
    
    days.push({
      day: i,
      checked,
      isToday,
      isFuture
    })
  }
  
  calendarDays.value = days
}

// 处理遮罩层点击
function handleOverlayClick() {
  if (!showSuccess.value) {
    emit('close')
  }
}

// 监听visible变化
watch(() => props.visible, (newVal) => {
  if (newVal) {
    getCheckinStatus()
  }
})

// 组件挂载时获取状态
onMounted(() => {
  if (props.visible) {
    getCheckinStatus()
  }
})
</script>

<style scoped>
.daily-checkin-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.daily-checkin-modal {
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  max-width: 90vw;
  max-height: 90vh;
  width: 480px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 成功动画样式 */
.success-animation {
  padding: 60px 40px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.success-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounce 0.6s ease-in-out;
}

.success-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
}

.success-subtitle {
  font-size: 20px;
  margin-bottom: 24px;
  opacity: 0.9;
}

.streak-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.streak-label {
  font-size: 14px;
  opacity: 0.8;
}

.streak-days {
  font-size: 24px;
  font-weight: 700;
  color: #ffd700;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-20px);
  }
  60% {
    transform: translateY(-10px);
  }
}

/* 签到界面样式 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 20px;
  color: #64748b;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e2e8f0;
  color: #475569;
}

.checkin-body {
  padding: 24px;
}

.streak-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 32px;
  padding: 20px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 0%, #f59e0b 100%);
  border-radius: 16px;
  color: #92400e;
}

.streak-icon {
  font-size: 32px;
}

.streak-text {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.streak-label {
  font-size: 14px;
  opacity: 0.8;
}

.streak-number {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.streak-unit {
  font-size: 14px;
  opacity: 0.8;
}

.checkin-button-container {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.checkin-button {
  padding: 16px 32px;
  border: none;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 160px;
  justify-content: center;
}

.checkin-button:not(.checked):not(.checking) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.checkin-button:not(.checked):not(.checking):hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6);
}

.checkin-button.checking {
  background: #94a3b8;
  color: white;
  cursor: not-allowed;
}

.checkin-button.checked {
  background: #10b981;
  color: white;
  cursor: not-allowed;
}

.button-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon {
  font-size: 20px;
}

.reward-info {
  margin-bottom: 32px;
}

.reward-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #e2e8f0;
}

.reward-item:last-child {
  border-bottom: none;
}

.reward-icon {
  font-size: 20px;
}

.reward-text {
  color: #475569;
  font-size: 14px;
}

.checkin-calendar {
  border-top: 1px solid #e2e8f0;
  padding-top: 24px;
}

.calendar-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  text-align: center;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  position: relative;
  background: #f8fafc;
  color: #64748b;
}

.calendar-day.checked {
  background: #10b981;
  color: white;
}

.calendar-day.today {
  background: #3b82f6;
  color: white;
  font-weight: 700;
}

.calendar-day.future {
  background: #f1f5f9;
  color: #cbd5e1;
}

.check-mark {
  position: absolute;
  top: 2px;
  right: 2px;
  font-size: 10px;
  color: #10b981;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .daily-checkin-modal {
    width: 95vw;
    margin: 20px;
  }
  
  .checkin-body {
    padding: 20px;
  }
  
  .streak-display {
    padding: 16px;
  }
  
  .streak-number {
    font-size: 28px;
  }
}
</style> 