<template>
  <div class="teaching-materials-container">
    <h1 class="page-title">教学课件</h1>
    
    <el-row :gutter="20">
      <!-- 左侧分类树 -->
      <el-col :span="5">
        <el-card class="category-card">
          <template #header>
            <div class="card-header">
              <span>资源分类</span>
              <el-button
                size="small"
                type="text"
                @click="openCategoryDialog"
              >
                <el-icon><el-icon-plus /></el-icon>
              </el-button>
            </div>
          </template>
          
          <el-tree
            :data="categories"
            :props="{ label: 'name', children: 'children' }"
            highlight-current
            node-key="id"
            default-expand-all
            @node-click="handleCategorySelect"
          />
        </el-card>
        
        <el-card class="tag-card">
          <template #header>
            <div class="card-header">
              <span>常用标签</span>
            </div>
          </template>
          
          <div class="tags-container">
            <el-tag
              v-for="tag in popularTags"
              :key="tag.id"
              :type="tag.type"
              style="margin: 0 5px 5px 0"
              effect="light"
              @click="filterByTag(tag)"
            >
              {{ tag.name }} ({{ tag.count }})
            </el-tag>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧内容区 -->
      <el-col :span="19">
        <!-- 工具栏 -->
        <div class="toolbar">
          <div class="search-box">
            <el-input
              v-model="searchQuery"
              placeholder="搜索课件"
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><el-icon-search /></el-icon>
              </template>
            </el-input>
          </div>
          
          <div class="filter-actions">
            <el-select v-model="fileType" placeholder="文件类型" clearable @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option label="文档" value="document" />
              <el-option label="视频" value="video" />
              <el-option label="音频" value="audio" />
              <el-option label="图片" value="image" />
              <el-option label="H5课件" value="h5" />
            </el-select>
            
            <el-select v-model="sortBy" placeholder="排序方式" @change="handleSearch">
              <el-option label="最新上传" value="uploadTime" />
              <el-option label="最多浏览" value="viewCount" />
              <el-option label="名称" value="name" />
            </el-select>
          </div>
          
          <div class="action-buttons">
            <el-button type="primary" @click="openUploadDialog">
              <el-icon><el-icon-upload /></el-icon>
              上传课件
            </el-button>
          </div>
        </div>
        
        <!-- 面包屑导航 -->
        <div class="breadcrumb">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/teaching-materials' }">全部</el-breadcrumb-item>
            <el-breadcrumb-item v-for="(item, index) in currentPath" :key="index">
              {{ item.name }}
            </el-breadcrumb-item>
          </el-breadcrumb>
          
          <div v-if="selectedTag" class="selected-tag">
            <span>当前标签:</span>
            <el-tag size="small" closable @close="clearTagFilter">
              {{ selectedTag.name }}
            </el-tag>
          </div>
        </div>
        
        <!-- 内容展示区 -->
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="10" animated />
        </div>
        
        <div v-else-if="materials.length === 0" class="empty-container">
          <el-empty description="暂无课件资源" />
        </div>
        
        <div v-else class="materials-container">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="material in materials" :key="material.id">
              <el-card class="material-card" shadow="hover" @click="showMaterialPreview(material)">
                <div class="material-thumbnail">
                  <el-image 
                    :src="material.thumbnail" 
                    fit="cover"
                    :preview-src-list="material.type === 'image' ? [material.url] : []"
                  />
                  <div class="material-type">
                    <el-tag size="small" :type="getFileTypeTag(material.type)">
                      {{ getFileTypeText(material.type) }}
                    </el-tag>
                  </div>
                </div>
                
                <div class="material-info">
                  <div class="material-name">{{ material.name }}</div>
                  <div class="material-meta">
                    <span class="upload-time">{{ formatDate(material.uploadTime) }}</span>
                    <span class="view-count">
                      <el-icon><el-icon-view /></el-icon>
                      {{ material.viewCount }}
                    </span>
                  </div>
                  
                  <div class="material-tags">
                    <el-tag 
                      v-for="tag in material.tags.slice(0, 3)" 
                      :key="tag.id"
                      size="small" 
                      effect="plain"
                      style="margin-right: 5px"
                      @click.stop="filterByTag(tag)"
                    >
                      {{ tag.name }}
                    </el-tag>
                    <span v-if="material.tags.length > 3" class="more-tags">+{{ material.tags.length - 3 }}</span>
                  </div>
                </div>
                
                <div class="material-actions">
                  <el-button size="small" @click.stop="downloadMaterial(material)">
                    <el-icon><el-icon-download /></el-icon>
                  </el-button>
                  <el-button size="small" @click.stop="openMaterial(material)">
                    <el-icon><el-icon-view /></el-icon>
                  </el-button>
                  <el-dropdown @command="(cmd) => handleCommand(cmd, material)" trigger="click" @click.stop>
                    <el-button size="small">
                      <el-icon><el-icon-more /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="edit">编辑</el-dropdown-item>
                        <el-dropdown-item command="share">分享</el-dropdown-item>
                        <el-dropdown-item command="delete" style="color: #F56C6C">删除</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <div class="pagination-container">
            <el-pagination
              :current-page="currentPage"
              :page-size="pageSize"
              :page-sizes="[12, 24, 36, 48]"
              layout="total, sizes, prev, pager, next"
              :total="total"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </div>
      </el-col>
    </el-row>
    
    <!-- 上传课件对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传课件"
      width="500px"
    >
      <el-form :model="uploadForm" label-width="80px">
        <el-form-item label="课件名称">
          <el-input v-model="uploadForm.name" placeholder="请输入课件名称" />
        </el-form-item>
        
        <el-form-item label="分类">
          <el-cascader
            v-model="uploadForm.categoryPath"
            :options="categories"
            :props="{ checkStrictly: true, label: 'name', value: 'id', children: 'children' }"
            placeholder="请选择分类"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="标签">
          <el-select
            v-model="uploadForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请输入标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in availableTags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="文件">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
          >
            <el-icon class="el-icon--upload"><el-icon-upload-filled /></el-icon>
            <div class="el-upload__text">拖拽文件到此处或 <em>点击上传</em></div>
            <template #tip>
              <div class="el-upload__tip">
                支持上传PDF、Word、PPT、视频、音频、图片等格式文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input
            v-model="uploadForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入课件描述（可选）"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUpload">上传</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 新增分类对话框 -->
    <el-dialog
      v-model="categoryDialogVisible"
      title="新增分类"
      width="400px"
    >
      <el-form :model="categoryForm" label-width="80px">
        <el-form-item label="父级分类">
          <el-cascader
            v-model="categoryForm.parentId"
            :options="categories"
            :props="{ checkStrictly: true, label: 'name', value: 'id', children: 'children' }"
            placeholder="请选择父级分类（可选）"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="分类名称">
          <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="categoryDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCategory">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      :title="previewMaterial?.name"
      width="70%"
      class="preview-dialog"
    >
      <div v-if="previewMaterial" class="preview-container">
        <!-- 文档预览 -->
        <div v-if="previewMaterial.type === 'document'" class="document-preview">
          <iframe :src="previewMaterial.previewUrl" frameborder="0"></iframe>
        </div>
        
        <!-- 视频预览 -->
        <div v-else-if="previewMaterial.type === 'video'" class="video-preview">
          <video controls :src="previewMaterial.url" style="width: 100%"></video>
        </div>
        
        <!-- 音频预览 -->
        <div v-else-if="previewMaterial.type === 'audio'" class="audio-preview">
          <audio controls :src="previewMaterial.url" style="width: 100%"></audio>
          <div class="audio-waveform" style="width: 100%; height: 100px; background-color: #f5f7fa; margin-top: 10px"></div>
        </div>
        
        <!-- 图片预览 -->
        <div v-else-if="previewMaterial.type === 'image'" class="image-preview">
          <el-image :src="previewMaterial.url" style="max-width: 100%; max-height: 70vh" />
        </div>
        
        <!-- H5课件预览 -->
        <div v-else-if="previewMaterial.type === 'h5'" class="h5-preview">
          <iframe :src="previewMaterial.url" frameborder="0" style="width: 100%; height: 70vh"></iframe>
        </div>
        
        <div class="preview-info">
          <div class="preview-meta">
            <div class="meta-item">
              <span class="label">上传时间:</span>
              <span class="value">{{ formatDate(previewMaterial.uploadTime) }}</span>
            </div>
            <div class="meta-item">
              <span class="label">文件大小:</span>
              <span class="value">{{ formatSize(previewMaterial.size) }}</span>
            </div>
            <div class="meta-item">
              <span class="label">浏览次数:</span>
              <span class="value">{{ previewMaterial.viewCount }}</span>
            </div>
          </div>
          
          <div class="preview-description" v-if="previewMaterial.description">
            <div class="label">描述:</div>
            <div class="value">{{ previewMaterial.description }}</div>
          </div>
          
          <div class="preview-tags">
            <span class="label">标签:</span>
            <el-tag
              v-for="tag in previewMaterial.tags"
              :key="tag.id"
              size="small"
              style="margin: 0 5px 5px 0"
            >
              {{ tag.name }}
            </el-tag>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { materialsApi } from '../api'

