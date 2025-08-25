<template>
  <div class="biology-container">
    <div class="header">
      <h1>🔬 生物实验中心</h1>
      <p>探索生物学的奥秘，了解生命科学的基础知识</p>
    </div>
    
    <div class="content">
      <div class="experiment-grid">
        <div class="experiment-card" v-for="experiment in experiments" :key="experiment.id">
          <div class="experiment-icon">{{ experiment.icon }}</div>
          <h3>{{ experiment.title }}</h3>
          <p>{{ experiment.description }}</p>
          <div class="experiment-topics">
            <span v-for="topic in experiment.topics" :key="topic" class="topic-tag">
              {{ topic }}
            </span>
          </div>
          <button class="start-btn" @click="startExperiment(experiment)">
            开始实验
          </button>
        </div>
      </div>
      
      <div class="biology-concepts">
        <h2>🧬 核心概念</h2>
        <div class="concepts-grid">
          <div class="concept-card" v-for="concept in concepts" :key="concept.id">
            <h4>{{ concept.title }}</h4>
            <p>{{ concept.description }}</p>
            <ul>
              <li v-for="point in concept.points" :key="point">{{ point }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const experiments = ref([
  {
    id: 1,
    icon: '🔬',
    title: '显微镜观察',
    description: '使用显微镜观察细胞结构，了解细胞的基本组成',
    topics: ['细胞生物学', '显微镜技术', '细胞结构']
  },
  {
    id: 2,
    icon: '🧬',
    title: 'DNA提取',
    description: '从植物或动物组织中提取DNA，了解遗传物质',
    topics: ['遗传学', '分子生物学', 'DNA结构']
  },
  {
    id: 3,
    icon: '🌱',
    title: '光合作用实验',
    description: '观察植物光合作用过程，了解能量转换',
    topics: ['植物生理学', '光合作用', '能量代谢']
  },
  {
    id: 4,
    icon: '🦠',
    title: '微生物培养',
    description: '培养和观察微生物，了解微生物世界',
    topics: ['微生物学', '无菌技术', '微生物分类']
  },
  {
    id: 5,
    icon: '🧪',
    title: '酶活性实验',
    description: '研究酶的催化作用，了解生物催化剂',
    topics: ['生物化学', '酶学', '催化作用']
  },
  {
    id: 6,
    icon: '🩸',
    title: '血型鉴定',
    description: '进行血型鉴定实验，了解免疫反应',
    topics: ['免疫学', '血型系统', '抗原抗体']
  }
])

const concepts = ref([
  {
    id: 1,
    title: '细胞理论',
    description: '生命的基本单位',
    points: [
      '所有生物都由细胞组成',
      '细胞是生命活动的基本单位',
      '新细胞来自已存在的细胞'
    ]
  },
  {
    id: 2,
    title: '遗传规律',
    description: '基因传递的基本规律',
    points: [
      '孟德尔遗传定律',
      '基因的显隐性关系',
      '基因的分离和组合'
    ]
  },
  {
    id: 3,
    title: '进化理论',
    description: '物种起源和演化',
    points: [
      '自然选择学说',
      '适者生存原理',
      '物种的适应性进化'
    ]
  },
  {
    id: 4,
    title: '生态系统',
    description: '生物与环境的关系',
    points: [
      '食物链和食物网',
      '能量流动和物质循环',
      '生态平衡的维持'
    ]
  }
])

const startExperiment = (experiment: any) => {
  // 跳转到聊天页面，并预设问题
  router.push({
    path: '/chat',
    query: {
      question: `我想了解${experiment.title}的相关知识，请详细介绍一下实验原理、步骤和注意事项。`
    }
  })
}
</script>

<style scoped>
.biology-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  color: white;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
}

.experiment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.experiment-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.experiment-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.experiment-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.experiment-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #fff;
}

.experiment-card p {
  margin-bottom: 1.5rem;
  opacity: 0.9;
  line-height: 1.6;
}

.experiment-topics {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.topic-tag {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.start-btn {
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.start-btn:hover {
  background: linear-gradient(45deg, #ee5a24, #ff6b6b);
  transform: scale(1.05);
}

.biology-concepts {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.biology-concepts h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.concepts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.concept-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.concept-card h4 {
  color: #ffd700;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.concept-card p {
  margin-bottom: 1rem;
  opacity: 0.9;
  font-style: italic;
}

.concept-card ul {
  list-style: none;
  padding: 0;
}

.concept-card li {
  padding: 0.3rem 0;
  position: relative;
  padding-left: 1.5rem;
}

.concept-card li::before {
  content: '🧬';
  position: absolute;
  left: 0;
  top: 0.3rem;
}

@media (max-width: 768px) {
  .biology-container {
    padding: 1rem;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .experiment-grid {
    grid-template-columns: 1fr;
  }
  
  .concepts-grid {
    grid-template-columns: 1fr;
  }
}
</style> 