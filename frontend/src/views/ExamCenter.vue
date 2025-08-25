<template>
  <div class="exam-center-container">
    <h1 class="page-title">组卷中心</h1>

    <el-row :gutter="20">
      <!-- 左侧筛选面板 -->
      <el-col :span="6">
        <el-card class="filter-card">
          <template #header>
            <div class="filter-header">
              <span>筛选条件</span>
              <el-button type="primary" size="small" @click="filterQuestions">应用筛选</el-button>
            </div>
          </template>
          
          <div class="filter-section">
            <h3 class="filter-title">题型</h3>
            <el-checkbox-group v-model="filters.questionTypes">
              <el-checkbox label="single">单选题</el-checkbox>
              <el-checkbox label="multiple">多选题</el-checkbox>
              <el-checkbox label="fill">填空题</el-checkbox>
              <el-checkbox label="essay">简答题</el-checkbox>
            </el-checkbox-group>
          </div>
          
          <div class="filter-section">
            <h3 class="filter-title">知识点</h3>
            <el-tree
              ref="knowledgeTree"
              :data="knowledgePoints"
              show-checkbox
              node-key="id"
              :default-expanded-keys="[1]"
              :props="{
                children: 'children',
                label: 'name'
              }"
            />
          </div>
          
          <div class="filter-section">
            <h3 class="filter-title">难度系数</h3>
            <el-slider
              v-model="filters.difficulty"
              range
              :min="1"
              :max="5"
              :marks="{
                1: '简单',
                3: '中等',
                5: '困难'
              }"
            />
          </div>
          
          <div class="filter-section">
            <h3 class="filter-title">最近使用</h3>
            <el-select v-model="filters.lastUsed" placeholder="请选择" style="width: 100%">
              <el-option label="全部" value="" />
              <el-option label="1周内" value="1week" />
              <el-option label="1月内" value="1month" />
              <el-option label="3月内" value="3months" />
              <el-option label="从未使用" value="never" />
            </el-select>
          </div>
        </el-card>

        <!-- 智能推荐卡片 -->
        <el-card class="recommendation-card">
          <template #header>
            <div class="card-header">
              <span>智能推荐题目</span>
            </div>
          </template>
          <div class="student-selector">
            <el-select v-model="selectedStudent" placeholder="选择学生" style="width: 100%">
              <el-option
                v-for="student in students"
                :key="student.id"
                :label="student.name"
                :value="student.id"
              />
            </el-select>
            <el-button type="primary" @click="recommendQuestions" style="width: 100%; margin-top: 10px">
              获取推荐题目
            </el-button>
          </div>
          <div v-if="hasRecommendation" class="recommendation-info">
            <el-alert
              title="已为该学生生成个性化推荐"
              type="success"
              :closable="false"
              show-icon
            >
              <p>根据学习情况分析，建议重点练习以下知识点:</p>
              <ul>
                <li v-for="(point, index) in recommendationPoints" :key="index">
                  {{ point }}
                </li>
              </ul>
            </el-alert>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧题目列表和试卷区域 -->
      <el-col :span="18">
        <el-card class="questions-card">
          <template #header>
            <div class="questions-header">
              <div class="left">
                <span class="title">题库</span>
                <el-tag type="info">共 {{ totalQuestions }} 题</el-tag>
              </div>
              <div class="right">
                <el-input
                  v-model="searchQuery"
                  placeholder="搜索题目"
                  prefix-icon="el-icon-search"
                  style="width: 250px; margin-right: 10px;"
                  @input="searchQuestions"
                />
                <el-button type="primary" @click="openNewPaperDialog">自动组卷</el-button>
              </div>
            </div>
          </template>

          <!-- 题目列表 -->
          <el-table
            v-loading="loading"
            :data="questions"
            style="width: 100%"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="50" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="title" label="题目" min-width="350">
              <template #default="scope">
                <div class="question-title" v-html="scope.row.title"></div>
                <el-tag size="small" :type="getQuestionTypeTag(scope.row.type)">
                  {{ getQuestionTypeText(scope.row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="knowledgePoint" label="知识点" width="120" />
            <el-table-column prop="difficulty" label="难度" width="120">
              <template #default="scope">
                <el-rate
                  v-model="scope.row.difficulty"
                  disabled
                  text-color="#ff9900"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button size="small" @click="showQuestionPreview(scope.row)">预览</el-button>
                <el-button
                  size="small"
                  type="primary"
                  @click="addToPaper(scope.row)"
                >添加</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination-container">
            <el-pagination
              background
              layout="total, sizes, prev, pager, next"
              :current-page="currentPage"
              :page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="totalQuestions"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-card>

        <!-- 当前组卷区域 -->
        <el-card class="paper-card" v-if="currentPaper.questions.length > 0">
          <template #header>
            <div class="paper-header">
              <div class="left">
                <span class="title">当前试卷</span>
                <el-tag type="success">{{ currentPaper.questions.length }} 题</el-tag>
              </div>
              <div class="right">
                <el-button size="small" @click="clearPaper">清空</el-button>
                <el-button type="primary" @click="savePaper">保存试卷</el-button>
              </div>
            </div>
          </template>

          <el-table :data="currentPaper.questions" style="width: 100%">
            <el-table-column type="index" width="50" />
            <el-table-column prop="title" label="题目" min-width="350">
              <template #default="scope">
                <div class="question-title" v-html="scope.row.title"></div>
              </template>
            </el-table-column>
            <el-table-column prop="score" label="分值" width="100">
              <template #default="scope">
                <el-input-number v-model="scope.row.score" :min="1" :max="20" size="small" />
              </template>
            </el-table-column>
            <el-table-column prop="difficulty" label="难度" width="120">
              <template #default="scope">
                <el-rate
                  v-model="scope.row.difficulty"
                  disabled
                  text-color="#ff9900"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template #default="scope">
                <el-button
                  size="small"
                  type="danger"
                  @click="removeFromPaper(scope.$index)"
                >删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="paper-summary">
            <div class="summary-item">
              <span>总题数:</span>
              <span class="value">{{ currentPaper.questions.length }}</span>
            </div>
            <div class="summary-item">
              <span>总分:</span>
              <span class="value">{{ totalScore }}</span>
            </div>
            <div class="summary-item">
              <span>平均难度:</span>
              <span class="value">{{ averageDifficulty }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 自动组卷对话框 -->
    <el-dialog
      title="自动组卷"
      v-model="newPaperDialogVisible"
      width="50%"
    >
      <el-form :model="newPaperForm" label-width="120px">
        <el-form-item label="试卷名称">
          <el-input v-model="newPaperForm.name" placeholder="请输入试卷名称" />
        </el-form-item>
        <el-form-item label="总分值">
          <el-input-number v-model="newPaperForm.totalScore" :min="1" :max="150" />
        </el-form-item>
        <el-form-item label="难度分布">
          <el-slider
            v-model="newPaperForm.difficultyDistribution"
            range
            :marks="{
              0: '简单',
              50: '中等',
              100: '困难'
            }"
          />
        </el-form-item>
        <el-form-item label="题型分布">
          <el-row :gutter="10">
            <el-col :span="12">
              <div class="question-type-item">
                <span>单选题:</span>
                <el-input-number v-model="newPaperForm.typeDistribution.single" :min="0" :max="50" size="small" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="question-type-item">
                <span>多选题:</span>
                <el-input-number v-model="newPaperForm.typeDistribution.multiple" :min="0" :max="50" size="small" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="question-type-item">
                <span>填空题:</span>
                <el-input-number v-model="newPaperForm.typeDistribution.fill" :min="0" :max="50" size="small" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="question-type-item">
                <span>解答题:</span>
                <el-input-number v-model="newPaperForm.typeDistribution.essay" :min="0" :max="50" size="small" />
              </div>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="针对学生">
          <el-select v-model="newPaperForm.studentId" placeholder="选择特定学生（可选）" clearable style="width: 100%">
            <el-option
              v-for="student in students"
              :key="student.id"
              :label="student.name"
              :value="student.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="newPaperDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="generatePaper">生成试卷</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 题目预览对话框 -->
    <el-dialog
      title="题目预览"
      v-model="previewDialogVisible"
      width="50%"
    >
      <div v-if="previewQuestion" class="question-preview">
        <div class="question-header">
          <el-tag size="small" :type="getQuestionTypeTag(previewQuestion.type)">
            {{ getQuestionTypeText(previewQuestion.type) }}
          </el-tag>
          <el-rate v-model="previewQuestion.difficulty" disabled text-color="#ff9900" />
        </div>
        <div class="question-content" v-html="previewQuestion.title"></div>
        
        <template v-if="['single', 'multiple'].includes(previewQuestion.type)">
          <div class="options">
            <div v-for="(option, index) in previewQuestion.options" :key="index" class="option">
              <div class="option-label">{{ String.fromCharCode(65 + index) }}.</div>
              <div class="option-content" v-html="option.content"></div>
            </div>
          </div>
        </template>
        
        <div class="answer-section">
          <div class="section-title">答案:</div>
          <div class="answer-content" v-html="previewQuestion.answer"></div>
        </div>
        
        <div class="analysis-section" v-if="previewQuestion.analysis">
          <div class="section-title">解析:</div>
          <div class="analysis-content" v-html="previewQuestion.analysis"></div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { examApi } from '../api'
import { useStudentsStore } from '../store'

// 页面状态
const loading = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalQuestions = ref(0)
const selectedQuestions = ref([])
const selectedStudent = ref(null)
const hasRecommendation = ref(false)


// 弹窗控制
const newPaperDialogVisible = ref(false)
const previewDialogVisible = ref(false)
const previewQuestion = ref(null)

// 学生数据
const studentsStore = useStudentsStore()
const students = computed(() => studentsStore.getStudents)
const recommendationPoints = ref([
  '细胞结构与功能',
  '遗传与变异的规律',
  '生态系统与物质循环'
])

// 筛选条件
const filters = reactive({
  questionTypes: [],
  difficulty: [1, 5],
  lastUsed: ''
})

// 知识点树形数据
const knowledgePoints = ref([
  {
    id: 1,
    name: '生物',
    children: [
      {
        id: 11,
        name: '细胞与分子',
        children: [
          { id: 111, name: '细胞结构与功能' },
          { id: 112, name: '细胞代谢与呼吸' },
          { id: 113, name: '光合作用' }
        ]
      },
      {
        id: 12,
        name: '遗传与进化',
        children: [
          { id: 121, name: '遗传的基本规律' },
          { id: 122, name: '基因与染色体' },
          { id: 123, name: '生物的进化' }
        ]
      },
      {
        id: 13,
        name: '生态与稳态',
        children: [
          { id: 131, name: '生态系统结构与功能' },
          { id: 132, name: '种群与群落' },
          { id: 133, name: '内环境与稳态' }
        ]
      },
      {
        id: 14,
        name: '生命活动的调节',
        children: [
          { id: 141, name: '神经调节' },
          { id: 142, name: '体液调节与免疫' },
          { id: 143, name: '植物生命活动调节' }
        ]
      }
    ]
  }
])

// 题目列表数据
const questions = ref([])

// 模拟题目数据
const generateMockQuestions = () => {
  const mockQuestions = []
  
  for (let i = 1; i <= 100; i++) {
    const type = ['single', 'multiple', 'fill', 'essay'][Math.floor(Math.random() * 4)]
    const difficulty = Math.floor(Math.random() * 5) + 1
    const knowledgePointIndex = Math.floor(Math.random() * recommendationPoints.value.length)
    
    const question = {
      id: i,
      title: `这是第${i}道${getQuestionTypeText(type)}，难度${difficulty}星，涉及${recommendationPoints.value[knowledgePointIndex]}相关内容。`,
      type: type,
      difficulty: difficulty,
      knowledgePoint: recommendationPoints.value[knowledgePointIndex],
      score: difficulty * 2,
      answer: '这里是答案内容',
      analysis: '这里是解析内容'
    }
    
    if (type === 'single' || type === 'multiple') {
      question.options = [
        { label: 'A', content: '选项A的内容' },
        { label: 'B', content: '选项B的内容' },
        { label: 'C', content: '选项C的内容' },
        { label: 'D', content: '选项D的内容' }
      ]
    }
    
    mockQuestions.push(question)
  }
  
  return mockQuestions
}

// 当前试卷数据
const currentPaper = reactive({
  name: '',
  questions: []
})

// 新试卷表单
const newPaperForm = reactive({
  name: '',
  totalScore: 100,
  difficultyDistribution: [20, 80],
  typeDistribution: {
    single: 10,
    multiple: 5,
    fill: 5,
    essay: 5
  },
  studentId: null
})

// 计算属性
const totalScore = computed(() => {
  return currentPaper.questions.reduce((sum, q) => sum + q.score, 0)
})

const averageDifficulty = computed(() => {
  if (currentPaper.questions.length === 0) return 0
  const sum = currentPaper.questions.reduce((sum, q) => sum + q.difficulty, 0)
  return (sum / currentPaper.questions.length).toFixed(1)
})

// 方法
const getQuestionTypeText = (type) => {
  const types = {
    single: '单选题',
    multiple: '多选题',
    fill: '填空题',
    essay: '简答题'
  }
  return types[type] || '未知题型'
}

const getQuestionTypeTag = (type) => {
  const tags = {
    single: '',
    multiple: 'success',
    fill: 'info',
    essay: 'warning'
  }
  return tags[type] || ''
}

const handleSelectionChange = (val) => {
  selectedQuestions.value = val
}

const showQuestionPreview = (question) => {
  previewDialogVisible.value = true
  previewQuestion.value = question
}

const addToPaper = (question) => {
  const newQuestion = { ...question }
  currentPaper.questions.push(newQuestion)
}

const removeFromPaper = (index) => {
  currentPaper.questions.splice(index, 1)
}

const clearPaper = () => {
  currentPaper.questions = []
}

const savePaper = () => {
  // 实际应用中这里会调用API保存试卷
  alert(`试卷已保存，包含 ${currentPaper.questions.length} 题，总分 ${totalScore.value} 分`)
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchQuestions()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchQuestions()
}

const searchQuestions = () => {
  currentPage.value = 1
  fetchQuestions()
}

const filterQuestions = () => {
  currentPage.value = 1
  fetchQuestions()
}

const recommendQuestions = () => {
  if (!selectedStudent.value) {
    alert('请先选择学生')
    return
  }
  
  // 模拟API调用
  loading.value = true
  setTimeout(() => {
    hasRecommendation.value = true
    loading.value = false
    fetchQuestions()
  }, 1000)
}

const fetchQuestions = async () => {
  loading.value = true
  try {
    // 模拟API调用
    setTimeout(() => {
      const allQuestions = generateMockQuestions()
      totalQuestions.value = allQuestions.length
      
      // 简单模拟筛选和分页
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      questions.value = allQuestions.slice(start, end)
      
      loading.value = false
    }, 500)
    
    // 实际API调用
    /*
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      query: searchQuery.value,
      questionTypes: filters.questionTypes,
      difficultyMin: filters.difficulty[0],
      difficultyMax: filters.difficulty[1],
      lastUsed: filters.lastUsed,
      knowledgePoints: knowledgeTree.value?.getCheckedKeys() || []
    }
    
    if (selectedStudent.value && hasRecommendation.value) {
      params.recommendedForStudent = selectedStudent.value
    }
    
    const response = await examApi.getQuestions(params)
    questions.value = response.data.items
    totalQuestions.value = response.data.total
    */
  } catch (error) {
    console.error('Failed to fetch questions', error)
  } finally {
    loading.value = false
  }
}

const openNewPaperDialog = () => {
  newPaperDialogVisible.value = true
}

const generatePaper = () => {
  // 模拟自动组卷
  loading.value = true
  setTimeout(() => {
    // 清空现有试卷
    currentPaper.questions = []
    currentPaper.name = newPaperForm.name
    
    // 随机选择题目
    const allQuestions = generateMockQuestions()
    const totalQuestionsNeeded = Object.values(newPaperForm.typeDistribution).reduce((a, b) => a + b, 0)
    
    // 确保题目总数不超过可用题目数
    const availableQuestions = Math.min(totalQuestionsNeeded, allQuestions.length)
    
    // 随机选择题目
    const randomQuestions = []
    const usedIndexes = new Set()
    
    for (let i = 0; i < availableQuestions; i++) {
      let randomIndex
      do {
        randomIndex = Math.floor(Math.random() * allQuestions.length)
      } while (usedIndexes.has(randomIndex))
      
      usedIndexes.add(randomIndex)
      randomQuestions.push(allQuestions[randomIndex])
    }
    
    // 添加到试卷
    randomQuestions.forEach(q => {
      currentPaper.questions.push({ ...q })
    })
    
    loading.value = false
    newPaperDialogVisible.value = false
  }, 1000)
}

// 生命周期钩子
onMounted(() => {
  fetchQuestions()
  
  // 获取学生列表（实际应该调用API）
  studentsStore.setStudents([
    { id: 1, name: '张三 (高三1班)' },
    { id: 2, name: '李四 (高三2班)' },
    { id: 3, name: '王五 (高三1班)' }
  ])
})
</script>

<style scoped>
.exam-center-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 600;
  color: #333;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-section {
  margin-bottom: 20px;
}

.filter-title {
  font-size: 14px;
  margin-bottom: 10px;
  color: #606266;
}

.recommendation-card {
  margin-bottom: 20px;
}

.student-selector {
  margin-bottom: 15px;
}

.recommendation-info {
  margin-top: 15px;
}

.questions-card {
  margin-bottom: 20px;
}

.questions-header,
.paper-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.questions-header .title,
.paper-header .title {
  font-size: 16px;
  font-weight: bold;
  margin-right: 10px;
}

.questions-header .left,
.paper-header .left {
  display: flex;
  align-items: center;
}

.question-title {
  margin-bottom: 5px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.paper-summary {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.summary-item {
  margin-left: 20px;
  font-size: 14px;
}

.summary-item .value {
  font-weight: bold;
  color: #409EFF;
  margin-left: 5px;
}

.question-type-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.question-preview {
  padding: 10px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-content {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.options {
  margin-bottom: 20px;
}

.option {
  display: flex;
  margin-bottom: 10px;
}

.option-label {
  width: 30px;
  font-weight: bold;
}

.section-title {
  font-weight: bold;
  margin-bottom: 10px;
  color: #409EFF;
}

.answer-section,
.analysis-section {
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #EBEEF5;
}

.card-header {
  font-weight: bold;
}
</style> 