// 状态变量
const searchQuery = ref('')
const fileType = ref('')
const sortBy = ref('uploadTime')
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)
const loading = ref(false)
const selectedTag = ref(null)
const currentCategory = ref(null)
const currentPath = ref([])

// 对话框控制
const uploadDialogVisible = ref(false)
const categoryDialogVisible = ref(false)
const previewDialogVisible = ref(false)
const previewMaterial = ref(null)

// 表单数据
const uploadForm = reactive({
  name: '',
  categoryPath: [],
  tags: [],
  file: null,
  description: ''
})

const categoryForm = reactive({
  name: '',
  parentId: null
})

// 模拟数据
const categories = ref([
  {
    id: 1,
    name: '生物',
    children: [
      { id: 11, name: '高一生物', children: [] },
      { id: 12, name: '高二生物', children: [] },
      { id: 13, name: '高三生物', children: [
        { id: 131, name: '细胞与分子', children: [] },
        { id: 132, name: '遗传与进化', children: [] },
        { id: 133, name: '生态与稳态', children: [] }
      ] }
    ]
  }
])

const popularTags = ref([
  { id: 1, name: '高考真题', count: 24, type: '' },
  { id: 2, name: '重难点', count: 18, type: 'success' },
  { id: 3, name: '模拟试题', count: 15, type: 'warning' },
  { id: 4, name: '基础知识', count: 12, type: 'info' },
  { id: 5, name: '解题方法', count: 10, type: 'danger' }
])

