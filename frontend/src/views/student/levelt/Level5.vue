<template>
  <div class="level-page">
    <!-- 背景图片 -->
    <div class="background-image"></div>
    
    <!-- 暂时隐藏其他元素 -->
    <!--
    <div class="top-nav">
      <div class="nav-left">
        <h1 class="chapter-title">光合作用</h1>
        <span class="chapter-subtitle">Photosynthesis</span>
      </div>
      <div class="nav-right">
        <button class="library-btn" @click="showLibrary = true">
          <i class="library-icon">📚</i>
          <span>生物图书馆</span>
        </button>
      </div>
    </div>

    <div class="levels-container">
      <div class="levels-grid">
        <div class="level-card" v-for="level in levels" :key="level.id" @click="selectLevel(level)">
          <div class="level-number">{{ level.number }}</div>
          <div class="level-content">
            <h3 class="level-title">{{ level.title }}</h3>
            <p class="level-desc">{{ level.description }}</p>
            <div class="level-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: level.progress + '%' }"></div>
              </div>
              <span class="progress-text">{{ level.progress }}%</span>
            </div>
          </div>
          <div class="level-status" :class="level.status">
            <span v-if="level.status === 'completed'">✓</span>
            <span v-else-if="level.status === 'locked'">🔒</span>
            <span v-else>▶</span>
          </div>
        </div>
      </div>
    </div>

    <div class="library-modal" v-if="showLibrary" @click="showLibrary = false">
      <div class="library-content" @click.stop>
        <div class="library-header">
          <h2>📚 生物图书馆</h2>
          <button class="close-btn" @click="showLibrary = false">×</button>
        </div>
        <div class="library-body">
          <div class="ppt-list">
            <div class="ppt-item" v-for="ppt in pptResources" :key="ppt.id" @click="openDocument(ppt)">
              <div class="ppt-icon">📊</div>
              <div class="ppt-info">
                <h3 class="ppt-name">{{ ppt.name }}</h3>
                <p class="ppt-desc">{{ ppt.description }}</p>
                <span class="ppt-size">{{ ppt.size }}</span>
              </div>
              <div class="ppt-action">
                <button class="view-btn">查看</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <DocumentViewer
      v-if="showDocumentViewer"
      :document="currentDocument"
      @close="showDocumentViewer = false"
    />
    -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DocumentViewer from '@/components/DocumentViewer.vue'

const showLibrary = ref(false)
const showPPTViewer = ref(false)
const currentPPT = ref(null)

// 关卡数据
const levels = ref([
  {
    id: 1,
    number: '关卡1',
    title: '光合作用概述',
    description: '了解光合作用的基本概念和重要性',
    progress: 100,
    status: 'completed'
  },
  {
    id: 2,
    number: '关卡2',
    title: '光合色素',
    description: '叶绿素等光合色素的种类和作用',
    progress: 75,
    status: 'in-progress'
  },
  {
    id: 3,
    number: '关卡3',
    title: '光反应阶段',
    description: '光能转化为化学能的过程',
    progress: 50,
    status: 'in-progress'
  },
  {
    id: 4,
    number: '关卡4',
    title: '暗反应阶段',
    description: 'CO2固定和糖类合成过程',
    progress: 0,
    status: 'locked'
  },
  {
    id: 5,
    number: '关卡5',
    title: '光合作用效率',
    description: '影响光合作用效率的因素',
    progress: 0,
    status: 'locked'
  },
  {
    id: 6,
    number: '关卡6',
    title: '实践应用',
    description: '光合作用在农业和环保中的应用',
    progress: 0,
    status: 'locked'
  }
])

// 课件资源
const pptResources = ref([
  {
    id: 1,
    name: '光合作用基础理论.ppt',
    description: '光合作用的基本原理和过程详解',
    size: '2.3MB',
    url: '/src/assets/课件/光合作用/光合作用基础理论.ppt',
    status: 'available'
  },
  {
    id: 2,
    name: '光合色素研究.ppt',
    description: '叶绿素等光合色素的结构和功能',
    size: '1.8MB',
    url: '/src/assets/课件/光合作用/光合色素研究.ppt',
    status: 'available'
  },
  {
    id: 3,
    name: '光反应机制.ppt',
    description: '光反应阶段的详细机制分析',
    size: '3.1MB',
    url: '/src/assets/课件/光合作用/光反应机制.ppt',
    status: 'available'
  },
  {
    id: 4,
    name: '暗反应过程.ppt',
    description: '卡尔文循环和糖类合成过程',
    size: '2.7MB',
    url: '/src/assets/课件/光合作用/暗反应过程.ppt',
    status: 'available'
  },
  {
    id: 5,
    name: '光合作用实验指导.ppt',
    description: '相关实验的操作步骤和注意事项',
    size: '1.5MB',
    url: '/src/assets/课件/光合作用/光合作用实验指导.ppt',
    status: 'available'
  }
])

