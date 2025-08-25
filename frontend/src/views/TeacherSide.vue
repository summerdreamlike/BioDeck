<template>
  <el-container class="layout-container">
    <!-- Header 置于顶部 -->
    <el-header class="header">
      <div class="header-left">
        <img :src="logoImage" alt="logo" class="logo-img">
      </div>
      <div class="user-info">
        <el-avatar 
          :size="36" 
          class="user-avatar"
          :src="userAvatar"
        >
          {{ currentTeacherName ? currentTeacherName.charAt(0) : 'T' }}
        </el-avatar>
        <el-dropdown @command="handleCommand" class="user-dropdown">
          <span class="dropdown-link">
            {{ currentTeacherName || '加载中...' }} 
            <el-icon><el-icon-arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <el-container class="main-container">
      <!-- 侧边栏 -->
      <el-aside width="220px" class="sidebar">
        <el-menu :default-active="$route.path" class="menu" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF">
          <el-menu-item index="/dashboard"><el-icon><el-icon-menu /></el-icon><span>学情监控</span></el-menu-item>
          <el-menu-item index="/exam-center"><el-icon><el-icon-document /></el-icon><span>组卷中心</span></el-menu-item>
          <el-menu-item index="/classroom"><el-icon><el-icon-video-camera /></el-icon><span>在线课堂</span></el-menu-item>
          <el-menu-item index="/teaching-materials"><el-icon><el-icon-folder /></el-icon><span>教学课件</span></el-menu-item>
          <el-menu-item index="/messages"><el-icon><el-icon-bell /></el-icon><span>消息中心</span></el-menu-item>
          <el-menu-item index="/tasks"><el-icon><el-icon-document-checked /></el-icon><span>任务发布</span></el-menu-item>
          <el-menu-item index="/feedback"><el-icon><el-icon-comment /></el-icon><span>反馈收集</span></el-menu-item>
          <el-menu-item index="/attendance"><el-icon><el-icon-user /></el-icon><span>考勤管理</span></el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区域 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store'
import { ElMessage, ElMessageBox } from 'element-plus'
import LogoImage from '../assets/img/Logo.png'

const router = useRouter()
const userStore = useUserStore()

// 当前教师姓名
const currentTeacherName = computed(() => {
  const user = userStore.getUserInfo
  return user ? user.name : '未知用户'
})

// 用户头像（可以后续从用户信息中获取）
const userAvatar = ref('')

// Logo 图片
const logoImage = ref(LogoImage)

// 处理下拉菜单命令
const handleCommand = async (command) => {
  if (command === 'profile') {
    // 跳转到个人中心页面
    ElMessage.info('个人中心功能开发中...')
  } else if (command === 'logout') {
    // 退出登录
    try {
      await ElMessageBox.confirm(
        '确定要退出登录吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )
      
      // 清除用户信息
      userStore.logout()
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      ElMessage.success('退出登录成功')
      router.push('/Login')
    } catch {
      // 用户取消退出
    }
  }
}

// 组件挂载时检查用户登录状态
onMounted(() => {
  // 首先尝试从store获取用户信息
  let user = userStore.getUserInfo
  
  // 如果store中没有用户信息，尝试从localStorage恢复
  if (!user) {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      try {
        user = JSON.parse(storedUser)
        userStore.setUserInfo(user)
      } catch (e) {
        console.error('解析用户信息失败:', e)
      }
    }
  }
  
  // 检查是否有有效的用户信息和token
  const token = localStorage.getItem('token')
  if (!user || !token) {
    // 如果没有用户信息或token，跳转到登录页
    router.push('/Login')
  }
})
</script>

<style scoped>
.layout-container { 
  height: 100vh; 
  display: flex; 
  flex-direction: column; 
}

/* Header 样式 */
.header { 
  background: #fff; 
  border-bottom: 1px solid #e6e6e6; 
  padding: 0 20px; 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  height: 60px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
}

/* 左侧 Logo 区域 */
.header-left {
  display: flex;
  align-items: center;
}

.logo-img {
  height: 40px;
  width: auto;
  object-fit: contain;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo-img:hover {
  transform: scale(1.05);
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
  color: #409EFF;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

/* 右侧用户信息区域 */
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  border: 2px solid #e6e6e6;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-avatar:hover {
  border-color: #409EFF;
  transform: scale(1.05);
}

.user-dropdown {
  display: flex;
  align-items: center;
}

.dropdown-link { 
  display: flex; 
  align-items: center; 
  cursor: pointer; 
  color: #333;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
  user-select: none;
  outline: none;
}

.dropdown-link:hover {
  background-color: #f5f7fa;
  color: #409EFF;
}

.dropdown-link:focus {
  outline: none;
  box-shadow: none;
}

/* 主容器 */
.main-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 侧边栏 */
.sidebar { 
  background-color: #304156; 
  height: 100%; 
  box-shadow: 2px 0 6px rgba(249, 249, 249, 0.1); 
}

.menu { 
  border-right: none; 
  height: 100%; 
}

/* 主内容区域 */
.main-content { 
  background: #f5f7fa; 
  padding: 20px; 
  overflow-y: auto; 
  height: 100%;
}

/* 修复下拉菜单点击时的黑边框问题 */
:deep(.el-dropdown-menu__item:focus) {
  outline: none;
  background-color: #f5f7fa;
}

:deep(.el-dropdown-menu__item:hover) {
  background-color: #ecf5ff;
  color: #409EFF;
}

:deep(.el-dropdown-menu__item.is-disabled) {
  background-color: transparent;
  color: #c0c4cc;
}
</style>