const availableTags = ref([
  { id: 1, name: '高考真题' },
  { id: 2, name: '重难点' },
  { id: 3, name: '模拟试题' },
  { id: 4, name: '基础知识' },
  { id: 5, name: '实验' },
  { id: 6, name: '图解' },
  { id: 7, name: '遗传图谱' },
  { id: 8, name: '显微图' },
  { id: 9, name: '生态案例' },
  { id: 10, name: '错题本' }
])

const materials = ref([])

// 生成模拟数据
const generateMockMaterials = () => {
  const mockMaterials = []
  const types = ['document', 'video', 'audio', 'image', 'h5']
  const names = [
    '高三生物细胞结构与功能',
    '高三生物遗传与变异专题',
    '高三生物生态系统结构与功能',
    '实验设计与探究方法',
    '生物膜与物质运输',
    '呼吸作用与能量转换',
    '内环境稳态与调节',
    '植物激素与生命活动调节',
    '免疫系统与健康',
    '生物多样性与保护'
  ]
  
  for (let i = 1; i <= 50; i++) {
    const type = types[Math.floor(Math.random() * types.length)]
    const nameIndex = Math.floor(Math.random() * names.length)
    const viewCount = Math.floor(Math.random() * 500)
    const date = new Date()
    date.setDate(date.getDate() - Math.floor(Math.random() * 30))
    
    const randomTags = []
    const tagCount = Math.floor(Math.random() * 4) + 1
    const usedTagIds = new Set()
    
    for (let j = 0; j < tagCount; j++) {
      let tagIndex
      do {
        tagIndex = Math.floor(Math.random() * availableTags.value.length)
      } while (usedTagIds.has(tagIndex))
      
      usedTagIds.add(tagIndex)
      randomTags.push(availableTags.value[tagIndex])
    }
    
    let thumbnail
    if (type === 'document') thumbnail = 'https://via.placeholder.com/300x200?text=PDF'
    else if (type === 'video') thumbnail = 'https://via.placeholder.com/300x200?text=Video'
    else if (type === 'audio') thumbnail = 'https://via.placeholder.com/300x200?text=Audio'
    else if (type === 'image') thumbnail = 'https://via.placeholder.com/300x200?text=Image'
    else thumbnail = 'https://via.placeholder.com/300x200?text=H5'
    
    mockMaterials.push({
      id: i,
      name: `${i}-${names[nameIndex]}`,
      type: type,
      url: '#',
      previewUrl: type === 'document' ? 'https://mozilla.github.io/pdf.js/web/viewer.html' : '#',
      thumbnail: thumbnail,
      uploadTime: date,
      size: Math.floor(Math.random() * 100) * 1024 * 1024, // 随机大小，单位字节
      viewCount: viewCount,
      tags: randomTags,
      description: `这是一份${names[nameIndex]}的教学资源，适合高三学生复习使用。`
    })
  }
  
  return mockMaterials
}

