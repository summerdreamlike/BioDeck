<template>
  <div class="document-viewer-overlay" @click="$emit('close')">
    <div class="document-viewer" @click.stop>
      <div class="viewer-header">
        <h3>{{ documentName }}</h3>
        <div class="viewer-actions">
          <el-button @click="downloadFile" type="primary" size="small">
            <el-icon><Download /></el-icon>
            下载
          </el-button>
          <el-button @click="$emit('close')" size="small">
            <el-icon><Close /></el-icon>
            关闭
          </el-button>
        </div>
      </div>
      
      <div class="viewer-content">
        <!-- PPT文件显示 -->
        <div v-if="isPPT" class="ppt-viewer">
          <div class="ppt-placeholder">
            <el-icon size="64" color="#409EFF"><Document /></el-icon>
            <h4>{{ documentName }}</h4>
            <p>这是一个PowerPoint演示文稿</p>
            <div class="ppt-actions">
              <el-button @click="downloadFile" type="primary" size="large">
                <el-icon><Download /></el-icon>
                下载查看
              </el-button>
              <p class="hint">点击下载后在本地打开查看</p>
            </div>
          </div>
        </div>
        
        <!-- PDF文件显示 -->
        <div v-else-if="isPDF" class="pdf-viewer">
          <iframe 
            v-if="pdfUrl" 
            :src="pdfUrl" 
            width="100%" 
            height="600"
            frameborder="0">
          </iframe>
          <div v-else class="pdf-placeholder">
            <el-icon size="64" color="#67C23A"><Document /></el-icon>
            <h4>PDF加载中...</h4>
          </div>
        </div>
        
        <!-- 其他文件类型 -->
        <div v-else class="file-viewer">
          <div class="file-placeholder">
            <el-icon size="64" color="#E6A23C"><Document /></el-icon>
            <h4>{{ documentName }}</h4>
            <p>此文件类型暂不支持在线预览</p>
            <el-button @click="downloadFile" type="primary" size="large">
              <el-icon><Download /></el-icon>
              下载文件
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Download, Close, Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  document: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const pdfUrl = ref('')

// 计算属性
const documentName = computed(() => props.document?.name || '未知文档')
const isPPT = computed(() => {
  const name = documentName.value.toLowerCase()
  return name.endsWith('.ppt') || name.endsWith('.pptx')
})
const isPDF = computed(() => {
  const name = documentName.value.toLowerCase()
  return name.endsWith('.pdf')
})

// 下载文件
function downloadFile() {
  try {
    // 尝试使用webpack处理后的文件路径
    const fileName = props.document.name
    const fileUrl = props.document.url
    
    if (fileUrl && fileUrl !== '#') {
      // 创建下载链接
      const link = document.createElement('a')
      link.href = fileUrl
      link.download = fileName
      link.target = '_blank'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      ElMessage.success('开始下载文件')
    } else {
      ElMessage.warning('文件链接无效，无法下载')
    }
  } catch (error) {
    console.error('下载失败:', error)
    ElMessage.error('下载失败，请重试')
  }
}

// 组件挂载时处理PDF
onMounted(() => {
  if (isPDF.value && props.document?.url && props.document.url !== '#') {
    pdfUrl.value = props.document.url
  }
})
</script>

<style scoped>
.document-viewer-overlay {
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

.document-viewer {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  max-width: 90vw;
  max-height: 90vh;
  width: 600px;
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

.viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.viewer-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.viewer-actions {
  display: flex;
  gap: 12px;
}

.viewer-content {
  padding: 32px;
  min-height: 400px;
}

.ppt-viewer,
.pdf-viewer,
.file-viewer {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.ppt-placeholder,
.pdf-placeholder,
.file-placeholder {
  text-align: center;
  padding: 48px 32px;
  border: 2px dashed #e4e7ed;
  border-radius: 16px;
  background: #fafafa;
  width: 100%;
}

.ppt-placeholder h4,
.pdf-placeholder h4,
.file-placeholder h4 {
  margin: 20px 0 12px 0;
  color: #303133;
  font-size: 18px;
  font-weight: 600;
}

.ppt-placeholder p,
.pdf-placeholder p,
.file-placeholder p {
  margin: 12px 0 24px 0;
  color: #606266;
  font-size: 14px;
}

.ppt-actions {
  margin-top: 24px;
}

.hint {
  margin-top: 12px;
  font-size: 12px;
  color: #909399;
  font-style: italic;
}

.pdf-viewer iframe {
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .document-viewer {
    max-width: 95vw;
    width: 95vw;
    margin: 20px;
  }
  
  .viewer-header {
    padding: 20px;
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .viewer-content {
    padding: 24px;
  }
  
  .ppt-placeholder,
  .pdf-placeholder,
  .file-placeholder {
    padding: 32px 20px;
  }
}
</style> 