// 文档查看器相关
const showDocumentViewer = ref(false)
const currentDocument = ref(null)

// 选择关卡
function selectLevel(level) {
  if (level.status === 'locked') {
    alert('该关卡尚未解锁，请先完成前置关卡')
    return
  }
  console.log('选择关卡:', level.number, level.title)
  // 这里可以添加跳转到具体关卡页面的逻辑
}

// 打开文档
function openDocument(doc) {
  currentDocument.value = doc
  showDocumentViewer.value = true
}
</script>

<style scoped>
.level-page {
  min-height: 81vh;
  width: 12000px;
  position: relative;
  overflow-x: auto;
  overflow-y: hidden;
}

/* 背景图片 */
.background-image {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 12000px;
  height: 100vh;
  background-image: url('@/assets/img/levelt/levelt5-background.jpg');
  background-size: auto 100vh;
  background-repeat: repeat-x;
  background-position: 0 0;
  z-index: -1;
}

/* 暂时隐藏其他样式 */
/*
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.nav-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chapter-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
}

.chapter-subtitle {
  font-size: 14px;
  color: #64748b;
  font-style: italic;
}

.library-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.library-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
}

.library-icon {
  font-size: 20px;
}

.levels-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.levels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.level-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: rgba(248, 250, 252, 0.8);
  border: 2px solid rgba(226, 232, 240, 0.8);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.level-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s;
}

.level-card:hover::before {
  left: 100%;
}

.level-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
  border-color: rgba(59, 130, 246, 0.4);
}

.level-number {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border-radius: 50%;
  font-size: 18px;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  flex-shrink: 0;
}

.level-content {
  flex: 1;
  min-width: 0;
}

.level-title {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.level-desc {
  margin: 0 0 16px;
  font-size: 14px;
  color: #64748b;
  line-height: 1.5;
}

.level-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: rgba(15, 23, 42, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #3b82f6);
  border-radius: 4px;
  transition: width 0.6s ease;
}

.progress-text {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
  min-width: 40px;
}

.level-status {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 18px;
  font-weight: bold;
  flex-shrink: 0;
}

.level-status.completed {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.level-status.in-progress {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
}

.level-status.locked {
  background: rgba(100, 116, 139, 0.2);
  color: #64748b;
}

.library-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(8px);
}

.library-content {
  background: white;
  border-radius: 20px;
  width: 95%;
  height: 95%;
  max-width: none;
  max-height: none;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
  display: flex;
  flex-direction: column;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.library-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  flex-shrink: 0;
}

.library-header h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 32px;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background 0.2s ease;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.library-body {
  padding: 30px;
  flex: 1;
  overflow-y: auto;
  background: #f8fafc;
}

.ppt-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.ppt-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.ppt-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
}

.ppt-icon {
  font-size: 32px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.ppt-info {
  flex: 1;
}

.ppt-name {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.ppt-desc {
  margin: 0 0 8px;
  font-size: 14px;
  color: #64748b;
  line-height: 1.5;
}

.ppt-size {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
}

.ppt-action {
  display: flex;
  align-items: center;
}

.view-btn {
  padding: 12px 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.view-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
}

.ppt-viewer-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
  backdrop-filter: blur(8px);
}

.ppt-viewer-content {
  background: white;
  border-radius: 20px;
  width: 95%;
  max-width: 1200px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: modalSlideIn 0.3s ease-out;
}

.ppt-viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.ppt-viewer-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.ppt-viewer-body {
  padding: 24px;
  background: #f8fafc;
}

@media (max-width: 768px) {
  .levels-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .top-nav {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .library-content,
  .ppt-viewer-content {
    width: 95%;
    margin: 20px;
  }
  
  .level-card {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .level-number {
    width: 50px;
    height: 50px;
    font-size: 16px;
  }
  
  .ppt-list {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
*/
</style>