// 方法
const handleCategorySelect = (category) => {
  currentCategory.value = category
  selectedTag.value = null
  
  // 构建面包屑路径
  buildCategoryPath(categories.value, category.id, [])
  
  handleSearch()
}

const buildCategoryPath = (cats, targetId, path) => {
  for (const cat of cats) {
    if (cat.id === targetId) {
      path.push(cat)
      currentPath.value = [...path]
      return true
    }
    
    if (cat.children && cat.children.length > 0) {
      path.push(cat)
      const found = buildCategoryPath(cat.children, targetId, path)
      if (found) return true
      path.pop()
    }
  }
  
  return false
}

const filterByTag = (tag) => {
  selectedTag.value = tag
  currentCategory.value = null
  currentPath.value = []
  handleSearch()
}

const clearTagFilter = () => {
  selectedTag.value = null
  handleSearch()
}

const handleSearch = () => {
  currentPage.value = 1
  fetchMaterials()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchMaterials()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchMaterials()
}

const getFileTypeText = (type) => {
  const typeMap = {
    document: '文档',
    video: '视频',
    audio: '音频',
    image: '图片',
    h5: 'H5'
  }
  return typeMap[type] || '未知'
}

const getFileTypeTag = (type) => {
  const typeMap = {
    document: '',
    video: 'success',
    audio: 'warning',
    image: 'info',
    h5: 'danger'
  }
  return typeMap[type] || ''
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
}

