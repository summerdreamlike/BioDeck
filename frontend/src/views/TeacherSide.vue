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
      <el-aside :width="asideWidth" class="sidebar" :class="[{ collapsed: isCollapsed, 'mobile-open': isMobile && mobileOpen}]">
        <!-- 侧边栏工具栏：折叠按钮（桌面端显示） -->
        <div class="sidebar-tools" v-if="!isMobile">
          <button class="collapse-btn" type="button" @click="isCollapsed = !isCollapsed">
            <el-icon><el-icon-d-arrow-left v-if="!isCollapsed" /><el-icon-d-arrow-right v-else /></el-icon>
            <span class="t">{{ isCollapsed ? '展开' : '折叠' }}</span>
          </button>
        </div>
        <el-menu :default-active="$route.path" class="menu" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF" :collapse="isCollapsed && !isMobile">
          <el-menu-item index="/dashboard"><el-icon><el-icon-menu /></el-icon><span>学情监控</span></el-menu-item>
          <el-menu-item index="/teaching-materials"><el-icon><el-icon-folder /></el-icon><span>教学课件</span></el-menu-item>
          <el-menu-item index="/tasks"><el-icon><el-icon-document-checked /></el-icon><span>作业发布</span></el-menu-item>
          <!-- <el-menu-item index="/feedback"><el-icon><el-icon-comment /></el-icon><span>反馈收集</span></el-menu-item>
          <el-menu-item index="/attendance"><el-icon><el-icon-user /></el-icon><span>考勤管理</span></el-menu-item>
          <el-menu-item index="/exam-center"><el-icon><el-icon-document /></el-icon><span>组卷中心</span></el-menu-item>
          <el-menu-item index="/classroom"><el-icon><el-icon-video-camera /></el-icon><span>在线课堂</span></el-menu-item>
          <el-menu-item index="/messages"><el-icon><el-icon-bell /></el-icon><span>消息中心</span></el-menu-item> -->
        </el-menu>
      </el-aside>
      
      <!-- 主内容区域 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
      <div v-if="isMobile" class="backdrop" :class="{ show: mobileOpen }" @click="mobileOpen=false"></div>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
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

// 响应式：折叠与移动端抽屉
const isCollapsed = ref(false)
const isMobile = ref(false)
const mobileOpen = ref(false)
const asideWidth = computed(() => isMobile.value ? '220px' : (isCollapsed.value ? '74px' : '200px'))

function handleResize() {
  isMobile.value = window.innerWidth < 992
  if (!isMobile.value) mobileOpen.value = false
}

// 处理下拉菜单命令
const handleCommand = async (command) => {
  if (command === 'profile') {
    // 跳转到个人中心页面
    router.push('/TeacherSide/profile')
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
  handleResize()
  window.addEventListener('resize', handleResize)
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

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
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
  height: 75px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
}

/* 左侧 Logo 区域 */
.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}


.logo-img {
  margin-left: 20px;
  height: 60px;
  width: auto;
  object-fit: contain;
  cursor: pointer;
  transition: transform 0.15s ease;
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
  transition: width .25s cubic-bezier(.2,.8,.2,1), transform .25s cubic-bezier(.2,.8,.2,1);
  position: relative;
}

.sidebar-tools { position: absolute; top: 8px; right: 8px; display: inline-flex; align-items: center; justify-content: center; z-index: 1300; }
.collapse-btn { display: inline-flex; align-items: center; gap: 6px; padding: 6px 10px; border-radius: 6px; border: 1px solid rgba(255,255,255,.12); background: rgba(255,255,255,.06); color: #fff; cursor: pointer; transition: all .2s ease; }
.collapse-btn:hover { background: rgba(255,255,255,.14); }
.collapse-btn .t { font-size: 12px; opacity: .85;}

.menu { 
  border-right: none; 
  height: 100%; 
  padding-top: 48px; /* 为悬浮的折叠按钮预留空间，防止菜单项下移 */
}

.sidebar.collapsed :deep(.el-menu-item span) { display: none; }
.sidebar.collapsed :deep(.el-menu-item) { justify-content: center; }

@media (max-width: 991px) {
  .sidebar { position: absolute; left: 0; top: 60px; bottom: 0; transform: translateX(-100%); z-index: 1200; }
  .sidebar.mobile-open { transform: translateX(0); }
}

/* 主内容区域 */
.main-content { 
  background: #f5f7fa; 
  padding: 20px; 
  overflow-y: auto; 
  height: 100%;
}

.backdrop { position: absolute; inset: 60px 0 0 0; background: rgba(0,0,0,.35); opacity: 0; pointer-events: none; transition: opacity .25s ease; }
.backdrop.show { opacity: 1; pointer-events: auto; }

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