const formatSize = (bytes) => {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const showMaterialPreview = (material) => {
  previewMaterial.value = material
  previewDialogVisible.value = true
  // 在实际应用中，这里应该调用API来增加浏览计数
  material.viewCount++
}

const downloadMaterial = (material) => {
  // 实际应用中这里应该调用API下载文件
  alert(`开始下载: ${material.name}`)
}

const openMaterial = (material) => {
  // 实际应用中这里应该在新窗口打开文件
  window.open(material.url, '_blank')
}

const handleCommand = (command, material) => {
  switch (command) {
    case 'edit':
      // 实现编辑功能
      alert(`编辑文件: ${material.name}`)
      break
    case 'share':
      // 实现分享功能
      alert(`分享文件: ${material.name}`)
      break
    case 'delete':
      // 实现删除功能
      if (confirm(`确定要删除文件 ${material.name} 吗？`)) {
        // 调用删除API
        // 然后重新加载数据
        alert(`文件 ${material.name} 已删除`)
        fetchMaterials()
      }
      break
  }
}

const openUploadDialog = () => {
  uploadForm.name = ''
  uploadForm.categoryPath = []
  uploadForm.tags = []
  uploadForm.file = null
  uploadForm.description = ''
  uploadDialogVisible.value = true
}

const handleFileChange = (file) => {
  uploadForm.file = file
  // 可以根据文件名自动填充表单的文件名
  if (!uploadForm.name && file.name) {
    uploadForm.name = file.name.split('.')[0]
  }
}

const submitUpload = () => {
  // 实际应用中这里应该调用API上传文件
  if (!uploadForm.name) {
    alert('请输入课件名称')
    return
  }
  
  if (!uploadForm.file) {
    alert('请选择文件')
    return
  }
  
  // 模拟上传成功
  alert('上传成功')
  uploadDialogVisible.value = false
  fetchMaterials()
}

const openCategoryDialog = () => {
  categoryForm.name = ''
  categoryForm.parentId = null
  categoryDialogVisible.value = true
}

const submitCategory = () => {
  // 实际应用中这里应该调用API创建分类
  if (!categoryForm.name) {
    alert('请输入分类名称')
    return
  }
  
  // 模拟创建成功
  alert('分类创建成功')
  categoryDialogVisible.value = false
  
  // 模拟更新分类树
  if (!categoryForm.parentId) {
    categories.value.push({
      id: Date.now(),
      name: categoryForm.name,
      children: []
    })
  } else {
    // 实际应用中应该递归查找并添加到正确的父节点
  }
}

const fetchMaterials = async () => {
  loading.value = true
  
  try {
    // 模拟API调用
    setTimeout(() => {
      const allMaterials = generateMockMaterials()
      
      // 应用筛选
      let filteredMaterials = [...allMaterials]
      
      if (searchQuery.value) {
        filteredMaterials = filteredMaterials.filter(material => 
          material.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
      }
      
      if (fileType.value) {
        filteredMaterials = filteredMaterials.filter(material => 
          material.type === fileType.value
        )
      }
      
      if (selectedTag.value) {
        filteredMaterials = filteredMaterials.filter(material => 
          material.tags.some(tag => tag.id === selectedTag.value.id)
        )
      }
      
      if (currentCategory.value) {
        // 实际应用中应该检查分类及其子分类
        filteredMaterials = filteredMaterials.filter(material => 
          Math.random() > 0.5 // 模拟分类筛选
        )
      }
      
      // 排序
      if (sortBy.value === 'uploadTime') {
        filteredMaterials.sort((a, b) => new Date(b.uploadTime) - new Date(a.uploadTime))
      } else if (sortBy.value === 'viewCount') {
        filteredMaterials.sort((a, b) => b.viewCount - a.viewCount)
      } else if (sortBy.value === 'name') {
        filteredMaterials.sort((a, b) => a.name.localeCompare(b.name))
      }
      
      // 分页
      total.value = filteredMaterials.length
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      materials.value = filteredMaterials.slice(start, end)
      
      loading.value = false
    }, 500)
    
    // 实际API调用
    /*
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      query: searchQuery.value,
      fileType: fileType.value,
      sortBy: sortBy.value,
      categoryId: currentCategory.value?.id,
      tagId: selectedTag.value?.id
    }
    
    const response = await materialsApi.getMaterials(params)
    materials.value = response.data.items
    total.value = response.data.total
    */
  } catch (error) {
    console.error('获取课件失败', error)
  } finally {
    loading.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  fetchMaterials()
})
</script>

<style scoped>
.teaching-materials-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: 600;
  color: #333;
}

.category-card,
.tag-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  max-width: 300px;
  margin-right: 20px;
}

.filter-actions {
  display: flex;
  gap: 10px;
  margin-right: 20px;
}

.breadcrumb {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.selected-tag {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  color: #606266;
}

.loading-container,
.empty-container {
  padding: 40px 0;
  text-align: center;
}

.materials-container {
  margin-bottom: 20px;
}

.material-card {
  margin-bottom: 20px;
  position: relative;
  transition: transform 0.3s;
}

.material-card:hover {
  transform: translateY(-5px);
}

.material-thumbnail {
  position: relative;
  height: 150px;
  overflow: hidden;
  border-radius: 4px;
}

.material-thumbnail .el-image {
  width: 100%;
  height: 100%;
}

.material-type {
  position: absolute;
  top: 10px;
  right: 10px;
}

.material-info {
  padding: 10px 0;
}

.material-name {
  font-weight: bold;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.material-meta {
  font-size: 12px;
  color: #909399;
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.material-tags {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.more-tags {
  font-size: 12px;
  color: #909399;
}

.material-actions {
  display: flex;
  justify-content: space-around;
  border-top: 1px solid #EBEEF5;
  padding-top: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.preview-container {
  max-height: 80vh;
}

.document-preview iframe,
.h5-preview iframe {
  width: 100%;
  height: 70vh;
  border: none;
}

.preview-info {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #EBEEF5;
}

.preview-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.meta-item {
  display: flex;
  align-items: center;
}

.preview-description {
  margin-bottom: 15px;
}

.preview-tags {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.label {
  font-weight: bold;
  color: #606266;
  margin-right: 5px;
}

.upload-time {
  margin-right: 10px;
}

.view-count {
  display: flex;
  align-items: center;
  gap: 3px;
}

.el-dialog.preview-dialog {
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  margin: 5vh auto !important;
}

.el-dialog.preview-dialog .el-dialog__body {
  flex: 1;
  overflow: auto;
}
</style> 